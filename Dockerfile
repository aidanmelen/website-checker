ARG UBUNTU_VERSION=20.04
ARG PYTHON_VERSION=3.9
ARG POETRY_VERSION=1.1.4


FROM ubuntu:${UBUNTU_VERSION} AS workspace
WORKDIR /app
# install workspace tools
RUN apt-get update
RUN apt-get install -y python3-pip git vim curl zsh
RUN pip3 install poetry${POETRY_VERSION+==$POETRY_VERSION}
ENV TERM xterm
ENV ZSH_THEME agnoster
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
# cache the slow installation of python dependencies
COPY pyproject.toml .
RUN poetry install --no-interaction --no-ansi --no-root 2>&1 || poetry update
# install python project with latest source code
COPY . .
RUN poetry install --no-interaction --no-ansi 2>&1 || poetry update
ENTRYPOINT ["poetry", "run"]
CMD ["zsh"]


FROM ubuntu:${UBUNTU_VERSION} AS build
WORKDIR /app
COPY --from=workspace / /
RUN poetry build --format wheel
ENTRYPOINT ["poetry", "run"]
CMD ["zsh"]


FROM python:${PYTHON_VERSION}-alpine AS release
COPY --from=build /app/dist /app/dist
RUN pip install /app/dist/*.whl
ENTRYPOINT ["check"]
