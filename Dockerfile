FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando para arrancar el servidor web Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
