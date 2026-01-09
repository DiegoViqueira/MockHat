# MochHat

## 📚 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Folder Structure](#folder-structure)
- [AI Engineering](#ai-engineering)
- [Sub Projects Documentation](#sub-projects-documentation)
- [Infrastructure](#infrastructure)
- [Development](#development)
- [TODO](#todo)
- [License](#license)
- [Contact](#contact)

## Overview

### AI-Powered English Writing Assessment

MockHat streamlines the evaluation of Cambridge English writing tasks using advanced AI. Whether it’s essays, emails, articles, or other assignment types, MockHat delivers fast, consistent, and level-specific feedback across B1 to C1 proficiency levels—aligned with Cambridge standards.

### Key Features

- **Effortless Evaluation**: Instantly assess a wide range of writing formats with feedback tailored to the CEFR levels (B1–C1).
- **Handwriting Recognition**: Accurately transcribes handwritten submissions, preserving spelling and grammar mistakes to reflect students’ true proficiency.
- **Time-Saving**: Say goodbye to manual corrections—MockHat’s AI handles the heavy lifting, so you can focus on teaching.

## Achitecture

![Architecture](docs/MockhatArchitecture.webp)

## Folder structure

```
MochHat/
├── Anotation/   # Contains scripts and tools for data annotation and labeling
├── App/         # Movile App (IN PROGRESS) Angular/Ionic
├── Docs/        # Contains Documentation
├── Frontend/    # MockHat Angular FrontEnd
├── Landing/     # MockHat Angular Landing Page
├── Notebooks/   # Reserverd for Notebooks (DEPRECATED)
├── Services/    # BackEnd Services ( API, AI Agents, Payments)
└── README.md
```

## AI Engineering

- [Documentation](docs/README_AI.MD)

## Sub Projects Documentation

- [Backend Services](Services/README.md)
- [Frontend](frontend/README.md)
- [Landing Page](Landing/README.md) - Landsay buyed template ( Adapted by MockHat)
- Notebooks were moved to [LangSmith](https://smith.langchain.com/) for better collaboration

## Infrastructure

| Resource            | Provider | Owner          | Description                                                     |
| ------------------- | -------- | -------------- | --------------------------------------------------------------- |
| Source Code Hosting | GitHub   | Diego Viqueira | Version control and collaboration platform                      |
| Web Application     | AWS      | Diego Viqueira | Hosted on AWS EC2 instances                                     |
| API Service         | AWS      | Diego Viqueira | RESTful API hosted on AWS EC2                                   |
| AI Agent            | AWS      | Diego Viqueira | LLM-based agent hosted on AWS EC2                               |
| Domain Management   | AWS      | Diego Viqueira | Managed via AWS Route 53                                        |
| Database            | MongoDB  | Diego Viqueira | Managed NoSQL database via MongoDB Atlas                        |
| CI/CD Pipeline      | TODO     | TODO           | Automated deployments via GitHub Actions                        |
| LLM Models (Azure)  | Azure    | Juan Bau       | Azure OpenAI Service with GPT-4o and GPT-4 Turbo models         |
| LLM Models (Groq)   | Groq     | Juan Bau       | Meta's LLaMA 4 Scout and Maverick models hosted on GroqCloud™   |
| Email Service       | Gmail    | Juan Bau       | Managed email service via Gmail                                 |
| Analytics Platform  | Google   | Diego Viqueira | Website traffic and user behavior tracking via Google Analytics |
| Payment Processing  | Stripe   | Diego Viqueira | Online payment processing platform facilitating transactions    |

## Development

### Agile Methodology

We follow the **Scrum** framework to manage our development process, ensuring iterative progress and continuous improvement.

### Roles

- **Product Owner (PO)**: Defines product features and priorities.
- **Scrum Master (SM)**: Facilitates Scrum practices and removes impediments.
- **Development Team**: Cross-functional group responsible for delivering increments.

### Events

- **Sprint Planning**: Define the work for the upcoming sprint.
- **Daily Stand-up**: Short daily meeting to synchronize activities.
- **Sprint Review**: Demonstrate completed work to stakeholders.
- **Sprint Retrospective**: Reflect on the sprint to identify improvements.

### Definition of Done (DoD)

Our Definition of Done ensures that each increment meets our quality standards before release.

- [x] Code has been written and committed.
- [x] Unit and integration tests have been written and passed.
- [x] Static code analysis has been passed.
- [x] Documentation has been updated accordingly.
- [x] No critical bugs are present.
- [x] Product Owner has approved the feature.

## TODO

- [ ] CI/CD Testing
- [ ] CI/CD Static code analysis

## License

This project is licensed under the MockHat License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [d.g.viqueiral@gmail.com](mailto:d.g.viqueiral@gmail.com).
