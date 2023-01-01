from fastapi import FastAPI, Depends, HTTPException
# from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import socketio
import aio_pika
import asyncio
from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuth2 as OAuth2Model, SecuritySchemeType
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import socketio
import aio_pika
import asyncio
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer

from app import schemas, models
from app.database import engine, SessionLocal
from app.deps import get_current_user, oauth2_scheme

from websockets_transcriber.events import sio, setup_rabbitmq
from fastapi.middleware.cors import CORSMiddleware


from app.controllers import note_controller, feedback_controller, auth_controller, summary_controller
from dotenv import load_dotenv
import os

load_dotenv(".env.local")
load_dotenv(".env", override=False)

database = os.getenv("SQLALCHEMY_DATABASE_URL")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_app = socketio.ASGIApp(sio, other_asgi_app=app, socketio_path='/ws/socket.io')

# Mount the socket.io app
app.mount("/ws", socket_app)

# Serve the static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def on_startup():
    await setup_rabbitmq()

@app.on_event("shutdown")
async def on_shutdown():
    if rabbitmq_connection:
        await rabbitmq_connection.close()

# Include all the routers
app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
app.include_router(note_controller.router, prefix="/notes", tags=["notes"])
app.include_router(feedback_controller.router, prefix="/feedback", tags=["feedback"])
app.include_router(summary_controller.router, prefix="/summary", tags=["summary"])  # Added summary controller

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
