from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import app as services_app

app = FastAPI(title="API de Eleições", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("", services_app)

@app.get("/")
def root():
    return {"message": "API rodando com sucesso no Render!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
