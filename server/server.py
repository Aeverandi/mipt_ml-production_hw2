import os
import grpc
from concurrent import futures
import pandas as pd
import xgboost as xgb
import numpy as np
import logging
from grpc_reflection.v1alpha import reflection

from protos import model_pb2
from protos import model_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def predict_function(data: pd.DataFrame):
    dmatrix = xgb.DMatrix(data)
    preds = model.predict(dmatrix)
    return preds
class PredictionService(model_pb2_grpc.PredictionServiceServicer):
    def __init__(self):
        self.model_path = os.environ.get('MODEL_PATH', '/app/models/model.json')
        self.model_version = os.environ.get('MODEL_VERSION', 'v1.0.0')
        logger.info(f"Загружаем модель из {self.model_path}")
        model = xgb.XGBRegressor()
        model.load_model(self.model_path)
        self.model = model
        logger.info("Модель успешно загружена")

    def Health(self, request, context):  # /health
        return model_pb2.HealthResponse(
            status="ok",
            model_version=self.model_version
        )

    def Predict(self, request, context): # /predict
        try:
            features = {
                'platelets': request.platelets,
                'serum_creatinine': request.serum_creatinine,
                'serum_sodium': request.serum_sodium,
                'age': request.age
            }

            df = pd.DataFrame([features])
            prediction = self.model.predict(df)[0] #predict_function(df)[0]
            
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(df)[0]
                confidence = max(probabilities)
            else:
                confidence = 1.0

            return model_pb2.PredictResponse(
                prediction=str(prediction),
                confidence=float(confidence),
                model_version=self.model_version
            )
            
        except Exception as e:
            logger.error(f"Ошибка при предсказании: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Ошибка обработки: {str(e)}")
            return model_pb2.PredictResponse()

def serve():     # gRPC сервер
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_PredictionServiceServicer_to_server(PredictionService(), server)

    SERVICE_NAMES = (
        model_pb2.DESCRIPTOR.services_by_name['PredictionService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    port = os.environ.get('PORT', '50051')
    server.add_insecure_port(f'[::]:{port}')
    
    logger.info(f"Сервер запущен на порту {port}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()