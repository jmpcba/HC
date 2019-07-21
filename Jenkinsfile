node {
    stage('Clone'){
        git credentialsId: 'GIT', url: 'https://github.com/jmpcba/HC.git'
    }

    stage('Build') { 
        echo "#########################"
        echo "# BUILDING DEPENDENCIES #"
        echo "#########################"
        dir('src') {
            sh "virtualenv v-env"
            sh ". v-env/bin/activate"
            sh "pip install -r requirements.txt"
            dir('v-env/lib/python3.6/site-packages/'){
                sh "zip -r9 ../../../function.zip ."
            }
            sh "zip -g function.zip *"
        }
    }
    stage('Deploy') {
        echo "####################"
        echo "# UPLOADING TO AWS #"
        echo "####################"
        dir('src') {
            sh "aws lambda update-function-code --function-name HC_data_service --zip-file fileb://function.zip"
        }
    }
}