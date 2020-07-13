FROM localhost/centos8/py38

ENV APP_ROOT=/data_server
ENV PIPENV_PYTHON=python

COPY ./app ${APP_ROOT}/app
COPY Pipfile ${APP_ROOT}/
COPY ./start.bash ${APP_ROOT}/start.bash
WORKDIR ${APP_ROOT}

EXPOSE 8000

RUN pipenv install --system --skip-lock

CMD ["/usr/bin/bash", "./start.bash"]