#!python

import datetime
import json
import logging
import os
import socket
import sys

import iptc
import urllib3
from kubernetes import client, watch
from kubernetes.client.rest import ApiException

VERSION = '0.6'


class IpTable:
    ip_cache = set()

    def __init__(self, table: str, chain: str, logger: logging.Logger, access_log: logging.Logger):
        self.table = iptc.Table(table)
        self.logger = logger
        self.access_log = access_log
        self.logger.debug(f'use ip table {self.table.name}')
        if not self.table.is_chain(chain):
            self.logger.debug(f'no chain {chain} in {self.table.name}. creating')
            self.chain = self.table.create_chain(chain)
            self.logger.debug(f'chain {self.chain.name} has been created')
        else:
            self.chain = iptc.Chain(self.table, chain)
        # for s in self.chain.rules:
        #     self.ip_cache.add(s.src)
        self.rule = iptc.Rule()
        self.rule.target = iptc.Target(self.rule, 'ACCEPT')

    def do_log(self, action: str, ip_address: str):
        if self.access_log:
            self.access_log.info(
                json.dumps(
                    {
                        'time': datetime.datetime.now().isoformat(),
                        'host': socket.gethostbyaddr(socket.gethostname())[0],
                        'chain': self.chain.name,
                        'table': self.table.name,
                        'action': action,
                        'ip': ip_address
                    }))

    def add_rule(self, src_ip_set: set):
        existing_rules = list(map(lambda x: x.src.split('/')[0], self.chain.rules))
        self.logger.debug(
            f'existing ip addresses in {self.chain.name}: {existing_rules[0:min(len(existing_rules), 20)]}')
        for src_ip in src_ip_set:
            if src_ip not in existing_rules:
                try:
                    self.rule.src = src_ip
                except ValueError as e:
                    self.logger.critical(f'{e} ({src_ip}) [{src_ip_set}]')
                    sys.exit(1)

                self.chain.insert_rule(self.rule)
                self.logger.info("ip inserted %s" % src_ip)
                self.do_log('add', src_ip)
            else:
                self.logger.info("ip already in list %s" % src_ip)

    def delete_rule(self, src_ip_set: set):
        for src_ip in src_ip_set:
            self.rule.src = src_ip
            try:
                self.chain.delete_rule(self.rule)
                self.logger.info("ip deleted %s" % src_ip)
                self.do_log('delete', src_ip)
            except iptc.ip4tc.IPTCError as e:
                self.logger.critical("error: %s ip %s" % (e, src_ip))

    def sync_list(self, ip_set: set):
        ip_list = list(ip_set)
        self.logger.debug(f'disable autocommit for {self.table.name} current value is {self.table.autocommit}')
        self.table.autocommit = False  # [0:min(len(existing_rules), 20)]
        self.logger.debug(f'auto commit for {self.table.name} is {self.table.autocommit}')

        self.logger.debug("iptables: %s, pods: %s" % (len(self.chain.rules), len(ip_list)))

        existing_rules = set(
            map(
                lambda x: x.src.split('/')[0],
                filter(
                    lambda x: x.src != '0.0.0.0/0.0.0.0',
                    self.chain.rules
                )
            )
        )
        self.add_rule(ip_set - existing_rules)
        self.delete_rule(existing_rules - ip_set)

        self.logger.info(f'iptables: {len(self.chain.rules)}, pods: {len(ip_list)}')

        self.logger.debug(f'commit table {self.table.name}')
        self.table.commit()
        self.logger.debug(f'table {self.table.name} committed')

        self.logger.debug(f'enable autocommit for {self.table.name}')
        self.table.autocommit = True
        self.logger.debug(f'auto commit for {self.table.name} is {self.table.autocommit}')


class PodWatcher:
    client = None
    table = None
    token = ''
    access_log = None

    def __init__(self, labels, chain, url, logging_level, access_log: str):
        self.logger = logging.getLogger(__name__)
        self.api_url = url
        self.logging_level = logging_level
        self.access_log_name = access_log
        self.init_logger()
        self.logger.debug(f'class instance {self.__class__.__name__} created')
        self.labels = labels
        self.logger.debug(f'labels: {self.labels}')
        self.chain_name = chain
        self.logger.debug('start iptables init')
        self.ip_table = IpTable('filter', self.chain_name, self.logger, self.access_log)
        self.logger.debug('finish iptables init')
        self.token = os.environ['K8S_TOKEN']

    def init_logger(self):
        self.logger.setLevel(logging.getLevelName(self.logging_level))
        ch = logging.StreamHandler()
        ch.setLevel(logging.getLevelName(self.logging_level))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        if self.access_log_name != '':
            self.access_log = logging.getLogger('kubetables_log')
            self.access_log.addHandler(logging.FileHandler(self.access_log_name))
            self.access_log.setLevel(logging.DEBUG)

    def init_client(self):
        self.client = self.create_k8s_client(
            self.api_url,
            self.token,
            debug=self.logging_level == 'DEBUG')

    def get_pods(self, timeout: int = 3600):
        if self.client is None:
            self.init_client()
        return self.client.list_pod_for_all_namespaces(
            label_selector=f'service in ({",".join(self.labels)})',
            timeout_seconds=timeout)

    def loop(self):
        while True:
            self.init_client()
            try:
                result = self.get_pods()
                # update iptables chain
                list_pods = set()
                for pod in result.items:
                    self.logger.debug("POD: {} {} {} {}".format(
                        pod.metadata.name,
                        pod.metadata.labels['service'],
                        pod.status.pod_ip,
                        pod.status.phase
                    ))
                    if pod.status.phase == 'Running' and pod.status.pod_ip is not None:
                        list_pods.add(pod.status.pod_ip)
                self.logger.info("found %s ip addresses" % len(list_pods))
                self.ip_table.sync_list(list_pods)

                last_resource_version = result.metadata.resource_version
                self.watch_changes(last_resource_version)
            except ApiException as e:
                self.logger.critical(e)

    def watch_changes(self, last_resource_version: str, timeout: int = 3600):
        w = watch.Watch()
        result = True
        try:
            for event in w.stream(self.client.list_pod_for_all_namespaces, timeout_seconds=timeout,
                                  resource_version=last_resource_version,
                                  label_selector=f'service  in ({",".join(self.labels)})'):
                self.logger.debug("{}: {} {} {} {}".format(
                    event["type"],
                    event["object"].metadata.name,
                    event["object"].metadata.labels["service"],
                    event["object"].status.pod_ip,
                    event["object"].status.phase))

                if event['object'].status.pod_ip is not None:
                    if event['type'] == 'DELETED':
                        self.ip_table.delete_rule({event['object'].status.pod_ip})
                    else:
                        self.ip_table.add_rule({event['object'].status.pod_ip})
        except urllib3.exceptions.ProtocolError as e:
            self.logger.critical(e)
            result = False
        w.stop()
        del w
        return result

    @staticmethod
    def create_k8s_client(kube_api_address: str = "", kube_api_key: str = "", debug: bool = True):
        configuration = client.Configuration()
        configuration.debug = debug
        configuration.host = kube_api_address
        configuration.verify_ssl = False
        configuration.api_key['authorization'] = kube_api_key
        configuration.api_key_prefix['authorization'] = "Bearer"
        return client.CoreV1Api(client.ApiClient(configuration))


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

    parser.add_argument('labels', metavar='LABELS', type=str, nargs='+',
                        help='the labels to filter pods')
    parser.add_argument('--debug', metavar='DEBUG', type=str, nargs=1,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='debug level',
                        default='CRITICAL')
    parser.add_argument('--url', metavar='CLUSTER', type=str, nargs=1,
                        required=True, help='kubernetes api url')
    parser.add_argument('--chain', metavar='CHAIN', type=str, nargs=1,
                        required=True, help='iptables chain to add/remove hosts',
                        default='TEST')
    parser.add_argument('--json', metavar='JSON_LOG', type=str, nargs=1,
                        required=False, help='set json log location',
                        default=None)
    args = parser.parse_args()
    debug_level = args.debug[0] if isinstance(args.debug, list) else args.debug
    access_log = args.json[0] if isinstance(args.json, list) else args.json
    watcher = PodWatcher(args.labels, args.chain[0], args.url[0], debug_level.upper(), access_log)
    watcher.loop()


if __name__ == '__main__':
    main()

# TODO: detect if rules were flushed
# TODO: detect if chain was deleted
