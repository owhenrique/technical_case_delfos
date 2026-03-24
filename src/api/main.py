from fastapi import FastAPI

from src.api.routers import router

app = FastAPI(
    title='Delfos Conector API', description='API exposing Fonte database data'
)

app.include_router(router)


@app.get('/health')
def health_check():
    return {'status': 'ok'}
