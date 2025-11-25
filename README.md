# data-engineering-youtube-pipeline
End-to-end Data Engineering pipeline implemented using Lambda Architecture. Features data ingestion, batch and streaming processing, and visualization leveraging a modern Big Data stack (Spark, Kafka, NiFi, MinIO, Docker).

---

# Architecture
The project follows the **Lambda Architecture** principles to handle both batch and real-time data processing:
1.  **Ingestion Layer:** Fetching data from external APIs (YouTube).
2.  **Storage Layer (Data Lake):** MinIO (S3 compatible) for raw data storage.
3.  **Speed Layer (Streaming):** Apache Kafka & Spark Streaming.
4.  **Batch Layer:** Apache Spark for historical data processing.
5.  **Serving Layer:** SQL Databases (Postgres) & BI Dashboards.

---

## Project Structure
The repository is organized to separate concerns and ensure scalability:

data-engineering-youtube-pipeline/
├── config/              # Configuration files
├── docker/              # Docker infrastructure (docker-compose)
├── src/
│   ├── ingestion/       # Python scripts for data extraction (APIs)
│   ├── processing/      # Spark jobs for transformation
│   └── visualization/   # Dashboard configs
├── tests/               # Unit and integration tests
├── .env                 # Environment variables (not committed)
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

## Phase I: Data Source & Extractions (Completed)

The first phase focuses on establishing secure connectivity with external data sources.

Key Features
Source: YouTube Data API v3.

Security: API Keys are managed via environment variables (.env) and excluded from version control.

Client Implementation: A modular Python client (YouTubeClient) handles authentication, error handling, and data fetching.

Data Entities: The pipeline extracts Video Metadata (Title, ID, Channel) and Statistics (View Count, Like Count).

### Technical Note on Streaming
While the project implements a "Streaming" layer, it is important to note that the YouTube Data API v3 is REST-based and does not support native WebSocket streaming (push).

Solution: We simulate streaming using a High-Frequency Polling mechanism.

Implementation: Apache NiFi / Python scripts allow us to fetch "new" data at short intervals, effectively creating a data stream for the downstream Kafka topics.

### Qucik Start
Prerequisites:
    Docker & Docker Compose
    Python 3.x

### Setup

#### 1. Clone the repository:

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd data-engineering-masterclass
\`\`\`

#### 2. Create a virtual environment and install dependencies:

\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

#### 3. Configure Environment Variables:

Create a **.env** file in the root directory:

\`\`\`
# .env file content
YOUTUBE_API_KEY=your_api_key_here
\`\`\`

#### 4. Run the ingestion test:

\`\`\`bash
python src/ingestion/youtube_client.py
\`\`\`
