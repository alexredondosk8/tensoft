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
    stage ("Paso 3: Merge pull request") {
      steps {
        echo "entrando a hacer el pull request y merge"
        withCredentials([usernamePassword(credentialsId: 'anderojas1', usernameVariable: 'ACCESS_TOKEN_USERNAME', passwordVariable: 'ACCESS_TOKEN_PASSWORD',)]) {
            echo "curl -X PUT -d '{\"commit_title\": \"Merge pull request\"}'  https://github.ibm.com/api/v3/repos/org-name/repo-name/pulls/$CHANGE_ID/merge?access_token=$ACCESS_TOKEN_PASSWORD"
      }
    }
  }
}
