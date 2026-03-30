import httpx

async def buscar_cep(cep: str):
    """
    Consulta o CEP na API pública ViaCEP.
    Retorna um dicionário com os dados ou None se não encontrado.
    """
    cep_limpo = cep.replace("-", "").strip()
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        dados = response.json()

    if "erro" in dados:
        return None
    return dados