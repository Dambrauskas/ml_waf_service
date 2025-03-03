from fastapi import (APIRouter, HTTPException, Depends, status, Request)
from fastapi.responses import JSONResponse
from loguru import logger

from settings import settings
from modules.service_a.schemas import RequestData
from utils import post_request, check_waf

router = APIRouter(prefix="/service_a", tags=["Сервис А"], responses={404: {"description": "Not found"}})

@router.post("/create_request")
async def create_request(request_data: RequestData = Depends(check_waf)):
    try:
        logger.debug(request_data)
        _ = await post_request(f"{settings.SERVICE_A_URL}/create_request", request_data)
    except Exception as e:
        raise e
    return JSONResponse("Заявка создана!", status.HTTP_200_OK)
    
