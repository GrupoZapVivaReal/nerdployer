#!/bin/sh

# wait for apt locks
sleep 60

## set limits
echo '* soft nofile 65000' >> /etc/security/limits.conf
echo '* hard nofile 65000' >> /etc/security/limits.conf

## updates everthing
apt-get update; apt-get dist-upgrade -y;

## aws kernel
apt-get install linux-aws -y

## cfn and aws support
apt-get -y install python-setuptools python-pystache python-pip libffi-dev libssl-dev
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
pip install pyopenssl ndg-httpsclient pyasn1 boto pystache
pip install awscli
easy_install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz

## docker support
apt-get install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update; apt-get install docker-ce -y
docker login -u $DOCKER_USER -p $DOCKER_PASSWORD
groupadd docker ; usermod -aG docker ubuntu

## clear and reboot
apt-get autoremove
shred -u /etc/ssh/*_key /etc/ssh/*_key.pub
shred -u ~/.*history
reboot