# cluster_status
Python/REST script to pull/dump subset of cluster status

Does a basic check of the current RF against desired RF. Difference might indicate something like a CVM down perhaps? Also very basic check of last Zookeeper and Cassandra startup.

If additional info needed, then uncomment the lines to print the json payload and add/change current output to print required info. Alternatively, dump and  review entire payload if preferred.

Thanks
ray
ray.m.hassan@gmail.com
