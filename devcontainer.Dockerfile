FROM python:3.12.7-slim-bookworm

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir \
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

ENV PATH="/app/venv/bin:$PATH"
CMD ["/bin/bash"]
