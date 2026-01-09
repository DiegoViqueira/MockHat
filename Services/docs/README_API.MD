# 🔌 MockHat Backend API

The REST API for the MockHat AI system, designed to support automated English writing assessments using cutting-edge LLMs (Large Language Models). This backend enables text analysis, structured feedback, and assessment orchestration for CEFR-level writing tasks.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [API Specifications](#api-specifications)
- [Rate Limits & Quotas](#rate-limits--quotas)
- [Security](#security)
- [Development](#development)
- [Docker Support](#docker-support)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Contributing](#contributing)
- [TODO](#todo)
- [License](#license)
- [Support](#support)

---

## Overview

This backend powers the core writing evaluation engine in the MockHat platform and exposes robust RESTful endpoints to:

- Submit written assignments for analysis
- Retrieve CEFR-aligned feedback
- Integrate with payment and subscription tiers
- Support real-time evaluations with LLMs (OpenAI, Groq)

---

## Folder structure

```
.
├── app/                   # Main application directory
│   ├── chains/            # LLM prompt chains
│   ├── core/              # Core utilities & Config
│   ├── databases/         # Rubric & Few Shot Databases
│   ├── decorators/        # Custom Python decorators
│   ├── enums/             # Project-wide enumerations
│   ├── events/            # Lifespam events
│   ├── factories/         # Object creation utilities
│   ├── handlers/          # Debug , Exceptions handlers
│   ├── i18n/              # Internationalization utilities
│   ├── loggers/           # Logging configuration
│   ├── middlewares/       # Middleware components
│   ├── models/            # Pydantic/DB models
│   ├── queue/             # Background job queues
│   ├── routes/            # API route definitions (Controllers)
│   ├── services/          # Business logic services
│   ├── agent.py           # AI Agent service entry point
│   ├── apy.py             # API server entry point
│   ├── paymets.py         # Payment service entry point
├── config/                # Environment and config files
├── dockers/               # Docker-related files
├── docs/                  # Documentation files
├── scripts/               # Shell scripts for CI/CD and deployment
├── tests/                 # Unit and integration tests
├── tools/                 # Developer tools and scripts
├── requirements.txt       # Core dependencies
├── requierements.dev.txt  # Dev-only dependencies
```

## API Specifications

### Base URLs

- Development: `http://localhost:8000`
- Production: `https://api.mockhat`

### API DOCS (swagger)

- Development: `http://localhost:8000/docs`
- Production: `https://api.mockhat/docs`

### Authentication

All requests require JWT authentication:

```http
Authorization: Bearer <JWT_TOKEN>
```

## Rate Limits & Constraints

### API Limits

- Requests per minute: 600
- File upload size: 10MB

### Assessment Quotas

| Tier           | Limit                 |
| -------------- | --------------------- |
| **Free**       | 50 assessments/month  |
| **Pro**        | 100 assessments/month |
| **Enterprise** | Custom                |

## Security

### Authentication & Authorization

- JWT-based authentication
- Role-based access control (RBAC)

### Data Protection

- TLS/SSL encryption
- AES-256 data encryption at rest
- GDPR compliance
- Regular security audits

## Development

### Technical Stack

- Python 3.12+
- FastAPI & Pydantic
- MongoDB
- Amazon SQS
- Docker & AWS ECR
- LangChain
- Azure OpenAI / Groq LLAMA4

### Guidelines

- Follow [Microsoft's REST API Design Guidelines](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design?utm_source=chatgpt.com)
- Use [VSCode Pylint extension](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) with default configuration
- [FastApi Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/)

> [!NOTE]
> Do not forget:
>
> - SOLID Principles: Design your code with these five principles to create robust and scalable software.​
> - DRY (Don't Repeat Yourself): Avoid code duplication to reduce errors and simplify maintenance.​
> - KISS (Keep It Simple, Stupid): Strive for simplicity to enhance readability and reduce complexity.​
> - YAGNI (You Aren't Gonna Need It): Implement only what's necessary to avoid overengineering.​
> - TDD (Test-Driven Development): Write tests before code to ensure functionality and facilitate refactoring.​
> - Comprehensive Documentation: Maintain clear documentation to aid understanding and onboarding.​

> [!TIP]
> 😉 In the era of Generative AI, leveraging tools like GitHub Copilot can significantly enhance productivity. I personally use Cursor—it's a powerful tool that streamlines development workflows.

### Environment Setup

1. **Create Environment**

```bash
conda create -n mockhat-api python=3.12
conda activate mockhat-api
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

3. **Environment Variables**

```bash
cp .env.prod .env
# Configure your .env file with the defined variables
```

4. **Run API**

```bash
python -m app.api
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_assessment.py
```

## Docker Support

### Build

```bash
docker build -t mockhat-ai-api -f ./docker/Dockerfile.api .
docker run -p 8000:8000 --env-file .env mockhat-ai-api
```

### AWS Production Deployment

```bash
# Deploy to production
sh ./scripts/deploy_api.sh
```

### Health Checks

```http
GET /health           # Basic health check
```

## Monitoring

- AWS Cloud Watch

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Submit pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## TODO

- [ ] Improve Testing & Coverage
- [ ] CI/CD Improve (Statics Code Analisis)

## License

Apache License 2.0 - [LICENSE](LICENSE)

## Support

- Email: [d.g.viqueiral@gmail.com](mailto:d.g.viqueiral@gmail.com)
