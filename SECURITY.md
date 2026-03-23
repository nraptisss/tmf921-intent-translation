# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within TMF921 Intent Translator, please follow responsible disclosure:

1. **Do NOT** create a public GitHub issue for security vulnerabilities
2. Send details privately to the maintainers via:
   - Email: security@example.com (placeholder)
   - Or contact through GitHub's private vulnerability reporting

Please include the following information:
- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue including how it could be exploited

## Security Best Practices

When using this system:

1. **API Security**: If deploying the backend API, use HTTPS and implement authentication
2. **Input Validation**: All NL inputs are sanitized before processing
3. **Data Privacy**: No user data is stored or logged
4. **Dependencies**: Keep dependencies updated to latest secure versions

## Known Security Considerations

1. **LLM Integration**: When connecting to external LLM APIs, ensure API keys are stored securely (environment variables, secrets management)
2. **Rate Limiting**: Implement rate limiting for production deployments
3. **CORS**: Configure CORS appropriately for cross-origin requests
4. **Input Length**: Maximum input length enforced to prevent DoS

## Security Updates

Security updates will be released as patch versions and announced through:
- GitHub Security Advisories
- Release notes

Thank you for helping keep TMF921 Intent Translator secure!
