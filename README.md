# Agno Documentation Crawler

A high-performance asynchronous web crawler designed to download and convert Agno documentation into markdown format.

## Features
- Asynchronous crawling with memory management
- Parallel processing with configurable batch sizes
- Markdown conversion and storage
- Docker support for easy deployment
- Progress tracking and error handling

## Prerequisites
- Docker Desktop
- Python 3.11+ (for local development)
- Git

## Quick Start

### Using Docker (Recommended)
1. Clone the repository:
   ```bash
   git clone https://github.com/Rythamo8055/crawler.git
   cd agno-crawler
   ```

2. Build and run using Docker Compose:
   ```bash
   docker-compose up --build
   ```

### Local Development Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the crawler:
   ```bash
   python app/crawler.py
   ```

## Project Structure
```
agno-crawler/
├── app/
│   ├── crawler.py      # Main crawler logic
│   └── config.py       # Configuration settings
├── docker/
│   ├── Dockerfile      # Multi-stage build for container
│   └── docker-compose.yml
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Configuration
Copy `.env.example` to `.env` and adjust settings:
```env
BATCH_SIZE=10
OUTPUT_DIR=./output
LOG_LEVEL=INFO
```

## Output
Crawled documentation is saved in the output directory with the following structure:
```
output/
├── agents/
├── reference/
├── tools/
└── workflows/
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License

## Support
For issues and feature requests, please use the GitHub issue tracker.