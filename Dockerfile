FROM python:3.11
WORKDIR /hammer_system_test_task

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry
COPY ./pyproject.toml .
RUN poetry install
COPY . .
