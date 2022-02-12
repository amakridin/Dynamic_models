from fastapi import APIRouter, Header, HTTPException, Request
from types_validator import Pong, CheckModel, ModelsList, ModelParams
from models import Models
from urllib.parse import parse_qsl
from pydantic import ValidationError
import json

X_AUTH_TOKEN = "test"


async def verify_token(x_auth_token: str = Header(...)):
    if x_auth_token != X_AUTH_TOKEN:
        raise HTTPException(status_code=400, detail="X-Auth-Token header invalid")

# router = APIRouter(prefix="/api", dependencies=[Depends(verify_token)])
router = APIRouter(prefix="/api")


@router.get("/ping", response_model=Pong)
async def ping() -> Pong:
    return Pong()


@router.get("/dynamic_models/check_model/{model_name}", response_model=CheckModel)
async def check_model(model_name: str):
    return await Models.check_model(model_name)


@router.get("/dynamic_models/list", response_model=ModelsList)
async def check_model():
    return await Models.get_model_list()


@router.get("/dynamic_models/{model_name}")
async def dynamic_models(request: Request, model_name: str):
    check_result = await Models.check_model(model_name)
    if check_result:
        params = request.query_params
        dict_params = dict(parse_qsl(str(params)))
        try:
            result = Models.models[model_name](**dict_params)
            return result
        except ValidationError as ex:
            return {"ValidationError": ex.errors()}
    return


@router.post("/dynamic_models/load_model")
async def dynamic_models(request: Request):
    model_params = await request.body()
    return Models.load_model(ModelParams(**json.loads(model_params.decode())))
