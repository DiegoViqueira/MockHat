#!/bin/bash

# Replace 'your_image_name' with the Docker image name you want to check
IMAGE_NAME="905418182087.dkr.ecr.eu-west-1.amazonaws.com/mockhat-payments.com"

# Get a list of tags for the specified image
tags=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep "^${IMAGE_NAME}:" | awk -F: '{print $2}')

# Filter tags to match semantic versioning format (e.g., 1.2.3) and sort them
latest_tag=$(echo "$tags" | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -n 1)

if [[ -n "$latest_tag" ]]; then
    IFS='.' read -r major minor patch <<< "$latest_tag"

    # Increment the patch number
    new_tag="${major}.${minor}.$((patch + 1))"

    echo "Latest tag for image '$IMAGE_NAME': $latest_tag"
    echo "New tag after incrementing: $new_tag"

    docker build -t $IMAGE_NAME:$new_tag -f ./docker/Dockerfile.payments .
    aws ecr get-login-password | docker login --username AWS --password-stdin *******.dkr.ecr.eu-west-1.amazonaws.com
    docker push $IMAGE_NAME:$new_tag

    aws cloudformation deploy   --template-file ./config/cloudformation-payments.yaml   --stack-name mockhat-payments   --parameter-overrides     HostedZoneId="Z07961711AQSYZYJ8EC9C"   VPC=vpc-0a8741ac883394d5b    AppDomainPrefix="payments"    PublicSubnetIds="subnet-05a8843fe15747b16,subnet-0c96a572e69454cbd"     ImageUrl="$IMAGE_NAME:$new_tag"   --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

else
    echo "No version tags found for image '$IMAGE_NAME' in X.Y.Z format"
fi
