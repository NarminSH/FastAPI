from fastapi import APIRouter


router_tasks = APIRouter(
    prefix= "/api/v1/task",
    tags=["tasks"]
)
