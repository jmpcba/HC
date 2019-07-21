node {
    stage('Clone'){
        git credentialsId: 'GIT', url: 'https://github.com/jmpcba/HC.git'
    }

    stage('Build') { 
        echo "Building Dependencies"
        dir('src') {
            sh "python3 -m pip install -r requirements.txt --target ./lib"
            sh "zip -r9 function.zip"
        }
    }
    stage('Deploy') {
        echo "Uploading to AWS" 
        dir('src') {
            sh "aws lambda update-function-code --function-name HC_data_service --zip-file fileb://function.zip"
        }
        
    }
}