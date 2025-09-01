# NTLM Authorization Proxy Server (NTLMAPS) - Python 3 Edition

**Author:** Fabian Boni  
**Original NTLMAPS by:** Dmitry Rozmanov and contributors  
**Version:** 0.9.9-py3  
**License:** GPL  

## Overview

NTLMAPS is a proxy server that translates between NTLM and Basic authentication protocols. This Python 3 modernized version enables Unix/Linux systems to seamlessly access corporate networks that require NTLM authentication through Microsoft proxy servers.

## Use Case

Many enterprise environments use Microsoft ISA Server, TMG, or other Windows-based proxy servers that require NTLM authentication. Unix/Linux systems and applications typically only support Basic authentication, creating a compatibility gap. NTLMAPS bridges this gap by:

1. **Receiving Basic authentication** from Unix/Linux clients (curl, yum, wget, etc.)
2. **Translating to NTLM authentication** with the upstream Windows proxy server
3. **Proxying the connection** transparently

This enables:
- ✅ **Package managers** (yum, dnf, apt, pip, npm) to work through corporate proxies
- ✅ **Development tools** (git, curl, wget) to access external resources
- ✅ **Automated scripts** and CI/CD pipelines to function in corporate environments
- ✅ **Linux servers** to receive security updates through corporate firewalls

## What's New in Python 3 Edition

This version includes comprehensive modernization and improvements:

### Python 3 Compatibility
- **Complete Python 2 → 3 migration**: Updated all code for Python 3.6+ compatibility
- **Import modernization**: Updated `thread` → `_thread`, `httplib` → `http.client`, `urlparse` → `urllib.parse`
- **String handling**: Fixed bytes/string handling with proper encoding (latin-1 for HTTP)
- **Dictionary methods**: Replaced deprecated `has_key()` with `in` operator
- **Exception handling**: Updated exception syntax and handling
- **Print statements**: Converted to print functions

### Enhanced NTLM Authentication
- **Improved NTLM message handling**: Fixed bytes/string concatenation in message creation
- **Both LM and NT authentication**: Enabled both authentication methods for better compatibility
- **Proper domain parsing**: Correctly separates username and domain from Basic auth credentials
- **Enhanced debugging**: Detailed NTLM handshake logging for troubleshooting

### Security and Reliability
- **Systemd service support**: Includes automated setup script for production deployment
- **Security hardening**: Runs as non-root user with restricted permissions
- **Log rotation**: Automatic log management
- **Firewall integration**: Optional firewall rule setup
- **Service management**: Standard systemctl commands for operation

### Configuration Improvements
- **Environment variable support**: Easy configuration through environment variables
- **Automated setup**: One-command installation script
- **Flexible deployment**: Customizable user, directories, and ports
- **Production ready**: Suitable for enterprise deployment

## Quick Start

### Prerequisites
- Python 3.6 or higher
- Root access for service installation (optional)

### Basic Usage

1. **Configure the proxy** (edit `server.cfg`):
```ini
[GENERAL]
LISTEN_PORT:5865
PARENT_PROXY:proxy.company.com
PARENT_PROXY_PORT:3128

[NTLM_AUTH]
NT_DOMAIN:company.com
NTLM_TO_BASIC:1
```

2. **Run manually**:
```bash
python3 main.py
```

3. **Configure clients**:
```bash
export http_proxy=http://username:password@localhost:5865/
export https_proxy=http://username:password@localhost:5865/
```

### Production Installation

Use the automated setup script for production deployment:

```bash
# Basic installation
sudo ./setup-ntlmaps.sh

# Custom configuration
sudo NTLM_PORT=8080 \
     PARENT_PROXY=proxy.company.com \
     NT_DOMAIN=company.com \
     ./setup-ntlmaps.sh
```

This creates a systemd service that:
- Runs automatically on boot
- Restarts on failure
- Logs to journald
- Runs securely as non-root user

## Service Management

After installation, manage the service with:

```bash
# Start/stop/restart
sudo systemctl start ntlmaps
sudo systemctl stop ntlmaps
sudo systemctl restart ntlmaps

# Enable/disable auto-start
sudo systemctl enable ntlmaps
sudo systemctl disable ntlmaps

# Check status and logs
sudo systemctl status ntlmaps
sudo journalctl -u ntlmaps -f
```

## Configuration Reference

### Key Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `LISTEN_PORT` | Port for NTLMAPS to listen on | `5865` |
| `PARENT_PROXY` | Upstream Windows proxy server | `proxy.company.com` |
| `PARENT_PROXY_PORT` | Upstream proxy port | `3128` |
| `NT_DOMAIN` | Windows domain name | `company.com` |
| `NTLM_TO_BASIC` | Enable Basic→NTLM translation | `1` |
| `DEBUG` | Enable debug logging | `1` |
| `AUTH_DEBUG` | Enable detailed NTLM auth logging | `1` |

### Authentication Flow

1. Client sends HTTP request with Basic auth: `username:password`
2. NTLMAPS extracts credentials and splits username/domain
3. NTLMAPS performs NTLM handshake with upstream proxy:
   - Message 1: Negotiation
   - Message 2: Challenge (receives nonce)
   - Message 3: Authentication (sends credentials)
4. Upstream proxy accepts NTLM auth and proxies request
5. NTLMAPS forwards response back to client

## Testing

Verify the proxy works with common tools:

```bash
# Test with curl
curl -v --proxy-user username@domain.com:password http://example.com

# Test with yum/dnf
yum check-update

# Test with wget
wget --proxy-user=username@domain.com --proxy-password=password http://example.com

# Test with pip
pip install --proxy http://username:password@localhost:5865 package_name
```

## Troubleshooting

### Common Issues

1. **Authentication failures**: 
   - Verify domain name format (`company.com` not `COMPANY`)
   - Check username format (`user@domain.com` or `DOMAIN\user`)
   - Ensure password is correct

2. **Connection issues**:
   - Verify upstream proxy address and port
   - Check firewall rules
   - Ensure NTLMAPS is listening on correct port

3. **Service startup issues**:
   - Check user/group permissions
   - Verify Python 3 is installed
   - Review systemd logs: `journalctl -u ntlmaps`

### Debug Logging

Enable detailed logging in `server.cfg`:
```ini
[DEBUG]
DEBUG:1
AUTH_DEBUG:1
```

View logs:
```bash
# Service logs
sudo journalctl -u ntlmaps -f

# Manual run with console output
python3 main.py
```

## Architecture

```
Linux Client (Basic Auth) → NTLMAPS → Windows Proxy (NTLM) → Internet
     ↓                        ↓              ↓
curl/yum/wget            Translates      ISA/TMG/etc
username:password        Basic→NTLM      NTLM Auth
```

## Changelog

### Version 0.9.9-py3 (2025)
- **BREAKING**: Requires Python 3.6+
- Complete Python 3 compatibility overhaul
- Enhanced NTLM authentication with LM+NT support
- Systemd service integration with setup script
- Security hardening and production deployment features
- Improved debugging and error handling
- Fixed bytes/string handling throughout codebase

### Previous Versions
See `changelog.txt` for complete version history.

## Contributing

This is a modernization of the original NTLMAPS project. Contributions welcome for:
- Bug fixes and improvements
- Additional authentication methods
- Enhanced security features
- Documentation improvements

## License

GPL - Same as original NTLMAPS

## Support

For issues with this Python 3 version, please provide:
- Python version (`python3 --version`)
- Operating system and version
- Configuration file (redacted)
- Debug logs showing the issue
- Steps to reproduce

## Acknowledgments

- **Original NTLMAPS team**: Dmitry Rozmanov and all contributors who created this essential tool
- **Community**: Users who kept this project alive and identified Python 3 compatibility needs
- **Enterprise users**: Organizations who need this bridge between Unix and Windows authentication

---

*This Python 3 modernization ensures NTLMAPS continues to serve enterprise environments in the modern era.*