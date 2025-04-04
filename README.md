# Discounted Product Aggregator

A FastAPI-based backend service that aggregates discounted products from e-commerce websites (Zara, Amazon) and exposes the data through a JSON API.

## Features

- 🕷️ **Async Web Scraping** - Concurrent scraping using Playwright
- 🚀 **FastAPI Endpoints** - Clean REST API with OpenAPI documentation
- 🐳 **Docker Ready** - Full containerization with PostgreSQL
- 🛒 **E-commerce Support** - Zara & Amazon (extensible to others)
- 🔍 **Smart Filtering** - Duplicate prevention, price tracking
- 📦 **Poetry Management** - Python dependency management
- ⚡ **Background Tasks** - Auto-refresh every 10 seconds

## Getting Started

### Prerequisites

- Python 3.9+
- Poetry (`pip install poetry`)
- Docker & Docker Compose
- Playwright browsers (`playwright install`)

### Installation

```bash
# Clone repository
git clone https://github.com/MohamadAhmadi100/discounted-product-aggregator.git
cd discounted-product-aggregator

# Install dependencies with Poetry
poetry install

# Install Playwright browsers
poetry run playwright install && playwright install chromium
```

### Configuration
Create .env file:

```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/scraper
```

### Running with Poetry
```bash
# Activate virtual environment
poetry shell

# Start application
poetry run uvicorn app.main:app --reload
```

### Running with Docker
```bash
# Start all services
docker-compose up --build -d

# Stop and remove containers
docker-compose down
```

### API Documentation

Access interactive docs at http://localhost:8000/docs

Example Requests:

```bash
# Get all discounted products
curl http://localhost:8000/api/v1/discounted-products

# Filter by store and minimum discount
curl "http://localhost:8000/api/v1/discounted-products?store=amazon&min_discount=20"

# Filter by category
curl "http://localhost:8000/api/v1/discounted-products?category=clothing"
```

