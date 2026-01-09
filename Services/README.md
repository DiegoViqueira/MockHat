# Mockhat Services

Backend services powering the MockHat AI writing evaluation platform — includes the API, AI Agents, and Payment processing.

## 📚 Table of Contents

- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [Modules Documentation](#modules-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This package contains all backend service modules required by the MockHat platform:

- **Agent**: AI Agent responsible for evaluating and processing writing submissions.
- **API**: RESTful API used to communicate between the platform frontend and backend services.
- **Payments**: Integrations and services for handling Stripe-based payment workflows.

## Folder Structure

```
.
├── app/                   # Main application directory
│   ├── agents/            # Logic for agents handling tasks
│   ├── chains/            # Processing chains and workflows
│   ├── core/              # Core functionalities and utilities
│   ├── databases/         # Database-related modules
│   ├── enums/             # Enumerations used across the application
│   ├── events/            # Event-based processing modules
│   ├── factories/         # Factory methods for creating objects
│   ├── handlers/          # Request and response handlers
│   ├── loggers/           # Logging configuration and utilities
│   ├── middlewares/       # Middleware for request processing
│   ├── models/            # Data models and schemas
│   ├── queue/             # Queue management for asynchronous tasks
│   ├── routes/            # API route definitions
│   ├── services/          # Business logic and services
│   ├── agent.py           # Main agent logic
│   ├── api.py             # API entry point
│   ├── payments.py        # Payment processing module
│
├── config/                # Configuration files
├── docs/                  # Documentation files
├── pocs/                  # PoC (Agentic)
├── docker/                # Docker-related files
├── scripts/               # Utility scripts
├── tests/                 # Unit and integration tests
├── tools/                 # Helper tools and utilities
├── .gitignore             # Git ignore rules
├── pytest.ini             # Pytest configuration
├── README.md              # Project documentation
├── requirements.dev.txt   # Development dependencies
├── requirements.txt       # Project dependencies
```

## Modules Documentation

Explore more details in the dedicated module documentation:

- [API](./docs/README_API.MD)
- [Agent](./docs/README_AGENT.MD)
- [Payments](./docs/README_PAYMENTS.MD)

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m 'Add your feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Open a pull request.

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [d.g.viqueiral@gmail.com](mailto:d.g.viqueiral@gmail.com).
