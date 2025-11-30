# Django Billing System

This project provides a simple billing application built with Django.  
You can run it in three ways:

1. Directly on your local machine (no Docker)  
2. Using a Docker container  
3. Using Docker Compose for a full environment (Django + database)

Pick whatever fits your setup.

---

## 1. Running Locally (Without Docker)

### Prerequisites
- Python 3.10 or higher  
- pip  
- virtualenv (optional, but recommended)  
- PostgreSQL or SQLite (if you're not using Postgres, Django will default to SQLite)

### Steps

#### 1. Clone the project
```sh
git clone <repo-url>
cd billing_system/billing_system
```

#### 2. Create and activate a virtual environment
```sh
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install dependencies
```sh
pip install -r requirements.txt
```

#### 4. Run migrations
```sh
python manage.py migrate
```

#### 5. (Optional) Load seed data
```sh
# if there is no test data in the db.sqlite3 to pull product and denominations data
python manage.py seed_data
```

#### 6. Start the development server
```sh
python mamange.py runserver
```

The app will be available at:
```cpp
http://127.0.0.1:8000/
```


## 2. Running with Docker

This approach builds and runs the Django application inside a Docker container.

### Prerequisites
- Docker installed on your machine

### Steps

#### 1. Build the image
```sh
git clone <repo-url>
cd billing_system
docker build -t billing_app:latest .
```

#### 2. Run the container
```sh
docker run --name billing_app -p 8000:8000 billing_app:latest
```

The app will be available at:
```cpp
http://localhost:8000/
```

> [!IMPORTANT] 
> Ensure to seed data before docker build.

## 3. Running with Docker Compose (Recommended)

### Prerequisites
- Docker
- Docker Compose

### Steps

#### 1. Start Service
```sh
docker compose up --build
```

This will:
- Build the Django app
- Start a Postgres container (if configured)
- Run migrations automatically (if included in your compose commands)

The app will be available at:
```cpp
http://localhost:8000/
```

#### 2. Stopping the service
```sh
docker compose down
```

#### 3. View logs
```sh
docker compose logs -f
```

> [!IMPORTANT] 
> Ensure to seed data before docker build.

## 4. Folder Structure

```sh
.
├── billing_system
│   ├── billing
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── management
│   │   │   └── commands
│   │   │       └── seed_data.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── templates
│   │   │   └── billing
│   │   │       ├── billing_page.html
│   │   │       ├── invoice.html
│   │   │       ├── purchase_detail.html
│   │   │       └── purchase_list.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── billing_system
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3
│   └── manage.py
├── docker-compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt
```