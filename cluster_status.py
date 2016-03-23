#! /usr/bin/env python

import argparse
import json
import requests
import sys
import traceback
import pprint

def configure_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-u', '--user', required=True, 
                    help='NCLI admin user (default admin)')
    arg_parser.add_argument('-p', '--password', required=True,
                    help='NCLI admin password (default nutanix/4u)')
    arg_parser.add_argument('-i', '--ip', required=True,
                    help='Cluster or CVM host/IP address')
    return arg_parser

class RestApi():
    def __init__(self, ip_addr, user, passwd):
        #self.serverIpAddress = "10.68.64.55"
        self.serverIpAddress = ip_addr
        #self.username = "admin"
        self.username = user
        #self.password = "nutanix/4u"
        self.password = passwd
        BASE_URL = 'https://%s:9440/PrismGateway/services/rest/v1'
        self.base_url = BASE_URL % self.serverIpAddress
        self.session = self.get_server_session(self.username, self.password)

    def get_server_session(self, username, password):
        session = requests.Session()
        session.auth = (username, password)
        session.verify = False
        session.headers.update(
            {'Content-Type': 'application/json; charset=utf-8'})
        return session

    def getClusterInformation(self):
        clusterURL = self.base_url + "/cluster"
        print "Getting cluster information for cluster %s" % self.serverIpAddress
        serverResponse = self.session.get(clusterURL)
        return serverResponse.status_code, json.loads(serverResponse.text)


if __name__ == "__main__":
    try:

        parser = configure_parser()
        args = parser.parse_args()
        print args

        ipaddr = args.ip
        user = args.user
        password = args.password

        client = RestApi(ipaddr, user, password)
        status, cluster = client.getClusterInformation()

        pp = pprint.PrettyPrinter(indent=2)
        print ("=" * 79)
        print "Status: %s" % status
        #print "Text:"
        #pp.pprint(cluster)
        print ("=" * 79) 
        print "Name: %s" % cluster.get('name')
        print "ID: %s" % cluster.get('id')
        print "Cluster External IP Address: %s" % cluster.get('clusterExternalIPAddress')
        print "Number of nodes: %s" % cluster.get('numNodes')
        print "Version: %s" % cluster.get('version')
        print "Hypervisor Types: %s" % cluster.get('hypervisorTypes')
        #print "Cluster current redundancy factor: %s" % cluster.get('clusterRedundancyState')
        current_RF = cluster["clusterRedundancyState"]["currentRedundancyFactor"]
        desired_RF = cluster["clusterRedundancyState"]["desiredRedundancyFactor"]
        if current_RF == desired_RF:
            print "Current redundancy factor (%s) == Desired redundancy factor (%s) : OK" % (current_RF, desired_RF)
        else: 
            print "Current redundancy factor (%s) != Desired redundancy factor (%s) : Not OK!" % (current_RF, desired_RF)

        zk_status = cluster["clusterRedundancyState"]["redundancyStatus"]["kZookeeperPrepareDone"] 
        if zk_status == True:
            print "Zookeeper status: OK"
        else: print "Zookeeper status not OK"
 
        cassandra_stat = cluster["clusterRedundancyState"]["redundancyStatus"]["kCassandraPrepareDone"]
        if cassandra_stat == True:
            print "Cassandra status: OK"
        else: print "Cassandra status not OK"

        print ("=" * 79) 

    except Exception as ex:
        print ex
        sys.exit(1)

