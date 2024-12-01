FROM ghcr.io/pyvista/pyvista:latest-slim

EXPOSE 8080
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py", "serve", "--host=0.0.0.0", "--port=8080"]