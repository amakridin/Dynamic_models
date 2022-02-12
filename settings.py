# from db.db_data import DbData


class Settings:
    host: str = "0.0.0.0"
    port: int = 8008
    service_name: str = "fastapi_app"
    timeout: int = 2
    # db = DbData("sqlite:///db/crm.db")