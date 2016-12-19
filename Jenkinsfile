#!/usr/bin/env groovy

def VIRTUALENV_VERSION = "15.0.3"
def LOGSTASH_VERSION = "5.1.1"

node {
    stage 'Checkout'
    checkout scm
    sh "git clean -fxd"

    stage 'Setup virtualenv'
    sh "wget -q -O virtualenv-${VIRTUALENV_VERSION}.tar.gz https://github.com/pypa/virtualenv/archive/${VIRTUALENV_VERSION}.tar.gz"
    sh "tar -xzf virtualenv-${VIRTUALENV_VERSION}.tar.gz"
    sh "python virtualenv-${VIRTUALENV_VERSION}/virtualenv.py venv"
    env.PATH = "${pwd()}/venv/bin:${env.PATH}"

    stage 'Build'
    sh "pip install vsc-base"
    sh "wget -q https://artifacts.elastic.co/downloads/logstash/logstash-${LOGSTASH_VERSION}.tar.gz"
    sh "tar -xzf logstash-${LOGSTASH_VERSION}.tar.gz"
    env.PATH = "${pwd()}/logstash-${LOGSTASH_VERSION}/bin:${env.PATH}"

    stage 'Test'
    sh "cd tests && python runtest.py"
}
