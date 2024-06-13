from fastapi import FastAPI
from routers import UserApi,UserAuthenticate
from database import Base, engine


Base.metadata.create_all(engine)
description = "Backend"

app = FastAPI(title="Backend User App",
    description=description,
    summary="Backend's User app.",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    # contact={
    #     "name": "Deadpoolio the Amazing",
    #     "url": "http://x-force.example.com/contact/",
    #     "email": "dp@x-force.example.com",
    # },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
    )


app.include_router(UserApi.router)
app.include_router(UserAuthenticate.router)



# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
