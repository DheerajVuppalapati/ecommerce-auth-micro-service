from fastapi import FastAPI

from app.cores.database import Base, engine
from app.routes import user


#define the fastapi app instance the module level 
app = FastAPI(title="E-commerce Backend")

Base.metadata.create_all(bind=engine)

app.include_router(user.router)