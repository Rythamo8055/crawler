# Agno Documentation Crawler

A high-performance asynchronous web crawler designed to download and convert web content into markdown format.

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/Rythamo8055/crawler.git
   cd crawler
   ```

2. Start the application:
   ```bash
   docker compose up
   ```

3. Open http://localhost:7860 in your browser to access the crawler interface.

## Features
- Multiple URL input methods:
  - Comma-separated URLs
  - Text file with URLs
  - XML sitemap content
  - XML sitemap URL
- User-selectable output directory
- Asynchronous crawling with memory management
- Parallel processing with configurable batch sizes
- Markdown conversion and storage

## Configuration (Optional)

The application works out of the box, but you can customize it by creating a `.env` file:

```env
BATCH_SIZE=10    # Number of URLs to process in parallel
OUTPUT_DIR=./output    # Where to save the markdown files
LOG_LEVEL=INFO    # Logging verbosity
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

## Local Development

If you prefer to run without Docker:

1. Install Python 3.11+
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app/crawler.py
   ```

## Support
For issues and feature requests, please use the GitHub issue tracker.

## License
MIT License