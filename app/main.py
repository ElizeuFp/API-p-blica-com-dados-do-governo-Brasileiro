from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import json
from app.routers import cep, cnpj

app = FastAPI(
    title="API de Dados do Governo Brasileiro",
    description="Consulta CEP, CNPJ, IBGE e outros dados abertos",
    version="1.0.0"
)

class PrettyJSONMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if response.headers.get("content-type") == "application/json" and response.status_code == 200:
            # Lê o corpo original
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            # Formata o JSON com indentação
            data = json.loads(body)
            pretty_body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
            # Converte headers para dicionário normal e remove content-length
            headers = dict(response.headers)
            headers.pop("content-length", None)
            # Cria nova resposta com o conteúdo formatado
            new_response = Response(
                content=pretty_body,
                status_code=response.status_code,
                headers=headers,
                media_type=response.media_type
            )
            return new_response
        return response

app.add_middleware(PrettyJSONMiddleware)

# Inclui roteadores
app.include_router(cep.router, prefix="/cep", tags=["CEP"])
app.include_router(cnpj.router, prefix="/cnpj", tags=["CNPJ"])

@app.get("/")
async def raiz():
    return {
        "mensagem": "API rodando!",
        "endpoints": [
            "/cep/{cep} - consultar endereço por CEP",
            "/cnpj/{cnpj} - consultar dados de empresa por CNPJ"
        ]
    }