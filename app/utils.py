from pathlib import Path
import json

import aiohttp
import asyncio
import aiohttp.client_exceptions
from fastapi import HTTPException, status, Request
from loguru import logger

from modules.waf.service import WAF
from modules.service_a.schemas import RequestData

async def post_request(url: str, data: dict):
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.post(url=url,
                                        data=json.dumps(data),
                                        headers={"Content-Type": "application/json"})
            response.raise_for_status()
        except aiohttp.ClientConnectionError as e:
            logger.error("Ошибка подключения")
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Сервис недоступен")
        except aiohttp.client_exceptions.ClientResponseError as e:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Данные не валидны!")

model_path = Path(__file__).parent.parent.joinpath("app").joinpath("modules").joinpath("waf").joinpath("waf_model.sav").__str__() 
waf = WAF(model_path)

async def check_waf(request_data: RequestData, request: Request):
    payload = request_data.model_dump().values()
    
    if not all(waf.waf_check(payload)):
        logger.error(
            f"Клиент: {request.client.host}:{request.client.port} - потенциальный злоумышленник!"
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверка WAF: Обнаружена потенциальная атака!")
    return request_data.model_dump()
