# 💳 MockHat Payments Gateway

A secure, scalable payment processing service powering all financial transactions for the MockHat platform. Built on Stripe, it supports robust subscription management, real-time financial reporting, and enterprise-grade security.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [Specifications](#specifications)
- [Pricing Tiers](#pricing-tiers)
- [Security](#security)
- [Development](#development)
- [Docker Support](#docker-support)
- [Deployment](#deployment)
- [Webhook Integration](#webhook-integration)
- [Contributing](#contributing)
- [TODO](#todo)
- [License](#license)
- [Support](#support)

---

## Overview

MockHat Payments Gateway is a secure payment processing service that handles all financial transactions for the MockHat platform. Built with Stripe integration, it provides robust payment processing, subscription management, and financial reporting capabilities.

- Built with **FastAPI** and **Stripe API v2023-10-16**
- Supports **subscription tiers** and **payment webhooks**
- Designed for **scale**, **security**, and **observability**

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

## Specifications

### Base URLs

- Development: `http://localhost:8002/`
- Production: `https://payments.mockhat.ai/`

### API Documentation

- Swagger UI: `/docs`
- OpenAPI Spec: `/openapi.json`

## Pricing Tiers

| Tier           | Features                                   | Support           |
| -------------- | ------------------------------------------ | ----------------- |
| **Free**       | 50 assessments/month, Basic features       | Community support |
| **Pro**        | 100 assessments/month, Advanced features   | Priority support  |
| **Enterprise** | Custom usage, SLA guarantees, Integrations | Dedicated support |

## Security

### Authentication

- API key authentication
- Stripe webhook signatures
- Rate limiting protection

### Compliance

- PCI DSS compliance
- GDPR compliance
- SOC 2 Type II certified
- Regular security audits

### Data Protection

- End-to-end encryption
- Tokenization of sensitive data

## Development

### Technical Stack

- Python 3.12+
- FastAPI & Pydantic
- Stripe API v2023-10-16
- MongoDB Atlas
- Docker & AWS ECR

### Guidelines

- Follow [Microsoft's REST API Design Guidelines](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design?utm_source=chatgpt.com)
- Use [VSCode Pylint extension](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) with default configuration
- [FastApi Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/)
- [Stripe Dev Documentation](https://docs.stripe.com/)
- [Stripe cli reference](https://docs.stripe.com/cli)

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

1. **Create Development Environment**

```bash
conda create -n mockhat-payments python=3.12
conda activate mockhat-payments
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

3. **Configure Environment Variables**

```bash
cp .env.example .env
```

4. **Start Development Server**

```bash
python -m app.payments
```

### Stripe development setup

1. **Login**

```
stripe login
```

2. **Run**

```
stripe listen --api-key sk_test_xxxxxxxxxxxxxxxxxxxxxx
```

### Testing

```bash
# Unit tests
pytest tests/unit

# Coverage report
pytest --cov=app --cov-report=html
```

## Docker Support

### Build

```bash
docker build -t mockhat-payments -f ./docker/Dockerfile.payments .
docker run -p 8002:8002 --env-file .env.prod mockhat-payments
```

## Deployment

### AWS Deployment

```bash
# Build and push to ECR
sh ./scripts/build_and_push.sh

# Deploy to ECS
sh ./scripts/deploy_payments.sh
```

### Monitoring

- AWS CloudWatch metrics
- Stripe Dashboard integration
- Payment success rates
- Transaction volumes
- Error tracking
- Performance metrics

### Health Checks

```http
GET /health           # Basic health check
GET /health/detailed  # System component status
```

## Webhook Integration

```bash
# Local webhook testing
stripe listen --forward-to localhost:8002/webhook

# Webhook endpoints
POST /webhook/stripe    # Stripe events
POST /webhook/internal  # Internal events
```

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/payment-feature`
3. Commit changes: `git commit -m 'Add payment feature'`
4. Push branch: `git push origin feature/payment-feature`
5. Submit pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## TODO

- [ ] Testing & Coverage
- [ ] CI/CD
- [ ] Deploy to production
- [ ] Finalize integration with MockHat Core API
- [ ] Add billing portal support

## License

MockHat License - [LICENSE](LICENSE)

## Support

- Technical Support: [d.g.viqueiral@gmail.com](mailto:d.g.viqueiral@gmail.com)
- Stripe Dashboard: [dashboard.stripe.com](https://dashboard.stripe.com)
