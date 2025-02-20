import sys
from Xray.cloud_storage.s3_ops import S3Operation


from Xray.entity.config_entity import ModelPusherConfig
from Xray.exception import XRayException
from Xray.logger import logger


class ModelPusher:
    def __init__(self,model_pusher_config: ModelPusherConfig):

        self.model_pusher_config = model_pusher_config
        self.s3 = S3Operation()


    
    def initiate_model_pusher(self):

        """
        Method Name :   initiate_model_pusher

        Description :   This method initiates model pusher. 
        
        Output      :    Model pusher artifact 
        """
        logger.info("Entered initiate_model_pusher method of Modelpusher class")
        try:
            # Uploading the best model to s3 bucket
            self.s3.upload_file(
                "model/model.pt",
                "model.pt",
                "lungxray20",
                remove=False,
            )
            logger.info("Uploaded best model to s3 bucket")
            logger.info("Exited initiate_model_pusher method of ModelTrainer class")


        except Exception as e:
            raise e
