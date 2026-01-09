# 🤖 MockHat AI Agent

The AI Agent is a core component of the MockHat platform, designed to evaluate writing submissions using advanced Large Language Models (LLMs). It performs intelligent analysis, generates CEFR-aligned feedback, and produces comprehensive multi-criteria evaluations in real time.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Development](#development)
- [Docker Support](#docker-support)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [TODO](#todo)
- [License](#license)
- [Support](#support)

---

## Overview

The AI Agent is a core component of the MockHat system, designed to process and evaluate writing assessments through Large Language Models (LLMs). This intelligent system analyzes written content, provides detailed feedback, and generates comprehensive evaluations based on multiple criteria.

## Features

- 🤖 **Automated feedback** generation from writing samples
- 🔄 **Real-time** text analysis and CEFR-level evaluation
- 🎯 **Multi-criteria** scoring (grammar, cohesion, task response, etc.)
- 🔌 **LLM integration** (Azure OpenAI, Groq LLAMA4)
- ⚙️ **Customizable** scoring logic and evaluation weights
- 📊 **Detailed reports** with structured output
- ⚡ **High-performance** asynchronous processing
- 🔐 **Secure** data handling with full compliance (e.g., GDPR)

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

## Development

### Technical Stack

- Python 3.12+
- FastAPI
- Docker
- LangChain
- Large Language Models (LLMs) (Azure OpenAI / Groq LLAMA4)

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

1. **Set up environment**

   ```bash
   conda create -n mockhat-agent python=3.9
   conda activate mockhat-agent
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements.dev.txt
   ```

3. **Run Agent**
   ```bash
   python -m app.agent
   ```

### Testing

```bash
pytest
```

## Docker Support

### Build

```bash
docker build -t mockhat-ai-agent -f ./docker/Dockerfile.agent .
```

### Run Container

```bash
docker run -p 8001:8001 mockhat-ai-agent
```

## Deployment

### Production Deployment

```bash
sh ./scripts/deploy_agent.sh
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)

## TODO

- [ ] RAG Support for retrive similar writings
- [ ] LLM as a judge - Avoid allucinations.
- [ ] Improve Testing & Coverage
- [ ] CI/CD Improve (Statics Code Analisis)

## License

This project is licensed under the MockHat License - see [LICENSE](LICENSE) file

## Support

- Email: [d.g.viqueiral@gmail.com](mailto:d.g.viqueiral@gmail.com)
- Issue Tracker: [GitHub Issues](https://github.com/yourusername/mockhat-ai-agent/issues)
