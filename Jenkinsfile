pipeline {
  agent any
  environment {
    REGION = 'us-east-2'      // your AWS region
    REPO   = 'voting-app'     // ECR repo name for THIS app
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Docker Build') {
      steps {
        sh 'docker build -t voting-app:latest .'
      }
    }

    stage('ECR Login') {
      steps {
        sh '''
          ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
          aws ecr get-login-password --region ${REGION} \
            | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
        '''
      }
    }

    stage('Tag & Push') {
      steps {
        sh '''
          ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
          IMAGE=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO}:latest

          # create ECR repo if missing
          aws ecr describe-repositories --repository-names ${REPO} --region ${REGION} \
            || aws ecr create-repository --repository-name ${REPO} --region ${REGION}

          docker tag voting-app:latest ${IMAGE}
          docker push ${IMAGE}
          echo "Pushed: ${IMAGE}"
        '''
      }
    }
  }

  post {
    success { echo '✅ voting-app image built & pushed to ECR.' }
    failure { echo '❌ Build failed — check logs.' }
  }
}
