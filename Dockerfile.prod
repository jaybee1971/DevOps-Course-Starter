FROM python:3.8-buster
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
# copy app code and run gunicorn
COPY entrypoint.sh ./*.py ./
COPY ./templates/ ./templates/
EXPOSE 5000
RUN chmod +x ./entrypoint.sh 
ENTRYPOINT ["sh", "entrypoint.sh"]
