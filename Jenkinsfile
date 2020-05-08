#!/usr/bin/env groovy

def LOGSTASH_VERSION = "7.6.2"

node {
    stage('checkout git') {
        checkout scm
        // remove untracked files (*.pyc for example)
        sh 'git clean -fxd'
    }

    stage('install logstash') {
        sh "wget -nv https://artifacts.elastic.co/downloads/logstash/logstash-${LOGSTASH_VERSION}.tar.gz"
        sh "tar -xzf logstash-${LOGSTASH_VERSION}.tar.gz"
        env.PATH = "${pwd()}/logstash-${LOGSTASH_VERSION}/bin:${env.PATH}"
    }

    stage('test') {
        sh 'python2.7 -V'
        sh 'pip3 install --ignore-installed --user tox'
        sh 'export PATH=$HOME/.local/bin:$PATH && tox -v -c tox.ini'
    }
}
