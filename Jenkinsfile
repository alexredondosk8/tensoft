pipeline {
  agent any
  stages {
    stage('Paso 1: inicio') {
      steps {
        echo 'Entrando a pipeline'
      }
    }
    stage('Paso 2: rama de ejecución') {
      steps {
        echo 'Rama ' + env.BRANCH_NAME
      }
    }
    stage ("Paso 3: credenciales") {
      steps {
        echo "entrando a hacer el pull request y merge"
        withCredentials([usernameColonPassword(credentialsId: '954ecaac-dc69-4712-9835-857c65b79f80', variable: 'key_jenkinsfile')]) {
          bat 'git checkout master'
          bat 'git pull . ' + "${env.BRANCH_NAME}"
        }
      }
    }
  }
}
