## Server Configuration

Development:
Uvicorn (with --reload)

Production (Docker):
Gunicorn with Uvicorn workers
## Server Configuration

Development:
Uvicorn (with --reload)

Production (Docker):
Gunicorn with Uvicorn workers

## 
Project structure

```
moj_pro_api/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
│
├── src/
│ ├── main.py
│ ├── app.py
│ ├── database.py
│ │
│ ├── models/
│ │ ├── user.py
│ │ └── sort_enums.py
│ │
│ ├── routers/
│ │ └── users.py
│ │
│ ├── services/
│ │ ├── auth_service.py
│ │ ├── user_service.py
│ │ └── logger.py
│ │
│ └── middleware/
│ └── metrics.py
│
└── users.json
```

