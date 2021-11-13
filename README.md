# Backend

### Development

1. Install dependencies

```bash
cd netomerch
pip install -r requirements-dev.txt
```

2. Make `.env` file (you can make it based on `.env.template`)

```bash
cp .env.template .env
```

3. Please make sure to check the code before pushing

```bash
isort .
flake8 .
pytest
```

*NB*: tests use PostgreSQL, so you need to allow user to create the database:

```bash
psql -U postgres -c "ALTER USER netomerch CREATEDB;"
```
