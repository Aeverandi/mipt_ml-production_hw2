# Домашнее задание №2
Выполнил: **Лобан Константин Михайлович, группа М08-402ПА**

В продолжение [первого ДЗ](https://github.com/Aeverandi/mipt_ml-production_hw/tree/new_ef_predict), использована почти та же модель (обученная [на том же датасете](https://www.kaggle.com/datasets/aadarshvelu/heart-failure-prediction-clinical-records)) для прогнозирования фракции сердечного выброса (`ejection_fraction`) у пациентов с сердечной недостаточностью (для определения которого необходимо выполнение эхокардиографии), но умеющая давать не менее качественные предсказания всего по 4 признакам: натрию (`serum_sodium`) и креатинину (`serum_creatinine`) сыворотки крови, тромбоцитам (`platelets`) и возрасту (`age`) пациента.

## Инструкция по локальному развертыванию
Перед запуском кода убедитесь, что у Вас запущен **Docker Desktop**!
```
git clone https://github.com/Aeverandi/mipt_ml-production_hw2.git
cd mipt_ml-production_hw2
pip install -r requirements.txt
docker build -t grpc-ml-service .
docker run -p 50051:50051 grpc-ml-service
```
Затем запустите терминал в той же директории (mipt_ml-production_hw2).

Предварительно убедитесь, что у Вас установлен **grpcurl** (если нет, [то скачайте его](https://github.com/fullstorydev/grpcurl/releases))
```
grpcurl -plaintext localhost:50051 mlservice.v1.PredictionService.Health
python -m client.client
```
## Скриншоты
После запуска контейнера он должен отобразиться в Docker Desktop:
<img width="1214" height="380" alt="2025-12-08_01-20-18" src="https://github.com/user-attachments/assets/462abb21-6fcc-48fe-84ae-6746f77cb172" />
Комманды запуска контейнера и вызовов /health и /predict:
<img width="910" height="534" alt="2025-12-08_01-18-25" src="https://github.com/user-attachments/assets/13e68463-0d47-48c0-a4b9-3d85eab9e17c" />

