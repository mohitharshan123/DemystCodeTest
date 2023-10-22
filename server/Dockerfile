FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/server

COPY requirements.txt /app/server/

# Build psycopg2-binary from source -- add required required dependencies
RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev && \
        pip install --no-cache-dir -r requirements.txt && \
        apk --purge del .build-deps

COPY . /app/server/

COPY entrypoint.sh /app/server/
RUN chmod +x /app/server/entrypoint.sh

ENTRYPOINT ["/app/server/entrypoint.sh"]