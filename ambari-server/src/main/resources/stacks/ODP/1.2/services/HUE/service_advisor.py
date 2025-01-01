#!/usr/bin/env ambari-python-wrap
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import imp
import traceback
import os

from resource_management.libraries.script.script import Script
from resource_management.core.logger import Logger
from resource_management.libraries.functions.format import format

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STACKS_DIR = os.path.join(SCRIPT_DIR, "../../../../")
PARENT_FILE = os.path.join(STACKS_DIR, "service_advisor.py")

try:
    if "BASE_SERVICE_ADVISOR" in os.environ:
        PARENT_FILE = os.environ["BASE_SERVICE_ADVISOR"]
    with open(PARENT_FILE, "rb") as fp:
        service_advisor = imp.load_module(
            "service_advisor", fp, PARENT_FILE, (".py", "rb", imp.PY_SOURCE)
        )
except Exception as e:
    traceback.print_exc()
    print("Failed to load parent file:{0}".format(e))

Logger.initialize_logger()


class Hue030ServiceAdvisor(service_advisor.ServiceAdvisor):
    def __init__(self, *args, **kwargs):
        self.as_super = super(Hue030ServiceAdvisor)
        self.as_super.__init__(*args, **kwargs)
        self.cardinalitiesDict = {}
        self.mastersWithMultipleInstances = set()
        self.mastersWithMultipleInstances.add("HUE_SERVER")
        self.notPreferableOnServerComponents = set()
        # Always call these methods
        self.modifyMastersWithMultipleInstances()
        self.modifyCardinalitiesDict()
        self.modifyHeapSizeProperties()
        self.modifyNotValuableComponents()
        self.modifyComponentsNotPreferableOnServer()
        self.modifyComponentLayoutSchemes()
        self.allRequestedProperties = {}


    def modifyMastersWithMultipleInstances(self):
        """
        Modify the set of masters with multiple instances.
        Must be overriden in child class.
        """
        # Nothing to do
        pass

    def modifyCardinalitiesDict(self):
        """
        Modify the dictionary of cardinalities.
        Must be overriden in child class.
        """
        self.cardinalitiesDict.update(
            {
                "HUE_SERVER": {"min":1},
            }
        )
        pass

    def modifyHeapSizeProperties(self):
        """
        Modify the dictionary of heap size properties.
        Must be overriden in child class.
        """
        pass

    def modifyNotValuableComponents(self):
        """
        Modify the set of components whose host assignment is based on other services.
        Must be overriden in child class.
        """
        # Nothing to do
        pass

    def modifyComponentsNotPreferableOnServer(self):
        """
        Modify the set of components that are not preferable on the server.
        Must be overriden in child class.
        """
        # Nothing to do
        pass

    def modifyComponentLayoutSchemes(self):
        """
        Modify layout scheme dictionaries for components.
        The scheme dictionary basically maps the number of hosts to
        host index where component should exist.
        Must be overriden in child class.
        """
        self.componentLayoutSchemes = {}
        pass


    def getServiceComponentLayoutValidations(self, services, hosts):
        """
        Get a list of errors.
        Must be overriden in child class.
        """

        return self.getServiceComponentCardinalityValidations(services, hosts, "HUE")


    @staticmethod
    def isKerberosEnabled(services, configurations):
         """
         Determines if security is enabled by testing the value of hue-desktop-site/kerberos_hue_principal enabled.
         If the property exists and is equal to "true", then is it enabled; otherwise is it assumed to be
         disabled.

         :type services: dict
         :param serevices: the dictionary containing the existing configuration values
         :type configurations: dict
         :param configurations: the dictionary containing the updated configuration values
         :rtype: bool
         :return: True or False
         """
         if configurations and "hue-ini" in configurations and \
            "kerberos_hue_principal" in configurations["hue-desktop-site"]["properties"]:
             return True
         elif services and "hue-desktop-site" in services["configurations"] and \
            "kerberos_hue_principal" in services["configurations"]["hue-desktop-site"]["properties"]:
             return True
         else:
             return False

    
    def getServiceConfigurationRecommendations(self, configurations, clusterData, services, hosts):

        putHiveSiteProperty = self.putProperty(configurations, "hive-site", services)
        
        putHDFSCoreProperty = self.putProperty(configurations, "core-site", services)
        putHDFSProperty = self.putProperty(configurations, "hdfs-site", services)

        putHbaseProperty = self.putProperty(configurations, "hbase-site", services)

        putLivyProperty = self.putProperty(configurations, "livy-conf", services)
        Logger.info("Running the getServiceConfigurationMethod for Hue")
        #cluster_env = self.getServicesSiteProperty(services, "cluster-env")
        #security_enabled = cluster_env is not None and "security_enabled" in cluster_env
        #    cluster_env["security_enabled"].lower() == "true"

        
        
        security_enabled = self.isKerberosEnabled(services,configurations)
        putHiveSiteProperty("webhcat.proxyuser.hue.groups", "*")
        putHiveSiteProperty("webhcat.proxyuser.hue.hosts", "*")
        if "hive-site" in services["configurations"]:
            Logger.info("Hive-site in services[configurations]")

            putHiveSiteProperty("hive.security.authorization.sqlstd.confwhitelist.append", "hive.server2.logging.operation.verbose")
            putHiveSiteProperty("webhcat.proxyuser.hue.groups", "*")
            putHiveSiteProperty("webhcat.proxyuser.hue.hosts", "*")
            
        
            Logger.info(format("Recommending hive options..."))

        if "hdfs-site" in services["configurations"]:
            putHDFSProperty("dfs.namenode.acls.enabled", "true")
            putHDFSCoreProperty("hadoop.proxyuser.hue.groups", "*")
            putHDFSCoreProperty("hadoop.proxyuser.hue.hosts", "*")

            if "hive-site" in services["configurations"]:
                putHDFSCoreProperty("hadoop.proxyuser.hive.groups", "*")
                putHDFSCoreProperty("hadoop.proxyuser.hive.hosts", "*")
            """
            if dfs_ha_enabled:
                putHDFSCoreProperty("hadoop.proxyuser.httpfs.groups", "*")
                putHDFSCoreProperty("hadoop.proxyuser.httpfs.hosts", "*")
            """    
            if security_enabled:
                putHDFSCoreProperty("hadoop.proxyuser.HTTP.groups", "*")
                putHDFSCoreProperty("hadoop.proxyuser.HTTP.hosts", "*")
                putHDFSCoreProperty("hue.kerberos.principal.shortname", "hue")
        
        if "spark3-env" in services["configurations"]:
            putHDFSCoreProperty("hadoop.proxyuser.spark.groups", "*")
            putHDFSCoreProperty("hadoop.proxyuser.spark.hosts", "*")

        if "livy-conf" in services["configurations"]:
            putLivyProperty("livy.server.csrf_protection.enabled", "false")


        if "hbase-env" in services["configurations"]:
            if security_enabled:
                putHbaseProperty("hbase.thrift.security.qop", "auth")
                putHbaseProperty("hbase.thrift.support.proxyuser", "true")
                putHbaseProperty("hbase.regionserver.thrift.http", "true")
 
                putHbaseProperty("hbase.rpc.engine", "org.apache.hadoop.hbase.ipc.SecureRpcEngine")

        if "ranger-env" in services["configurations"]:
            putHbaseProperty("hbase.regionserver.thrift.http", "true")
            putHbaseProperty("hbase.thrift.support.proxyuser", "true")
            putHiveSiteProperty("hive.server2.enable.impersonation", "true")
        
        Logger.info(format("In getServiceConfigurationRecommendations"))
