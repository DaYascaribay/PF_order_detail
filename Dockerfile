# Usa una imagen liviana de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente
COPY . .

# Expone el puerto donde corre Flask (ajusta si cambias el puerto en run.py)
EXPOSE 1015

# Comando para correr la app
CMD ["python", "run.py"]