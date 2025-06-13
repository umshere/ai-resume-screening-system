# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.4.x   | :white_check_mark: |
| 0.3.x   | :white_check_mark: |
| < 0.3   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in the AI Resume Screening System, please follow these steps:

### 🔒 Responsible Disclosure

1. **Do NOT** create a public GitHub issue for security vulnerabilities
2. **Email** security details to the project maintainers
3. **Include** detailed information about the vulnerability
4. **Allow** reasonable time for the issue to be resolved before public disclosure

### 📧 Contact Information

For security issues, please contact:

- **Email**: [Your email or create a security contact]
- **Response Time**: We aim to respond within 48 hours

### 🛡️ Security Best Practices

When deploying this system:

#### Environment Variables

- ✅ **Never commit `.env` files** with real API keys
- ✅ **Use environment variables** in production
- ✅ **Rotate API keys** regularly
- ✅ **Use least-privilege** access for API keys

#### Deployment Security

- ✅ **Enable HTTPS** for all production deployments
- ✅ **Set upload file size limits** to prevent abuse
- ✅ **Monitor API usage** to detect anomalies
- ✅ **Use secure headers** (HSTS, CSP, etc.)

#### Data Privacy

- ✅ **Process resume data** only in memory
- ✅ **No persistent storage** of uploaded files
- ✅ **Clear temporary files** after processing
- ✅ **Comply with data protection** regulations (GDPR, CCPA, etc.)

### 🔍 Security Considerations

#### API Keys Security

- **Gemini API**: Store securely, monitor usage quotas
- **Azure OpenAI**: Use managed identities when possible
- **OpenAI**: Enable usage monitoring and alerts

#### File Upload Security

- **File Type Validation**: Only PDF, DOCX, TXT allowed
- **File Size Limits**: Configured to prevent DoS attacks
- **Content Scanning**: Files processed safely without execution

#### Network Security

- **HTTPS Only**: All API communications encrypted
- **CORS Configuration**: Properly configured for production
- **Rate Limiting**: Implemented to prevent abuse

### 🚨 Known Security Considerations

1. **AI Model Outputs**: AI responses should be validated before display
2. **File Processing**: Large files may consume significant memory
3. **API Rate Limits**: Implement client-side rate limiting
4. **Error Messages**: Ensure sensitive information isn't exposed in errors

### 📋 Security Checklist for Deployment

Before deploying to production:

- [ ] API keys are stored as environment variables
- [ ] HTTPS is enabled and enforced
- [ ] File upload limits are configured
- [ ] Error handling doesn't expose sensitive information
- [ ] API usage monitoring is enabled
- [ ] Logs don't contain sensitive data
- [ ] Regular security updates are scheduled

### 🔄 Update Policy

- **Critical Security Issues**: Patched within 24-48 hours
- **High Priority Issues**: Patched within 1 week
- **Medium Priority Issues**: Included in next minor release
- **Low Priority Issues**: Included in next major release

### 🛠️ Security Tools

We recommend using these tools for security monitoring:

- **Dependabot**: Automated dependency updates
- **CodeQL**: Static security analysis
- **OWASP ZAP**: Web application security testing
- **Snyk**: Vulnerability scanning

### 📞 Support

For security-related questions or concerns:

- Check our [Security Policy](SECURITY.md)
- Review [Deployment Guide](DEPLOYMENT.md)
- Contact the development team

---

**Note**: This is an open-source project for educational purposes. Users are responsible for ensuring their deployments meet their organization's security requirements.
