FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
#RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=50051
ENV MODEL_PATH=/app/models/model.json
ENV MODEL_VERSION=v1.0.0
EXPOSE 50051
CMD ["python", "-m", "server.server"]