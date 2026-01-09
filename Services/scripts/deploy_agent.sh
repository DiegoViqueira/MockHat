#!/bin/bash
set -e

# Configuración
PROJECT_NAME="mockhat-ai-agent"
AWS_REGION="eu-west-1"  # Cambia a tu región
STACK_NAME="mockhat-ai-agent"
SQS_QUEUE_NAME="mockhat-assessments-writings"
IMAGE_NAME="905418182087.dkr.ecr.eu-west-1.amazonaws.com/${PROJECT_NAME}"


tags=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep "^${IMAGE_NAME}:" | awk -F: '{print $2}')

# Filter tags to match semantic versioning format (e.g., 1.2.3) and sort them
latest_tag=$(echo "$tags" | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -n 1)

if [ -z "$latest_tag" ]; then
    echo "No se encontraron tags de imagen válidas para ${IMAGE_NAME}"
    new_tag="1.0.0"
else
    IFS='.' read -r major minor patch <<< "$latest_tag"
    new_tag="${major}.${minor}.$((patch + 1))"
fi


# Obtener el ID de la cuenta de AWS
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "Construyendo la imagen Docker..."
docker build -t ${IMAGE_NAME}:${new_tag} -f ./docker/Dockerfile.agent .

# Iniciar sesión en ECR
echo "Iniciando sesión en ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

docker push $IMAGE_NAME:$new_tag

# Verificar el estado del stack
STACK_STATUS=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query "Stacks[0].StackStatus" --output text 2>/dev/null || echo "DOES_NOT_EXIST")

echo "Estado actual del stack: ${STACK_STATUS}"

# Obtener el ARN de la cola SQS existente
SQS_QUEUE_ARN=$(aws sqs get-queue-attributes --queue-url "https://sqs.eu-west-1.amazonaws.com/905418182087/mockhat-assessments-writings.fifo" --attribute-names QueueArn --query "Attributes.QueueArn" --output text)

echo "ARN de la cola SQS: ${SQS_QUEUE_ARN}"

if [ "${STACK_STATUS}" == "ROLLBACK_COMPLETE" ]; then
    echo "El stack ${STACK_NAME} está en estado ROLLBACK_COMPLETE. Eliminando stack..."
    aws cloudformation delete-stack --stack-name ${STACK_NAME}
    echo "Esperando a que el stack se elimine completamente..."
    aws cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}
    STACK_STATUS="DOES_NOT_EXIST"
fi

if [ "${STACK_STATUS}" == "DOES_NOT_EXIST" ]; then
    echo "Creando nuevo stack ${STACK_NAME}..."
    aws cloudformation deploy \
      --template-file ./config/cloudformation-agent.yaml \
      --stack-name ${STACK_NAME} \
      --parameter-overrides \
        VpcId=vpc-0a8741ac883394d5b \
        SubnetIds="subnet-05a8843fe15747b16,subnet-0c96a572e69454cbd" \
        SQSQueueName="mockhat-assessments-writings.fifo" \
        SQSQueueARN="${SQS_QUEUE_ARN}" \
        ImageTag="${new_tag}" \
        ProjectName="${PROJECT_NAME}"\
      --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
else
    echo "Actualizando stack existente ${STACK_NAME}..."
    aws cloudformation deploy \
      --template-file ./config/cloudformation-agent.yaml \
      --stack-name ${STACK_NAME} \
      --parameter-overrides \
        VpcId=vpc-0a8741ac883394d5b \
        SubnetIds="subnet-05a8843fe15747b16,subnet-0c96a572e69454cbd" \
        SQSQueueName="mockhat-assessments-writings.fifo" \
        SQSQueueARN="${SQS_QUEUE_ARN}" \
        ImageTag="${new_tag}" \
        ProjectName="${PROJECT_NAME}" \
       --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
fi

echo "Despliegue completado" 