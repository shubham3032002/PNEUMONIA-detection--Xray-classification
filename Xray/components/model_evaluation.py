import sys
from typing import Tuple

import torch
from torch.nn import CrossEntropyLoss, Module
from torch.optim import SGD, Optimizer
from torch.utils.data import DataLoader

from Xray.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelEvaluationArtifact,
    ModelTrainerArtifact,
)
from Xray.entity.config_entity import ModelEvaluationConfig
from Xray.exception import XRayException
from Xray.logger import logger
from Xray.ml_model.model.arch import Net


class ModelEvaluation:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_evaluation_config: ModelEvaluationConfig,
        model_trainer_artifact: ModelTrainerArtifact,
    ):

        self.data_transformation_artifact = data_transformation_artifact

        self.model_evaluation_config = model_evaluation_config

        self.model_trainer_artifact = model_trainer_artifact



    def configuration(self) -> Tuple[DataLoader, Module, float, Optimizer]:
        logger.info("Entered the configuration method of Model evaluation class")

        try:
            test_dataloader: DataLoader = (
                self.data_transformation_artifact.transformed_test_object
            )

            model: Module = Net()

            model: Module = torch.load(self.model_trainer_artifact.trained_model_path)

            model.to(self.model_evaluation_config.device)

            cost: Module = CrossEntropyLoss()

            optimizer: Optimizer = SGD(
                model.parameters(), **self.model_evaluation_config.optimizer_params
            )

            model.eval()

            logger.info("Exited the configuration method of Model evaluation class")

            return test_dataloader, model, cost, optimizer

        except Exception as e:
            raise XRayException(e, sys)
        


    def test_net(self) -> float:
        logger.info("Entered the test_net method of Model evaluation class")

        try:
            test_dataloader, net, cost, _ = self.configuration()

            with torch.no_grad():
                holder = []

                for _, data in enumerate(test_dataloader):
                    images = data[0].to(self.model_evaluation_config.device)

                    labels = data[1].to(self.model_evaluation_config.device)

                    output = net(images)

                    loss = cost(output, labels)

                    predictions = torch.argmax(output, 1)

                    for i in zip(images, labels, predictions):
                        h = list(i)

                        holder.append(h)

                    logger.info(
                        f"Actual_Labels : {labels}     Predictions : {predictions}     labels : {loss.item():.4f}"
                    )

                    self.model_evaluation_config.test_loss += loss.item()

                    self.model_evaluation_config.test_accuracy += (
                        (predictions == labels).sum().item()
                    )

                    self.model_evaluation_config.total_batch += 1

                    self.model_evaluation_config.total += labels.size(0)

                    logger.info(
                        f"Model  -->   Loss : {self.model_evaluation_config.test_loss/ self.model_evaluation_config.total_batch} Accuracy : {(self.model_evaluation_config.test_accuracy / self.model_evaluation_config.total) * 100} %"
                    )

            accuracy = (
                self.model_evaluation_config.test_accuracy
                / self.model_evaluation_config.total
            ) * 100

            logger.info("Exited the test_net method of Model evaluation class")

            return accuracy

        except Exception as e:
            raise XRayException(e, sys)
        
        

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        logger.info(
            "Entered the initiate_model_evaluation method of Model evaluation class"
        )

        try:
            accuracy = self.test_net()

            model_evaluation_artifact: ModelEvaluationArtifact = (
                ModelEvaluationArtifact(model_accuracy=accuracy)
            )

            logger.info(
                "Exited the initiate_model_evaluation method of Model evaluation class"
            )
            print(f"Evalidation_accuracy:{accuracy}")

            return model_evaluation_artifact

        except Exception as e:
            raise XRayException(e, sys)
