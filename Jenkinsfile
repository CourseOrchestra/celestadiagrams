node {
    if (!(env.BRANCH_NAME == 'master' || env.BRANCH_NAME.startsWith('PR'))){
        echo 'Not a PR or main branch. Skip build.'
        currentBuild.result = 'SUCCESS'
        return
    }
    
    stage ('Clone') {
        checkout scm
    }
    
    stage ('Build') {
        sh 'mkdir -p target'
        sh 'rm -r target/*'
        sh 'mkdir -p target/celestasql'
        sh 'mkdir -p target/filter'
        sh 'python celestasql.py'
        sh 'python filter.py'
    }
    
    stage('Publish') {
        archive 'target/celestasql/*.png'
        archive 'target/filter/*.png'
    }
}
