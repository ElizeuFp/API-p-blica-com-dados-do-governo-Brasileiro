from fastapi import APIRouter, HTTPException
from app.services.cep_service import buscar_cep

router = APIRouter()

@router.get("/{cep}")
async def consultar_cep(cep: str):
    """
    Retorna endereço completo a partir de um CEP brasileiro.
    Exemplo: /cep/01001000
    """
    resultado = await buscar_cep(cep)
    if resultado is None:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    return resultado