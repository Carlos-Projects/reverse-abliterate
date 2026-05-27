# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in reverse-abliterate, please report it privately.

**Do not** open a public GitHub issue. Instead, email **Carlos@AIAgentObservatory.org** or use GitHub's [private vulnerability reporting](https://github.com/Carlos-Projects/reverse-abliterate/security/advisories/new).

Please include:
- Description of the vulnerability
- Steps to reproduce
- Affected version(s)
- Potential impact

## Response Timeline

- **24h**: Acknowledgment of receipt
- **7 days**: Initial assessment and fix timeline
- **30 days**: Patch release (for validated issues)

## Scope

reverse-abliterate is a CLI tool that scans local model directories. Vulnerabilities include:
- Path traversal via crafted model paths
- Code injection through model metadata
- Unsafe deserialization of model configs
- Integrity bypass in weight verification

## Supported Versions

| Version | Supported |
|---------|-----------|
| >= 0.1.0 | ✅ |

## Safe Usage

- Only scan models from trusted sources
- Verify weight manifests before loading models
- Run `reverse-abliterate harden` on production models
