#!/usr/bin/env groovy


node {
    LOGSTASH_VERSION = '2.3.4'
    VIRTUALENV_VERSION = '15.0.3'

    stage 'Checkout'
    checkout scm

    stage 'Setup virtualenv'
    sh 'wget -O virtualenv-15.0.3.tar.gz https://github.com/pypa/virtualenv/archive/15.0.3.tar.gz'
    sh 'tar -xzf virtualenv-15.0.3.tar.gz'
    sh 'python virtualenv-15.0.3/virtualenv.py bootstrap'
    sh 'bootstrap/bin/pip install virtualenv-15.0.3.tar.gz'
    sh 'bootstrap/bin/virtualenv venv'
    sh 'source venv/bin/activate'

    stage 'Build'
    sh 'pip install vsc-base'
    sh 'wget https://download.elastic.co/logstash/logstash/logstash-2.3.4.tar.gz'
    sh 'tar -xzf logstash-2.3.4.tar.gz'
    env.PATH = "${pwd}/logstash-2.3.4/bin:${env.PATH}"

    stage 'Test'
    sh 'cd tests && python runtest.py -d'
}
