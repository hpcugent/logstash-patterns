#!/usr/bin/env groovy


node {
    stage 'Checkout'
    checkout scm

    stage 'Setup virtualenv'
    def LOGSTASH_VERSION = "2.3.4"
    def VIRTUALENV_VERSION = "15.0.3"
    echo "Using ${VIRTUALENV_VERSION}"
    sh "wget -O virtualenv-${VIRTUALENV_VERSION}.tar.gz https://github.com/pypa/virtualenv/archive/${VIRTUALENV_VERSION}.tar.gz"
    sh "tar -xzf virtualenv-${VIRTUALENV_VERSION}.tar.gz"
    sh "python virtualenv-${VIRTUALENV_VERSION}/virtualenv.py venv"
    env.PATH = "${pwd()}/venv/bin:${env.PATH}"

    stage 'Build'
    sh "pip install vsc-base"
    sh "wget -q https://download.elastic.co/logstash/logstash/logstash-${LOGSTASH_VERSION}.tar.gz"
    sh "tar -xzf logstash-${LOGSTASH_VERSION}.tar.gz"
    env.PATH = "${pwd()}/logstash-${LOGSTASH_VERSION}/bin:${env.PATH}"

    stage 'Test'
    sh "cd tests && python runtest.py"
    junit '**/test-reports/*.xml'
}
