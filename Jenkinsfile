#!/usr/bin/env groovy


node {
    stage 'Checkout'
    checkout scm

    stage 'Setup virtualenv'
    LOGSTASH_VERSION = '2.3.4'
    VIRTUALENV_VERSION = '15.0.3'
    echo 'Using ${VIRTUALENV_VERSION}'
    sh 'wget -O virtualenv-15.0.3.tar.gz https://github.com/pypa/virtualenv/archive/${VIRTUALENV_VERSION}.tar.gz'
    sh 'tar -xzf virtualenv-15.0.3.tar.gz'
    sh 'python virtualenv-15.0.3/virtualenv.py venv'
    env.PATH = "${pwd()}/venv/bin:${env.PATH}"

    stage 'Build'
    sh 'pip install vsc-base'
    sh 'wget -q https://download.elastic.co/logstash/logstash/logstash-2.3.4.tar.gz'
    sh 'tar -xzf logstash-2.3.4.tar.gz'
    env.PATH = "${pwd()}/logstash-2.3.4/bin:${env.PATH}"

    stage 'Test'
    sh 'cd tests && python runtest.py'
    junit '**/test-reports/*.xml'
}
