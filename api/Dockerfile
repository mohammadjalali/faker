FROM python:3.11-slim-buster

WORKDIR /api/

COPY api.py requirements.txt /api/

RUN pip install -r requirements.txt

CMD ["fastapi", "run", "--workers", "4", "api.py", "--port", "8000"]
