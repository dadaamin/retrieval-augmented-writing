# Fetching data from SHIP

Based on [fhirpack](https://github.com/fhirpack/fhirpack)

See this spreadsheet for available FHIR resources (Amin can share access): https://docs.google.com/spreadsheets/d/1A5qsj5TR4SzG6iFi1dwQqgECwwPAwM9ljOvmJra6Re0/edit?invite=COWhtfQL#gid=0

## Setup

Fill your credentials into `.env` (see `.env.example`).

```sh
conda env update -f environment.yml
conda activate raw-fhir

pip install -r requirements-dev.txt
```
