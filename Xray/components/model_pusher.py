import sys
from Xray.cloud_storage.s3_ops import S3Operation
from Xray.entity.config_entity import ModelPusherConfig
from Xray.exception import XRayException
from Xray.logger import logger


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig):
        """
        Class Name :   ModelPusher
        Description :   This class is responsible for pushing the trained model to an S3 bucket.
        
        Input : ModelPusherConfig instance
        
        Output : None
        """
        self.model_pusher_config = model_pusher_config
        self.s3 = S3Operation()

    def initiate_model_pusher(self):
        """
        Method Name :   initiate_model_pusher

        Description :   This method uploads the best trained model to the specified S3 bucket.
        
        Output      :   None
        
        Raises      :   XRayException
        """
        logger.info("Entered initiate_model_pusher method of ModelPusher class")
        try:
            # Fetch configuration details from ModelPusherConfig
            local_model_path = self.model_pusher_config.local_model_path
            s3_model_key = self.model_pusher_config.s3_model_key
            s3_bucket_name = self.model_pusher_config.s3_bucket_name

            # Uploading the best model to S3 bucket
            self.s3.upload_file(
                file_name=local_model_path,
                object_name=s3_model_key,
                bucket_name=s3_bucket_name,
                remove=False,
            )
            logger.info(f"Uploaded best model to S3 bucket: {s3_bucket_name}")
            logger.info("Exited initiate_model_pusher method of ModelPusher class")

        except Exception as e:
            logger.error("An error occurred during model pushing", exc_info=True)
            raise XRayException(e, sys) from e
