#!/bin/bash
set -e

# Configuración
PROJECT_NAME="mockhat-ai-agent"
AWS_REGION="eu-west-1"  # Cambia a tu región

# Obtener el ID de la cuenta de AWS
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Construir la imagen Docker
echo "Construyendo la imagen Docker..."
docker build -t ${PROJECT_NAME}:latest -f ./docker/Dockerfile.agent .

# Iniciar sesión en ECR
echo "Iniciando sesión en ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Etiquetar la imagen para ECR
ECR_REPOSITORY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${PROJECT_NAME}"
echo "Etiquetando la imagen para ECR: ${ECR_REPOSITORY}"
docker tag ${PROJECT_NAME}:latest ${ECR_REPOSITORY}:latest

# Subir la imagen a ECR
echo "Subiendo la imagen a ECR..."
docker push ${ECR_REPOSITORY}:latest

echo "Imagen subida correctamente a ECR: ${ECR_REPOSITORY}:latest"

# Actualizar el servicio ECS (opcional)
read -p "¿Deseas actualizar el servicio ECS? (s/n): " update_service
if [[ $update_service == "s" ]]; then
    echo "Actualizando el servicio ECS..."
    aws ecs update-service --cluster ${PROJECT_NAME} --service ${PROJECT_NAME} --force-new-deployment --region ${AWS_REGION}
    echo "Servicio ECS actualizado correctamente"
fi

echo "Despliegue completado" 