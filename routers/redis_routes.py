from fastapi import APIRouter, HTTPException
from operations.redis_operations import set_value, get_value, delete_value

router = APIRouter()

@router.post("/set/{key}/{value}")
async def set_value_route(key: str, value: str):
    if set_value(key, value):
        return {"message": f"Key '{key}' set to '{value}'"}
    else:
        raise HTTPException(status_code=500, detail="Failed to set value")

@router.get("/get/{key}")
async def get_value_route(key: str):
    value = get_value(key)
    if value is not None:
        return {"key": key, "value": value}
    else:
        raise HTTPException(status_code=404, detail="Key not found")

@router.delete("/delete/{key}")
async def delete_value_route(key: str):
    if delete_value(key):
        return {"message": f"Key '{key}' deleted"}
    else:
        raise HTTPException(status_code=404, detail="Key not found or failed to delete")
