FROM python:3.9-slim

# WORKDIR /scheduling_optimization

COPY . .

RUN pip3 install --no-cache-dir --upgrade pip

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]