import logging

from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler  # noqa: PLC2701
from slowapi.errors import RateLimitExceeded

from src.api.limiter import limiter
from src.api.logging_config import setup_logging
from src.api.routers import router

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title='Delfos Conector API',
    description='API exposing Fonte database data',
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router)


@app.middleware('http')
async def log_requests(request: Request, call_next):
    """
    Middleware de logging que registra cada requisicao HTTP.

    Captura o metodo, path e IP de origem antes da execucao
    e loga o status code retornado ao final.

    Args:
        request (Request): O objeto da requisicao recebida.
        call_next: A proxima funcao na cadeia de middlewares.

    Returns:
        Response: A resposta HTTP gerada pelo endpoint.
    """
    logger.info(
        'Request: %s %s from %s',
        request.method,
        request.url.path,
        request.client.host,
    )
    response = await call_next(request)
    logger.info(
        'Response: %s %s -> %d',
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


@app.get('/health')
def health_check():
    """
    Endpoint simples de verificacao de saude da aplicacao.

    Returns:
        dict: Um dicionario indicando que o status esta OK.
    """
    return {'status': 'ok'}
