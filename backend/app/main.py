from fastapi import FastAPI

app = FastAPI(
    title="Dai AI Agent",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Dai Backend Running"
    }