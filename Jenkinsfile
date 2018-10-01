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
    stage ("Paso 3: Rama de desarrollador") {
      // si no es la rama master entonces ejecuta la integración continua
      when { not { branch 'master' } }
      steps {
        echo "entrando a hacer el pull request y merge"
        withCredentials([usernameColonPassword(credentialsId: '954ecaac-dc69-4712-9835-857c65b79f80', variable: 'key_jenkinsfile')]) {
          bat 'git checkout master'
          bat 'git pull . origin/' + "${env.BRANCH_NAME}"
          bat 'git merge ' + "${env.BRANCH_NAME}"
          // bat 'git push'
        }
      }
    }
    stage ("Paso 3: Rama master") {
      // si es la rama master no se hace integración
      when { branch 'master'}
      steps {
        echo 'Sólo se ejecuta en ramas de desarroladores'
      }
    }
  }
}
