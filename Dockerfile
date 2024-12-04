FROM python3.10-slim
WORKDIR /src
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY containers .
CMD ["uvicorn", "src.app.main:app", "--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]