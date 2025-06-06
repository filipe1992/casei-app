import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile
import uuid
from datetime import datetime, timezone
from app.core.config import settings
import logging

class S3Service:
    def __init__(self):
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        except ClientError as e:
            logging.error(f"Erro ao criar cliente S3: {str(e)}")
            self.s3_client = None
        self.bucket_name = settings.S3_BUCKET_NAME
    
    def upload_file(self, object_name: str, file_input: UploadFile):
        """
        Faz o upload de um arquivo para o S3
        """
        try:
            self.s3_client.upload_fileobj(file_input.file, self.bucket_name, object_name)
        except ClientError as e:
            logging.error(f"Erro ao fazer upload do arquivo para o S3: {str(e)}")
            return False
        return True
        

    def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """
        Gera uma URL pré-assinada para acessar um objeto no S3
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))

    def generate_presigned_post(self, object_name: str, expiration: int = 3600):
        """
        Gera uma URL pré-assinada para upload de arquivo
        """
        try:
            response = self.s3_client.generate_presigned_post(
                self.bucket_name,
                object_name,
                Fields=None,
                Conditions=None,
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_file(self, object_name: str):
        """
        Deleta um arquivo do S3
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def generate_file_key(user_id: int, guest_id: int, filename: str) -> str:
        """
        Gera uma chave única para o arquivo no S3
        """
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())
        extension = filename.split('.')[-1]
        
        return f"user_{user_id}/guest_{guest_id}/{timestamp}_{unique_id}.{extension}"
    
    @staticmethod
    def generate_file_key_user(user_id: int, filename: str) -> str:
        """
        Gera uma chave única para o arquivo no S3
        """
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())
        extension = filename.split('.')[-1]
        return f"user_{user_id}/personal/{timestamp}_{unique_id}.{extension}"

s3_service = S3Service() 