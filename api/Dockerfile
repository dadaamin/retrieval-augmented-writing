FROM continuumio/miniconda3:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get --allow-releaseinfo-change-suite update && apt-get install build-essential -y

WORKDIR /app
COPY environment.yml /app/
RUN conda env create -f environment.yml

COPY setup.py /app/setup.py
COPY src /app/src/
COPY data /app/data/
COPY README.md /app/README.md

COPY docker/entrypoint.sh /app/entrypoint.sh
COPY docker/seed.sh /app/seed.sh

RUN conda run -n raw pip install -e .

EXPOSE 8000
CMD ./entrypoint.sh
