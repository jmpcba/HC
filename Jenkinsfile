def sitePackageDir = "env/lib/python3.6/site-packages"
def image = 'jmpcba/hc_infra_build:latest'

docker.image(image).inside {
    stage('Clone'){
        checkout scm
    }

    stage('environment setup'){
        sh """
        set -x
        python3 -m venv env
        . env/bin/activate
        python -m pip install -r requirements.txt
        """
    }
/*
    stage('validate code'){
        sh """
            set -x
            . env/bin/activate
            python -m pylint -E *.py
            """
    }
*/
    stage('Build package') {
        echo "#########################"
        echo "# BUILDING DEPENDENCIES #"
        echo "#########################"

        sh """
            set +x
            cp *.py ${sitePackageDir}
            """
        
        dir(sitePackageDir){
            sh "zip -qr9 hc_backend.zip ."
            sh "mv hc_backend.zip ${WORKSPACE}"
        }
    }

    stage('Deploy to AWS') {
        echo "####################"
        echo "# UPLOADING TO AWS #"
        echo "####################"  
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'AWS_JMPCBA', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
            sh """
            aws s3 cp hc_backend.zip s3://jmpcba-lambda/hc_backend.zip
            aws lambda update-function-code --function-name HC_backend_service --s3-bucket jmpcba-lambda --s3-key hc_backend.zip --region us-east-1
            """
        }
    }
}