# Web wallet system

Does not include any authentication

Docker containers developed and adapted for Ubuntu 22.04

### Getting started

```bash
    cp .env.example .env
    make build
    make migrate
    make start
```

Address of swagger API is https://127.0.0.1:8000

### Tests

To run tests, just use Makefile alias command

```bash
    make test
```

