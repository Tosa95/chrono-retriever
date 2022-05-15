FROM python:3.9

COPY . /app
WORKDIR /app
RUN python -m venv /venv
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install poetry && poetry install

WORKDIR /app/src
CMD python -m uvicorn chrono.backend.main:app --host 0.0.0.0 --reload