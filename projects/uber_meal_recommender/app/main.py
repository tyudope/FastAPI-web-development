from fastapi import FastAPI


app = FastAPI(title = "Uber Meal Recommender")


@app.get("/health")
def health():
    return {"status": "ok"}