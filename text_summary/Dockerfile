FROM python:3.8.8-slim-buster

EXPOSE 8000

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.1.4

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  netcat \
  gcc \
  postgresql \
  && apt-get clean

RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . .

COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]