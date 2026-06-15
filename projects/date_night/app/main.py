from fastapi import FastAPI


app = FastAPI(title = "Date Night v0")


@app.get("/health")
def health():
    return {"status" : "ok"}


