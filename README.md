# cluster_status
Python/REST script to pull/dump subset of cluster status

Does a basic check of the current RF (redundancy factor) against desired RF. Difference might indicate something like a CVM down perhaps? Also very basic check of Zookeeper and Cassandra ability to support the desired fault tolerance (FT).

Example:

$ ./cluster_status.py --i 10.68.64.55 -u admin -p nutanix/4u
Getting cluster information for cluster 10.68.64.55
===============================================================================
Status: 200
===============================================================================
Name: SAFC-FTM
ID: 00051776-7333-e1cd-0000-0000000052ea::21226
Cluster External IP Address: 10.68.64.55
Number of nodes: 4
Version: 4.6
Hypervisor Types: [u'kKvm']
Current redundancy factor (2) == Desired redundancy factor (2) : OK
Zookeeper FT status: OK
Cassandra FT status: OK
===============================================================================

If additional info needed, then uncomment the lines to print the json payload and add/change current output to print required info. Alternatively, dump and  review entire payload if preferred.

Thanks
ray
ray.m.hassan@gmail.com
