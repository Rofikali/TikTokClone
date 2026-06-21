# PostgreSQL Setup for Django (Without Docker)

This guide explains how to install, configure, and connect PostgreSQL to a Django project running in GitHub Codespaces or a Linux environment without Docker.

---

## 1. Check if PostgreSQL Is Installed

```bash
psql --version
```

If you see:

```text
command not found
```

install PostgreSQL:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

---

## 2. Start PostgreSQL

Start the PostgreSQL service:

```bash
sudo service postgresql start
```

Verify that PostgreSQL is running:

```bash
sudo service postgresql status
```

Expected output:

```text
active (running)
```

---

## 3. Create Database and User

Open PostgreSQL as the postgres superuser:

```bash
sudo -u postgres psql
if error
    sudo service postgresql status
    sudo service postgresql start

    sudo su postgres
    psql
```

Create the database and user:

```sql
CREATE DATABASE tiktokapi;

CREATE USER admin WITH PASSWORD 'admin';

ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE tiktokapi TO admin;
```

Exit PostgreSQL:

```sql
\q
```

---

## 4. Test the Connection

Verify that the new user can connect:

```bash
psql -h localhost -U admin -d tiktokapi
```

Password:

```text
admin
```

Successful connection:

```text
tiktokapi=>
```

Exit:

```sql
\q
```

---

## 5. Install PostgreSQL Driver for Django

Install Psycopg:

```bash
pip install "psycopg[binary]"
```

Verify installation:

```bash
pip freeze | grep psycopg
```

Expected:

```text
psycopg==3.x.x
```

---

## 6. Configure Django

In `settings/prod.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "tiktokapi",
        "USER": "admin",
        "PASSWORD": "admin",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


```

---

## 7. Run Migrations

```bash
ENVIRONMENT=production python manage.py migrate
```

Create a superuser:

```bash
ENVIRONMENT=production python manage.py createsuperuser
```

---

## 8. Start the Django Server

```bash
ENVIRONMENT=production python manage.py runserver
```

Expected output:

```text
Starting development server at http://127.0.0.1:8000/
```

---

## Troubleshooting

### Error: psycopg module not found

Install Psycopg:

```bash
pip install "psycopg[binary]"
```

---

### Error: connection refused

Check if PostgreSQL is running:

```bash
sudo service postgresql status
```

Start it if necessary:

```bash
sudo service postgresql start
```

---

### Error: database does not exist

Connect as postgres:

```bash
sudo -u postgres psql
```

List databases:

```sql
\l
```

Create the database if missing:

```sql
CREATE DATABASE tiktokapi;
```

---

### Verify PostgreSQL Is Listening on Port 5432

```bash
pg_isready
```

Expected:

```text
accepting connections
```

---

## Useful Commands

Check PostgreSQL version:

```bash
psql --version
```

List databases:

```bash
sudo -u postgres psql -c "\l"
```

List users:

```bash
sudo -u postgres psql -c "\du"
```

Connect manually:

```bash
psql -h localhost -U admin -d tiktokapi
```
