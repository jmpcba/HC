node {
    stage('Clone'){
        git credentialsId: 'GIT', url: 'https://github.com/jmpcba/HC.git'
    }

    stage('Build') { 
        steps {
            echo "Building Dependencies"
            dir('src') {
                sh "pip3 install -r requirements.txt --target ./lib"
                sh "zip -r9 function.zip"
            }
        }
    }
    stage('Deploy') { 
        steps {
            dir('src') {
                echo "Uploading to AWS"
                sh "aws lambda update-function-code --function-name HC_data_service --zip-file fileb://function.zip"
            }
        }
    }
}