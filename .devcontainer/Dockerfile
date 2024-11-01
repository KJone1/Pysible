FROM python:3.12.7-slim-bookworm

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

RUN python3 -m venv "${VIRTUAL_ENV}" && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    flake8 \
    black \
    isort \
    mypy \
    autopep8 \
    ipython \
    ruff \
    pylint \
    vulture \
    add-trailing-comma \
    unimport \
    pyupgrade \
    bandit \
    poetry \
    pudb \
    pdbpp

CMD ["/bin/bash"]
