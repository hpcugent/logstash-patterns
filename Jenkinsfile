#!/usr/bin/env groovy

def VECTOR_VERSION = "0.37.1"

node {
    stage('checkout git') {
        checkout scm
        // remove untracked files (*.pyc for example)
        sh 'git clean -fxd'
    }

    stage('install vector') {
        sh "wget -nv https://packages.timber.io/vector/${VECTOR_VERSION}/vector-${VECTOR_VERSION}-x86_64-unknown-linux-gnu.tar.gz"
        sh "tar -xzf vector-${VECTOR_VERSION}-x86_64-unknown-linux-gnu.tar.gz"
        env.PATH = "${pwd()}/vector-x86_64-unknown-linux-gnu/bin/:${env.PATH}"
    }

    stage('test') {
        sh 'python3.6 -V'
        sh 'pip3 install --ignore-installed --prefix $PWD/.vsc-tox tox'
        sh 'export PATH=$PWD/.vsc-tox/bin:$PATH && export PYTHONPATH=$PWD/.vsc-tox/lib/python$(python3 -c "import sys; print(\\"%s.%s\\" % sys.version_info[:2])")/site-packages:$PYTHONPATH && tox -v -c tox.ini'
        sh 'rm -r $PWD/.vsc-tox'
    }
}
