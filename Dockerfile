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
COPY entrypoint-prod.sh gunicorn_config.py ./
COPY ./todo_app/*.py ./todo_app/
COPY ./todo_app/templates/ ./todo_app/templates/
EXPOSE 5000
RUN chmod +x ./entrypoint-prod.sh 
ENTRYPOINT ["sh", "entrypoint-prod.sh"]

FROM base-image as todo-dev
# copy entrypoint script and run
COPY entrypoint-dev.sh ./
EXPOSE 5000
RUN chmod +x ./entrypoint-dev.sh
ENTRYPOINT ["sh", "entrypoint-dev.sh"]

FROM base-image as todo-test
# Install chrome
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable
# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
    echo "Installing chromium webdriver version ${LATEST}" &&\
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
    apt-get install unzip -y &&\
    unzip ./chromedriver_linux64.zip
# Install Firefox and Geckodriver (needs work, commenting out)
# RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
#     wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
#     tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C ./ && \
#     chmod +x ./geckodriver && \
#     rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
# RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
#     apt-get purge firefox && \
#     wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
#     tar xjf $FIREFOX_SETUP -C /opt/ && \
#     ln -s /opt/firefox/firefox ./ && \
#     rm $FIREFOX_SETUP
COPY entrypoint-test.sh ./
COPY ./todo_app/ ./todo_app/
EXPOSE 5000
RUN chmod +x ./entrypoint-test.sh
ENTRYPOINT ["sh", "entrypoint-test.sh"]
