# Hanif Backend API - Production Ready

Production-ready FastAPI backend dengan async database support, modular structure, dan Docker deployment.

## 🚀 Features

- ✅ **Async SQLAlchemy** - Performance 10x lebih cepat dengan async database operations
- ✅ **Config Validation** - Pydantic-settings untuk environment variable validation
- ✅ **Modular Structure** - Scalable architecture dengan APIRouter
- ✅ **Docker Support** - Ready untuk production deployment
- ✅ **Automated Tests** - Pytest dengan async test coverage
- ✅ **CORS Support** - Ready untuk frontend integration
- ✅ **Health Checks** - Monitoring dan load balancer ready
- ✅ **OpenAPI Docs** - Auto-generated API documentation

## 📁 Project Structure

```
backend-production-example/
├── app/
│   ├── __init__.py
│   ├── main.py              # App factory
│   ├── config.py            # Configuration validation
│   ├── database.py          # Async database connection
│   ├── models.py            # SQLAlchemy models
│   └── schemas.py           # Pydantic schemas
├── routers/
│   ├── __init__.py
│   ├── categories.py        # Category endpoints
│   └── products.py          # Product endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   └── test_api.py          # API tests
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🛠️ Quick Start

### Option 1: Local Development (Recommended for Learning)

```bash
# 1. Clone repository
git clone https://github.com/hokicuanxz/backend-production-example.git
cd backend-production-example

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env and set your DATABASE_URL

# 5. Run database migrations (if using Alembic)
# For now, tables are created automatically in DEBUG mode

# 6. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Docker (Production)

```bash
# 1. Clone repository
git clone https://github.com/hokicuanxz/backend-production-example.git
cd backend-production-example

# 2. Copy environment file
cp .env.example .env

# 3. Start all services (API + PostgreSQL + pgAdmin)
docker-compose up -d

# 4. Check logs
docker-compose logs -f api

# 5. Stop services
docker-compose down
```

## 📖 API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Application
APP_NAME=Hanif Backend API
APP_VERSION=1.0.0
DEBUG=true  # Set to false in production

# Database (PostgreSQL with asyncpg)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/hanif_db

# Server
HOST=0.0.0.0
PORT=8000
```

### Docker Environment Variables

For Docker deployment, use these in `.env`:

```bash
# Database
DB_USER=hanif
DB_PASSWORD=hanif_secret
DB_NAME=hanif_db
DB_PORT=5432

# API
API_PORT=8000
DEBUG=false

# pgAdmin
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin
PGADMIN_PORT=5050
```

## 🧪 Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

## 📡 API Endpoints

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/category` | Create new category |
| POST | `/category/{id}` | Get category details |
| GET | `/category` | List all categories |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/add-product` | Create new product |
| GET | `/product` | List products (with search & pagination) |
| PUT | `/change-product/{id}` | Update product |
| DELETE | `/product/{id}` | Delete product |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f db

# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Rebuild after code changes
docker-compose up -d --build

# Run tests in container
docker-compose run --rm api pytest
```

## 🎯 Next Steps (Learning Path)

This project is designed as a learning resource. Here's a suggested path:

1. **Understand the Structure** - Read through `app/main.py` and `app/config.py`
2. **Modify Endpoints** - Try adding a new endpoint in `routers/`
3. **Add Authentication** - Implement JWT authentication
4. **Add Alembic** - Set up database migrations
5. **Deploy** - Deploy to a cloud provider (Railway, Render, AWS)

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Docker Documentation](https://docs.docker.com/)
- [pytest Documentation](https://docs.pytest.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

---

**Made with ❤️ for learning backend development with Python**
