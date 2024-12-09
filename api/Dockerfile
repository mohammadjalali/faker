FROM python:3.11-slim-buster

WORKDIR /api/

COPY api.py requirements.txt /api/

RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir -r requirements.txt

CMD ["fastapi", "run", "--workers", "4", "api.py", "--port", "8000"]
