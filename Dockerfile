FROM python:3.8-buster as base-image
# setup poetry and environment
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    && mkdir /code
WORKDIR /code
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH = "${PATH}:/root/.poetry/bin"
# install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

FROM base-image as todo-prod
# copy app code and run gunicorn
COPY entrypoint-prod.sh ./*.py ./
COPY ./templates/ ./templates/
EXPOSE 5000
RUN chmod +x ./entrypoint-prod.sh 
ENTRYPOINT ["sh", "entrypoint-prod.sh"]

FROM base-image as todo-dev
# copy app code, test code and run flask
# COPY entrypoint-dev.sh ./*.py ./
# COPY ./templates/ ./templates/
# COPY ./tests/ ./tests/
COPY entrypoint-dev.sh ./
EXPOSE 5000
RUN chmod +x ./entrypoint-dev.sh
ENTRYPOINT ["sh", "entrypoint-dev.sh"]
