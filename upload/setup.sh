#!/bin/bash
INSTALL_CMD=yum
${INSTALL_CMD} install -y sudo
test -x /usr/bin/sudo && export SUDO=/usr/bin/sudo
#${SUDO} ${INSTALL_CMD} upgrade -y
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
source ~/.nvm/nvm.sh
nvm install 11
set -x
java -version
yum whatprovides mvn
yum whatprovides yapf
${SUDO} wget https://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
${SUDO} sed -i s/\$releasever/7/g /etc/yum.repos.d/epel-apache-maven.repo
${SUDO} ${INSTALL_CMD} install -y git python36 python36-pip apache-maven
PIP_CMD="${SUDO} /usr/bin/pip-3.6"
${PIP_CMD} install yapf
${SUDO} ${INSTALL_CMD} install -y java-1.8.0-openjdk-devel
${SUDO} alternatives --set java /usr/lib/jvm/jre-1.8.0-openjdk.x86_64/bin/java
${SUDO} alternatives --set javac /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.242.b08-0.50.amzn1.x86_64/bin/javac
#${SUDO} ${INSTALL_CMD} remove -y java-1.7.0-openjdk
java -version
javac -version
mvn -version
git clone https://github.com/malariagen/sims-backbone.git
cd sims-backbone
./generate.sh
#${PIP_CMD} install --upgrade pip
${PIP_CMD} install -r python_client/requirements.txt
${PIP_CMD} install -r test/requirements.txt
${PIP_CMD} install -r server/backbone_server/REQUIREMENTS
${PIP_CMD} install -r upload/requirements.txt
${PIP_CMD} install git+https://github.com/idwright/chemistry-cmislib.git
cd upload
./import.sh $1
