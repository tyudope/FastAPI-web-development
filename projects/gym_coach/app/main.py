from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def status():
    return {"status" : "ok"}