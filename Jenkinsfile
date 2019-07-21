node {
    stage('Clone'){
        git credentialsId: 'GIT', url: 'https://github.com/jmpcba/HC.git'
    }

    stage('Build') { 
        echo "Building Dependencies"
        dir('src') {
            sh "virtualenv v-env"
            sh ". v-env/bin/activate"
            sh "pip install -r requirements.txt"
            dir('v-env/lib/python3.6/site-packages/'){
                sh "zip -r9 ../../../../function.zip ."
            }
            sh "zip -g function.zip *"
        }
        sh "deactivate"
    }
    stage('Deploy') {
        echo "Uploading to AWS" 
        dir('src') {
            sh "aws lambda update-function-code --function-name HC_data_service --zip-file fileb://function.zip"
        }
        
    }
}