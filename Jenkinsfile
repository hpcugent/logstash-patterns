#!/usr/bin/env groovy

def LOGSTASH_VERSION = '2.3.4'

node {
    stage 'Checkout'
    checkout scm

    stage 'Build'
    sh 'virtualenv venv'
    sh 'source venv/bin/activate'
    sh 'pip install vsc-base'
    sh 'wget https://download.elastic.co/logstash/logstash/logstash-${LOGSTASH_VERSION}.tar.gz'
    sh 'tar -xzf logstash-${LOGSTASH_VERSION}.tar.gz'
    env.PATH = "${pwd}/logstash-${LOGSTASH_VERSION}/bin:${env.PATH}"

    stage 'Test'
    sh 'cd tests && python runtest.py -d'
}
