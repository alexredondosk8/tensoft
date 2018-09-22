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
    stage('Paso 3: integración') {
      steps {
      // Checkout main branch
      git checkout master

      // Merge it with pull request (insert your pull id)
      git merge --no-ff pull/*/head:+env.BRANCH_NAME

      // TEST Local Merge Branch Compilation If Desired
      // msbuild ...

      // Push merged information back to git
      git push origin master
      }
    }
  }
}
