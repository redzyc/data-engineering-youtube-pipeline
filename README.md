# data-engineering-youtube-pipeline

An end-to-end data engineering pipeline implementing the Lambda Architecture. The project demonstrates ingestion, batch processing, streaming simulation, and visualization using a modern data stack (Spark, Kafka, NiFi, MinIO, Docker).

## Table of Contents
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Environment variables](#environment-variables)
- [Run the ingestion client](#run-the-ingestion-client)
- [Contributing](#contributing)
- [License](#license)

---

## Architecture

This repository follows the Lambda Architecture to balance low-latency stream processing and accurate historical batch processing:

- Ingestion Layer: Collects data from external APIs (e.g. YouTube Data API v3).
- Storage / Data Lake: Raw data persisted to an S3-compatible store (MinIO) for later batch processing.
- Speed Layer: Simulated streaming via high-frequency polling and Kafka for near-real-time processing.
- Batch Layer: Apache Spark jobs for historical/large-scale transformations.
- Serving Layer: Processed results are stored in a serving database (Postgres) and visualized via BI tools.

---

## Features

- YouTube ingestion client with robust error handling
- Support for batch processing (Spark) and simulated streaming (polling + Kafka)
- Modular code layout for ingestion, processing, and visualization

---

## Project Structure

Top-level layout:

```
data-engineering-youtube-pipeline/
├── config/              # configuration files and templates
├── data/                # sample & raw data
│   └── raw/
├── docker/              # docker-compose and related infra
├── src/
│   ├── ingestion/       # data ingestion clients and helpers
│   ├── processing/      # Spark jobs and ETL code
│   └── visualization/   # dashboard and visualization configs
├── tests/               # unit and integration tests
├── requirements.txt     # Python dependencies
└── README.md            # this file
```

---

## Prerequisites

- Python 3.8+ (virtual environment recommended)
- Docker & Docker Compose (for running infra like MinIO and Kafka locally)

---

## Setup

1. Clone the repository

```bash
git clone https://github.com/redzyc/data-engineering-youtube-pipeline.git
cd data-engineering-youtube-pipeline
```

2. Create and activate a virtual environment, then install dependencies

Mac / Linux (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
# upgrade packaging tools before installing requirements
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
python -m venv venv
# activate the venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Tip: You can also use pipx, pipenv, or poetry if you prefer other virtual environment / dependency managers.

---

## Environment variables

This repository expects the YouTube API key and other secrets to be provided as environment variables. You can store them in a `.env` file in the project root or export them directly in your shell.

Example `.env` (do not commit your secrets to source control):

```
YOUTUBE_API_KEY=your_api_key_here
# Optionally: OTHER_SERVICE_KEY=...
```


---

## Run the ingestion client

Run a quick ingestion script to test your setup:

```bash
# from project root
python src/ingestion/youtube_client.py
```

If your API key is correctly set in the environment, the client will fetch sample results and print or save them to `data/raw/` depending on the configured behavior.

---

## Contributing

Contributions are welcome! Please open an issue to discuss larger changes. For code contributions:

1. Fork the repository
2. Create a feature branch
3. Add tests for any new behavior
4. Open a pull request with a clear description

---

## License

This project is licensed under the terms defined in the `LICENSE` file.

---
