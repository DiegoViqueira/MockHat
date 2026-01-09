# 🌐 MockHat WebUI

The front-end application of the MockHat platform, built with Angular. It provides a responsive and intuitive interface for users to submit, review, and manage writing assessments powered by AI.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Security](#security)
- [Development](#development)
- [Docker Support](#docker-support)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [TODO](#todo)
- [License](#license)
- [Support](#support)

---

## Overview

The MockHat WebUI is responsible for the main user interface. It communicates with the MockHat Backend API and provides:

- Secure access to writing evaluations
- Real-time feedback presentation
- Dashboard, history tracking, and plan management
- Multi-language support (i18n)

Built with Angular, it is optimized for performance, accessibility, and scalability.

---

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

- Angular 19
- Angular Material

### Guidelines

- Use [VS Code Prettier ESLint](https://marketplace.visualstudio.com/items?itemName=rvest.vs-code-prettier-eslint) with default configuration
- [Angular Dev Documentation](https://angular.dev)
- [Angular Material Dev Documentation](https://material.angular.io)

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

To setup Angular development environment follow instructions over the following [link](https://hertasecurity.atlassian.net/wiki/spaces/DEVELOPMEN/pages/2143715329/Angular+environment+Setup+for+Development)

2. **Install Dependencies**

   ```bash
   npm install
   ```

3. **Run**
   ```bash
   ng serve
   ```

### Testing

```bash
npm run test
```

### Build

```
npm run build:prod
```

### Translations

Lint translations

```
npx ngx-translate-lint ./src "./src/assets/i18n/*.json" >> test
```

## Deployment

### AWS Production Deployment

```
- aws s3 sync dist/ s3://mockhat/ --delete
- echo "CloudFront Cache Invalidation"
- aws cloudfront create-invalidation --distribution-id E2EOF2864QM65O --paths "/*"
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

- [ ] Improve CI/CD
- [ ] Improve Testing

## License

This project is licensed under the Apache License 2.0 - see [LICENSE](LICENSE) file

## Support

- Email: [d.g.viqueiral@gmail.com](mailto:d.g.viqueiral@gmail.com)
- Issue Tracker: [GitHub Issues](https://github.com/yourusername/mockhat-ai-agent/issues)
