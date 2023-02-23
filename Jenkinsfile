#!/usr/bin/env groovy

def LOGSTASH_VERSION = "7.10.2"

node {
    stage('checkout git') {
        checkout scm
        // remove untracked files (*.pyc for example)
        sh 'git clean -fxd'
    }

    stage('install logstash') {
        sh "wget -nv https://artifacts.elastic.co/downloads/logstash/logstash-${LOGSTASH_VERSION}-linux-x86_64.tar.gz"
        sh "tar -xzf logstash-${LOGSTASH_VERSION}-linux-x86_64.tar.gz"
        env.PATH = "${pwd()}/logstash-${LOGSTASH_VERSION}/bin:${env.PATH}"
    }

    stage('test') {
        sh 'pip3 install --ignore-installed --prefix $PWD/.vsc-tox tox'
        sh 'export PATH=$PWD/.vsc-tox/bin:$PATH && export PYTHONPATH=$PWD/.vsc-tox/lib/python$(python3 -c "import sys; print(\\"%s.%s\\" % sys.version_info[:2])")/site-packages:$PYTHONPATH && tox -v -c tox.ini'
        sh 'rm -r $PWD/.vsc-tox'
    }
}
