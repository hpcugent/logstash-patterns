#!/usr/bin/env groovy

def VIRTUALENV_VERSION = "20.0.18"
def LOGSTASH_VERSION = "7.6.2"

node {
    stage('Checkout') {
        checkout scm
        sh "git clean -fxd"
    }

    stage('Setup virtualenv') {
        pip3 install virtualenv
        virtualenv venv
        env.PATH = "${pwd()}/venv/bin:${env.PATH}"
    }

    stage('Build') {
        sh "pip install vsc-base"
        sh "wget -q https://download.elastic.co/logstash/logstash/logstash-${LOGSTASH_VERSION}.tar.gz"
        sh "tar -xzf logstash-${LOGSTASH_VERSION}.tar.gz"
        env.PATH = "${pwd()}/logstash-${LOGSTASH_VERSION}/bin:${env.PATH}"
    }

    stage('Test') {
        sh "cd tests && python3 runtest.py"
    }
}
