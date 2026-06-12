from fastapi import FastAPI

from lab_security.audit import security_checks
from lab_security.settings import settings

app = FastAPI(title="Lab Security")


@app.get("/")
def root():
    return {
        "message": "Lab de seguridad y mantenimiento",
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "debug": settings.debug,
    }


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.app_env}


@app.get("/security")
def security():
    return security_checks()
