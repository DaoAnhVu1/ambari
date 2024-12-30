#!/usr/bin/env python
import os
import pwd
import grp
import json
import io


from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute, Directory
from resource_management.core.resources.accounts import Group, User
from resource_management.libraries.functions import format


def setup_user():
  """
  Creates Hue user home directory and sets up the correct ownership.
  """
  __create_hue_user()
  __set_home_dir_ownership()

def __create_hue_user():
  import params
  try:
    grp.getgrnam(params.hue_group)
  except KeyError:
    Logger.info(format("Creating group '{params.hue_group}' for Hue Service"))
    Group(
      group_name = params.hue_group,
      ignore_failures = True
    )
  try:
    pwd.getpwnam(params.hue_user)
  except KeyError:
    Logger.info(format("Creating user '{params.hue_user}' for Hue Service"))
    User(
      username = params.hue_user,
      groups = [params.hue_group],
      ignore_failures = True
    )

def __set_home_dir_ownership():
  import params
  """
  Updates the Hue user home directory to be owned by hue:hue.
  """
  if not os.path.exists("/home/{0}".format(params.hue_user)):
    Directory(params.hue_local_home_dir,
            mode=0o700,
            cd_access='a',
            owner=params.hue_user,
            group=params.hue_group,
            create_parents=True
    )


def conf_hue():
  import params
  """
  Installing HUE
  """
  
  Logger.info("Starting yum install for hue")
  Execute('chown -R {0}:{1} {2}'.format(params.hue_user,params.hue_group,params.hue_dir))
  
  hue_symlink_path = "/usr/odp/current/hue-server"
  if os.path.islink(hue_symlink_path):
    os.remove(hue_symlink_path)
  elif os.path.isdir(hue_symlink_path):
    raise IsADirectoryError("{} is a directory. Can't create a symlink.".format(hue_symlink_path))
  elif os.path.isfile(hue_symlink_path):
    raise FileExistsError("{} is a file. Can't create a symlink.".format(hue_symlink_path))

  Execute('ln -s {0} {1}'.format(params.hue_dir, hue_symlink_path))
  Logger.info("Hue Service is installed")

def add_hdfs_configuration(if_ranger=False, security_enabled=False):
  import params
  services_configurations = {}
  services_configurations['core-site'] = {}
  services_configurations['core-site']['hadoop.proxyuser.hue.groups'] = '*'
  services_configurations['core-site']['hadoop.proxyuser.hue.hosts'] = '*'
  services_configurations['hdfs-site'] = {}
  services_configurations['hdfs-site']['dfs.namenode.acls.enabled'] = 'true'
  if params.hue_hbase_module_enabled == 'Yes':
    services_configurations['core-site']['hadoop.proxyuser.hbase.groups'] = '*'
    services_configurations['core-site']['hadoop.proxyuser.hbase.hosts'] = '*'
  if params.hue_hive_module_enabled == 'Yes':
    services_configurations['core-site']['hadoop.proxyuser.hive.groups'] = '*'
    services_configurations['core-site']['hadoop.proxyuser.hive.hosts'] = '*'
  if params.hue_spark_module_enabled == 'Yes':
    services_configurations['core-site']['hadoop.proxyuser.spark.groups'] = '*'
    services_configurations['core-site']['hadoop.proxyuser.spark.hosts'] = '*'
  if params.hue_oozie_module_enabled == 'Yes':
    services_configurations['core-site']['hadoop.proxyuser.oozie.groups'] = '*'
    services_configurations['core-site']['hadoop.proxyuser.oozie.hosts'] = '*'
  if params.dfs_ha_enabled:
    services_configurations['core-site']['hadoop.proxyuser.httpfs.groups'] = '*'
    services_configurations['core-site']['hadoop.proxyuser.httpfs.hosts'] = '*'
#     services_configurations['httpfs-site'] = {}
#     services_configurations['httpfs-site']['httpfs.proxyuser.hue.groups'] = '*'
#     services_configurations['httpfs-site']['httpfs.proxyuser.hue.hosts'] = '*'
  if security_enabled:
    services_configurations['core-site']['hadoop.proxyuser.HTTP.groups'] = '*'
    services_configurations['core-site']['hadoop.proxyuser.HTTP.hosts'] = '*'
    services_configurations['core-site']['hue.kerberos.principal.shortname'] = 'hue'
  add_configurations(services_configurations)

def add_hbase_configuration(if_ranger=False, security_enabled=False):
  import params
  services_configurations = {}
  services_configurations['hbase-site'] = {}
  if if_ranger:
    services_configurations['hbase-site']['hbase.regionserver.thrift.http'] = 'true'
    services_configurations['hbase-site']['hbase.thrift.support.proxyuser'] = 'true'
  if security_enabled:
    services_configurations['hbase-site']['hbase.thrift.security.qop'] = 'auth'
    services_configurations['hbase-site']['hbase.thrift.support.proxyuser'] = 'true'
    services_configurations['hbase-site']['hbase.regionserver.thrift.http'] = 'true'
    services_configurations['hbase-site']['hbase.thrift.kerberos.principal'] = params.HTTP_principal
    services_configurations['hbase-site']['hbase.thrift.keytab.file'] = params.HTTP_keytab
    services_configurations['hbase-site']['hbase.rpc.engine'] = 'org.apache.hadoop.hbase.ipc.SecureRpcEngine'
  add_configurations(services_configurations)

def add_hive_configuration(if_ranger=False, security_enabled=False):
  services_configurations = {}
  services_configurations['hive-site'] = {}
  services_configurations['hive-site']['hive.security.authorization.sqlstd.confwhitelist.append'] = 'hive.server2.logging.operation.verbose'
  services_configurations['hive-site'] = {}
  services_configurations['hive-site']['webhcat.proxyuser.hue.groups'] = '*'
  services_configurations['hive-site']['webhcat.proxyuser.hue.hosts'] = '*' 	
  if if_ranger:
    services_configurations['hive-site']['hive.server2.enable.impersonation'] = 'true'
  add_configurations(services_configurations)

def add_oozie_configuration(if_ranger=False, security_enabled=False):
  services_configurations = {}
  services_configurations['oozie-site'] = {}
  services_configurations['oozie-site']['oozie.service.ProxyUserService.proxyuser.hue.groups'] = '*'
  services_configurations['oozie-site']['oozie.service.ProxyUserService.proxyuser.hue.hosts'] = '*'
  add_configurations(services_configurations)

def add_spark_configuration(if_ranger=False, security_enabled=False):
  services_configurations = {}
  services_configurations['livy-conf'] = {}
  services_configurations['livy-conf']['livy.server.csrf_protection.enabled'] = 'false'
  add_configurations(services_configurations)

def add_configurations(services_configurations):
  """
  Run the script file to add configurations
  #/var/lib/ambari-server/resources/scripts/configs.sh set ambari-server-host \
   cluster_name core-site "hadoop.proxyuser.hbase.hosts" "*"

  services_configurations:{'configuration file1':{'key1':'value1','key2':'value2',...},
                           'configuration file2':{'key1':'value1','key2':'value2',...}
                           ...}
  """

  json_config_file_path = '/var/lib/ambari-agent/cache/cluster_cache/metadata.json'
  with io.open(json_config_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
  ambari_server_port = data['-1']['clusterLevelParams']['ambari_server_port']
  ambari_server_use_ssl = data['-1']['clusterLevelParams']['ambari_server_use_ssl']
  ssl = ""
  port = ""
  if ambari_server_use_ssl == "true" :
    ssl = "-s"
    port ="-port " + ambari_server_port


  import params

  if isinstance(services_configurations, dict):
    for i in range(len(services_configurations)):
      key1 = list(services_configurations.keys())[i]
      value1 = services_configurations[key1]
      if isinstance(value1, dict):
        for j in range(len(value1)):
          key2 = list(value1.keys())[j]
          value2 = value1[key2]
          cmd = format(params.service_packagedir + "/files/configs.sh " + port + " " + ssl + " set " + params.ambari_server_hostname + " " + params.cluster_name + " " + key1 + " '" + key2 + "' '"+ value2 + "'")
          Execute(cmd)

  
