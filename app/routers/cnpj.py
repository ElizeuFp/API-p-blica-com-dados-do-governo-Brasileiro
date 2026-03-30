from fastapi import APIRouter, HTTPException
from app.services.cnpj_service import buscar_cnpj

router = APIRouter()

@router.get("/{cnpj}")
async def consultar_cnpj(cnpj: str):
    """
    Retorna dados cadastrais de uma empresa a partir do CNPJ.
    Exemplo: /cnpj/19131243000197
    """
    resultado = await buscar_cnpj(cnpj)
    if resultado is None:
        raise HTTPException(status_code=404, detail="CNPJ não encontrado")
    return resultado