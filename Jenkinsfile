#!/usr/bin/env groovy

def LOGSTASH_VERSION = '2.3.4'
def VIRTUALENV_VERSION = '15.0.3'

node {
    stage 'Checkout'
    checkout scm

    stage 'Setup virtualenv'
    sh 'wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-${VIRTUALENV_VERSION}.tar.gz'
    sh 'tar -xzf virtualenv-${VIRTUALENV_VERSION}.tar.gz'
    sh 'python virtualenv-${VIRTUALENV_VERSION}/virtualenv.py bootstrap'
    sh 'virtualenv-${VIRTUALENV_VERSION}/bin/pip install virtualenv-${VIRTUALENV_VERSION}.tar.gz
    sh 'virtualenv-${VIRTUALENV_VERSION}/bin/virtualenv venv'
    sh 'source venv/bin/activate'

    stage 'Build'
    sh 'pip install vsc-base'
    sh 'wget https://download.elastic.co/logstash/logstash/logstash-${LOGSTASH_VERSION}.tar.gz'
    sh 'tar -xzf logstash-${LOGSTASH_VERSION}.tar.gz'
    env.PATH = "${pwd}/logstash-${LOGSTASH_VERSION}/bin:${env.PATH}"

    stage 'Test'
    sh 'cd tests && python runtest.py -d'
}
