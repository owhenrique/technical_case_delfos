from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
"""
Instancia global do rate limiter baseado em IP.

Utiliza o slowapi para impor limites de requisicoes por janela de tempo,
protegendo a API contra uso abusivo ou ataques de forca bruta. A funcao
`get_remote_address` extrai o IP do cliente a cada requisicao.

O limiter e registrado como state da aplicacao FastAPI em `main.py`.
"""
