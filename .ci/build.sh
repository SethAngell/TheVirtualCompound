docker-compose build --build-arg DB_NAME=${DB_NAME} --build-arg DB_USER=${DB_USER} --build-arg DB_PASS=${DB_PASS} --build-arg DB_HOST=${DB_HOST} --build-arg DB_PORT=${DB_PORT} --build-arg S3_KEY=${S3_KEY} --build-arg S3_SECRET_KEY=${S3_SECRET_KEY} 
docker-compose up -d
