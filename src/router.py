import aiohttp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import IMEI_API_TOKEN, IEMI_API_URL
from src.models import User
from src.auth import current_user


router = APIRouter(
    prefix="/api",
    tags=["API"]
)


async def check_imei_valid(imei: str):
    """Функция отправляет IMEI на проверку в imeicheck.net"""
    print("Проверка")
    data = {
        "deviceId": imei,
        "serviceId": 12
    }
    print(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            IEMI_API_URL,
            json=data,
            headers={
                "Authorization": f"Bearer {IMEI_API_TOKEN}",
                "Accept-Language": "en",
                "Content-Type": "application/json"
            },
        ) as response:
            if response.status == 201:
                print("Проверка выполнена")
                response_data = await response.json()
                return {
                    "status": response_data.get("status"),
                    "deviceName": response_data.get("properties", {}).get("deviceName"),
                    "warrantyStatus": response_data.get("properties", {}).get("warrantyStatus"),
                    "simLock": response_data.get("properties", {}).get("simLock"),
                    "fmiOn": response_data.get("properties", {}).get("fmiOn"),
                    "lostMode": response_data.get("properties", {}).get("lostMode"),
                    "purchaseCountry": response_data.get("properties", {}).get("purchaseCountry"),
                }
            else:
                print("Проверка не выполнена")
                print(IMEI_API_TOKEN)
                print(response.text)
                raise HTTPException(status_code=response.status, detail="Ошибка при проверке IMEI")


@router.post("/check-imei")
async def check_imei(
    imei: str,
    current_user: User = Depends(current_user),
):
    print(f"Received token: {current_user}")
    if not current_user:
        print("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")

    imei_info = await check_imei_valid(imei)
    if not imei_info:
        raise HTTPException(status_code=400, detail="Invalid IMEI format")

    return imei_info
