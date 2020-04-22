#!/usr/bin/env groovy

def LOGSTASH_VERSION = "7.6.2"

node {
    stage('checkout git') {
        checkout scm
        sh "git clean -fxd"
    }

    stage('SEtup virtualenv') {
        sh 'pip3 install --ignore-installed virtualenv'
        sh 'virtualenv venv'
        env.PATH = "${pwd()}/venv/bin:${env.PATH}"
    }

    stage('build') {
        sh "pip install vsc-base"
        sh "wget -q https://download.elastic.co/logstash/logstash/logstash-${LOGSTASH_VERSION}.tar.gz"
        sh "tar -xzf logstash-${LOGSTASH_VERSION}.tar.gz"
        env.PATH = "${pwd()}/logstash-${LOGSTASH_VERSION}/bin:${env.PATH}"
    }

    stage('test') {
        sh "cd tests && python3 runtest.py"
    }
}
