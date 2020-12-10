ARG PYTHON_VERSION=3.9
ARG POETRY_VERSION=1.1.4

FROM python:${PYTHON_VERSION} as base
RUN pip install --upgrade pip \
 && pip install poetry${POETRY_VERSION+==$POETRY_VERSION}
WORKDIR /app
COPY pyproject.toml *poetry.lock .
RUN poetry install --no-interaction --no-ansi --no-root
ENTRYPOINT ["poetry", "run", "bash"]

FROM base as dev
COPY . .
RUN poetry install --no-interaction --no-ansi

FROM dev AS build
RUN poetry build --format wheel

FROM python:${PYTHON_VERSION}-alpine AS release
COPY --from=build /app/dist /app/dist
RUN pip install /app/dist/*.whl
ENTRYPOINT ["check"]
