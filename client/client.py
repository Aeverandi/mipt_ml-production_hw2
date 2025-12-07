import grpc
import logging
import os

from protos import model_pb2
from protos import model_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run():
    server_address = os.environ.get('SERVER_ADDRESS', 'localhost:50051')
    channel = grpc.insecure_channel(server_address)
    stub = model_pb2_grpc.PredictionServiceStub(channel)
    
    logger.info("Проверяем здоровье сервиса...")
    health_request = model_pb2.HealthRequest()
    health_response = stub.Health(health_request)
    logger.info(f"Health check: {health_response}")
    
    logger.info("Делаем предсказание...")
    predict_request = model_pb2.PredictRequest(
        platelets = 180,
        serum_creatinine = 0.9,
        serum_sodium = 135,
        age = 75
    )
    predict_response = stub.Predict(predict_request)
    logger.info(f"Результат предсказания: {predict_response}")

if __name__ == '__main__':
    run()