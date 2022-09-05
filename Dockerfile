FROM python:3.10-alpine
# If we need to pass through a GPU, we can do so with the nvidia CUDA images:
# FROM nvidia/cuda:11.7.1-base-ubuntu22.04

RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# # install server dependencies
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "app.py"]