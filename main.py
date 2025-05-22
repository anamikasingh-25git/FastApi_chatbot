from fastapi import FastAPI, Depends
from app.api.routers import chats, messages, branches, auth
from app.core.cache import init_cache
from app.dependencies import get_current_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(chats.router, prefix="/api/v1/chats", dependencies=[Depends(get_current_user)])
app.include_router(messages.router, prefix="/api/v1/messages", dependencies=[Depends(get_current_user)])
app.include_router(branches.router, prefix="/api/v1/branches", dependencies=[Depends(get_current_user)])

@app.on_event("startup")
async def on_startup():
    init_cache()