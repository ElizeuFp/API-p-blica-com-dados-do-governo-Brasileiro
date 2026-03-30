import httpx

async def buscar_cnpj(cnpj: str):
    """
    Consulta dados de CNPJ na BrasilAPI (fonte: Receita Federal).
    Retorna dicionário com os dados ou None se não encontrado.
    """
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
    
    # Desabilita verificação SSL (apenas para desenvolvimento local)
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url)
        
        if response.status_code == 404:
            return None
        response.raise_for_status()
        dados = response.json()
        
    return dados