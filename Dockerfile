FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache build-base gcc musl-dev libffi-dev
RUN pip3 install pip --upgrade

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apk del build-base gcc musl-dev libffi-dev

COPY vedro_telemetry_api/ vedro_telemetry_api/
COPY migrations/ migrations/

CMD ["python3", "-m", "vedro_telemetry_api"]
