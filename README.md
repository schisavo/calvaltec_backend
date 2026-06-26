# FastAPI Supabase Project

API REST moderna con FastAPI, SQLAlchemy/SQLModel, Alembic, Supabase (PostgreSQL), Authlib (OAuth Google/Microsoft), Pydantic v2 y soporte opcional para Redis y OpenAI.

---

## 🚀 Requisitos previos

- [Python](https://www.python.org/) 3.12.x (recomendado)
- [pyenv](https://github.com/pyenv/pyenv) para gestionar versiones
- [Git](https://git-scm.com/) para sincronizar con GitHub
- Cuenta en [Supabase](https://supabase.com/) para la base de datos
- Cuenta en [Render](https://render.com/) para despliegue

---

## 🛠️ Configuración del entorno

# Instalar Python con `pyenv`:
   ```bash
   pyenv install 3.12.3
   pyenv virtualenv 3.12.3 fastapi-supabase
   pyenv local fastapi-supabase

# Instalar dependencias:
    ```bash
    pip install -r requirements.txt 
    ```

# Instalar dependencias: Crear .env 
    DATABASE_URL=postgresql+psycopg2://usuario:password@host:5432/postgres
    GOOGLE_CLIENT_ID=xxxx
    GOOGLE_CLIENT_SECRET=xxxx
    MICROSOFT_CLIENT_ID=xxxx
    MICROSOFT_CLIENT_SECRET=xxxx
    OPENAI_API_KEY=xxxx
    REDIS_URL=redis://localhost:6379

# 📂 Estructura del proyecto
    app/
    │
    ├── api/              # Rutas y dependencias
    ├── core/             # Configuración, seguridad, OAuth
    ├── models/           # Modelos SQLAlchemy/SQLModel
    ├── schemas/          # Pydantic v2 schemas
    ├── repositories/     # Repositorios de acceso a datos
    ├── services/         # Lógica de negocio
    ├── ai/               # Prompts y cadenas IA
    ├── utils/            # Helpers y constantes
    ├── tests/            # Pruebas
    ├── main.py           # Punto de entrada FastAPI
    │
    alembic/              # Migraciones
    .env                  # Variables de entorno (ignorado)

# Run Project 
    uvicorn app.main:app --reload
