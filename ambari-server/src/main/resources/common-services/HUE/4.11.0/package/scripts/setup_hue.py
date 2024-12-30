#!/usr/bin/env python
# encoding=utf8
import sys

if sys.version_info[0] == 2:
  reload(sys)
  sys.setdefaultencoding('utf-8')

  

from resource_management.libraries.functions import format
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.core.source import Template, InlineTemplate
from resource_management.core.logger import Logger

#from common import add_hdfs_configuration, add_hbase_configuration, add_hive_configuration,\
#  add_oozie_configuration, add_spark_configuration
  

def setup_hue():
  import params
  # import status_params
  Logger.info("Configure Hue Service")
  # create the pid and log dir
  Directory([params.hue_log_dir, params.hue_pid_dir],
        mode=0o755,
        cd_access='a',
        owner=params.hue_user,
        group=params.hue_group,
        create_parents=True
  )
  File([params.hue_log_file, params.hue_server_pid_file],
    mode=0o644,
    owner=params.hue_user,
    group=params.hue_group,
    content=''
  )
    
  # these plugin files do not exist in 4.x  
  #Logger.info(format("Creating symlinks /usr/odp/current/hadoop-client/lib/hue-plugins-{params.hue_version}-SNAPSHOT.jar"))
  #Link("{0}/desktop/libs/hadoop/java-lib/*".format(params.hue_dir),to = "/usr/odp/current/hadoop-client/lib")
  Execute('find {0} -iname "*.sh" | xargs chmod +x'.format(params.service_packagedir))
  # Create a home directory for solr user on HDFS
  params.HdfsResource(params.hue_hdfs_home_dir,
                type="directory",
                action="create_on_execute",
                owner=params.hue_user,
                mode=0o755,
                recursive_chmod=True
  )
  Logger.info(format("Creating {hue_conf_dir}/log.conf file"))
  File(format("{hue_conf_dir}/log.conf"), 
    content = InlineTemplate(params.hue_log_content), 
    owner = params.hue_user
  )
  Logger.info(format("Creating {hue_conf_dir}/hue.ini config file"))
  File(format("{hue_conf_dir}/hue.ini"), 
    content = InlineTemplate(params.hue_ini_content), 
    owner = params.hue_user,
    mode = 0o600
  )
  File(format("{hue_conf_dir}/hue_metastore.ini"),
       content = Template("metastore.j2"),
       owner = params.hue_user,
       mode = 0o600
  )
  if params.rdbms_mysql_engine or\
     params.rdbms_postgresql_engine or\
     params.rdbms_sqlite_engine or \
     params.rdbms_oracle_engine:
    File(format("{hue_conf_dir}/hue_databases.ini"),
         content = Template("databases.j2"),
         owner = params.hue_user,
         mode = 0o600
    )
  else:
    import os
    if os.path.exists(format("{hue_conf_dir}/hue_databases.ini")):
      os.remove(format("{hue_conf_dir}/hue_databases.ini"))
    else:
      Logger.info("Not removing hue_databases.ini since it doesn't exist!")
  #Logger.info(format("Run the script file to add configurations"))
  """
  if params.hue_hdfs_module_enabled == 'Yes':
    add_hdfs_configuration(params.has_ranger_admin, params.security_enabled)
  if params.hue_hbase_module_enabled == 'Yes':
    add_hbase_configuration(params.has_ranger_admin, params.security_enabled)
  if params.hue_hive_module_enabled == 'Yes':
    add_hive_configuration(params.has_ranger_admin, params.security_enabled)
  if params.hue_oozie_module_enabled == 'Yes':
    add_oozie_configuration(params.has_ranger_admin, params.security_enabled)
  if params.hue_spark_module_enabled == 'Yes':
    add_spark_configuration(params.has_ranger_admin, params.security_enabled)
  """
