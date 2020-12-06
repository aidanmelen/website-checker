ARG PYTHON_VERSION=3.9
ARG POETRY_VERSION=1.1.4

FROM python:${PYTHON_VERSION} as base
RUN pip install --upgrade pip \
 && pip install poetry${POETRY_VERSION+==$POETRY_VERSION}
WORKDIR /app
COPY pyproject.toml *poetry.lock .
RUN poetry install --no-interaction --no-ansi --no-root

FROM base as dev
COPY . .
RUN poetry install --no-interaction --no-ansi
ENTRYPOINT ["poetry", "run"]
CMD ["bash"]

FROM dev AS pre-commit
ENV PRE_COMMIT_CMD='poetry run pre-commit run --all-files'
RUN ${PRE_COMMIT_CMD}
ENTRYPOINT ${PRE_COMMIT_CMD}

FROM dev AS safety
ENV EXPORT_CMD='poetry export --format requirements.txt --output r.txt'
ENV SAFETY_CMD='poetry run safety check --full-report --file r.txt'
RUN ${EXPORT_CMD} && ${SAFETY_CMD} && rm -rf r.txt
ENTRYPOINT ${EXPORT_CMD} && ${SAFETY_CMD} && rm -rf r.txt

FROM dev AS pytest
ENV PYTEST_CMD='poetry run pytest --cov -vvv'
RUN ${PYTEST_CMD}
ENTRYPOINT ${PYTEST_CMD}

FROM dev AS build
ENV BUILD_CMD='poetry build --format wheel'
RUN ${BUILD_CMD}
ENTRYPOINT ${BUILD_CMD}

FROM python:${PYTHON_VERSION}-alpine AS release
COPY --from=build /app/dist /app/dist
RUN pip install /app/dist/*.whl
ENTRYPOINT ["check"]
