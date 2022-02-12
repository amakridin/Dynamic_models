import uvicorn
from settings import Settings
from fastapi import FastAPI
from routes import router
from models import Models


if __name__ == "__main__":
    Models.load_models()
    settings = Settings()
    app = FastAPI(title=settings.service_name)
    app.state.__setattr__("settings", settings)
    app.include_router(router)
    uvicorn.run(app=app,
                port=settings.port,
                access_log=True,
                host=settings.host)
