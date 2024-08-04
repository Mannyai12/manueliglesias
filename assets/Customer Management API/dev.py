import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.routers.api:app", host="localhost", reload=True, port=8000)