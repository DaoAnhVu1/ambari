# Raw copy
mkdir -p target/rpms
cp ambari-agent/target/rpm/ambari-agent/RPMS/x86_64/ambari-agent-2.7.9.0-0.x86_64.rpm target/rpms
cp ambari-infra/target/rpm/ambari-infra/RPMS/noarch/ambari-infra-2.7.9.0-0.noarch.rpm target/rpms
cp ambari-infra/ambari-infra-assembly/target/rpm/ambari-infra-assembly/RPMS/noarch/ambari-infra-assembly-2.7.9.0-0.noarch.rpm target/rpms
cp ambari-logsearch/ambari-logsearch-logfeeder/target/rpm/ambari-logsearch-logfeeder/RPMS/noarch/ambari-logsearch-logfeeder-2.7.9.0-0.noarch.rpm target/rpms
cp ambari-logsearch/ambari-logsearch-assembly/target/rpm/ambari-logsearch-portal/RPMS/noarch/ambari-logsearch-portal-2.7.9.0-0.noarch.rpm target/rpms
cp ambari-infra/ambari-infra-manager/target/rpm/ambari-infra-manager/RPMS/noarch/ambari-infra-manager-2.7.9.0-0.noarch.rpm target/rpms
cp ambari-infra/ambari-infra-solr-client/target/rpm/ambari-infra-solr-client/RPMS/noarch/ambari-infra-solr-client-2.7.9.0-0.noarch.rpm target/rpms
cp ambari-infra/ambari-infra-assembly/target/rpm/ambari-infra-solr/RPMS/noarch/ambari-infra-solr-2.7.9.0-0.noarch.rpm target/rpms
cp ambari-server/target/rpm/ambari-server/RPMS/x86_64/ambari-server-2.7.9.0-0.x86_64.rpm target/rpms
cp ambari-views/target/rpm/ambari-views/RPMS/noarch/ambari-views-2.7.9.0-0.noarch.rpm target/rpms
cp contrib/views/files/target/rpm/files/RPMS/noarch/files-1.0.0.0-SNAPSHOT.noarch.rpm target/rpms
cp contrib/views/capacity-scheduler/target/rpm/capacity-scheduler/RPMS/noarch/capacity-scheduler-1.0.0.0-SNAPSHOT.noarch.rpm target/rpms
cp ambari-metrics/ambari-metrics-*/target/rpm/ambari-metrics-*/RPMS/noarch/*.rpm target/rpms
cp ambari-infra/ambari-infra-solr-plugin/target/rpm/ambari-infra-solr-plugin/RPMS/noarch/ambari-infra-solr-plugin-2.7.9.0-0.noarch.rpm target/rpms

createrepo target/rpms

# Fake copy
rm -rf target/rpms
mkdir -p target/rpms
cp ambari-agent/target/rpm/ambari-agent/RPMS/x86_64/ambari-agent-2.7.9.0-0.x86_64.rpm target/rpms
cp ambari-server/target/rpm/ambari-server/RPMS/x86_64/ambari-server-2.7.9.0-0.x86_64.rpm target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-infra-2.7.9.0-110.noarch.rpm target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-infra-assembly-2.7.9.0-110.noarch.rpm target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-infra-manager-2.7.9.0-110.noarch.rpm target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-infra-solr-2.7.9.0-110.noarch.rpm target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-infra-solr-client-2.7.9.0-110.noarch.rpm target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-infra-solr-plugin-2.7.9.0-110.noarch.rpm target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-logsearch-logfeeder-2.7.9.0-110.noarch.rpm  target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-logsearch-portal-2.7.9.0-110.noarch.rpm  target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-metrics-collector-2.7.9.0.0-110.x86_64.rpm  target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-metrics-grafana-2.7.9.0.0-110.x86_64.rpm  target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-metrics-hadoop-sink-2.7.9.0.0-110.x86_64.rpm  target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-metrics-monitor-2.7.9.0.0-110.x86_64.rpm  target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/ambari-views-2.7.9.0-110.noarch.rpm  target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/capacity-scheduler-1.0.0.0-110.noarch.rpm  target/rpms
cp /home/app1/Downloads/odp/var/www/html/ambari-release/dist/centos9/1.x/BUILDS/2.7.9.0.0-110/rpms/files-1.0.0.0-110.noarch.rpm  target/rpms

createrepo target/rpms


# Copy 2
rm target/rpms/ambari-agent-2.7.9.0-0.x86_64.rpm
rm target/rpms/ambari-server-2.7.9.0-0.x86_64.rpm
cp ambari-agent/target/rpm/ambari-agent/RPMS/x86_64/ambari-agent-2.7.9.0-0.x86_64.rpm target/rpms
cp ambari-server/target/rpm/ambari-server/RPMS/x86_64/ambari-server-2.7.9.0-0.x86_64.rpm target/rpms

createrepo target/rpms