FROM bitnami/python:3.7.1
WORKDIR /app
COPY . ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--pythonpath", ".", "main:app"]