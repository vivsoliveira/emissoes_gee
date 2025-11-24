# ESSE ARQUIVO COLOCA CADA NUMERO NO SEU RESPECTIVO ESTADO PARA CONSEGUIR UNIR AS TABELAS
import requests
import pandas as pd

print("Baixando lista de municípios do IBGE...")
url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

try:
    response = requests.get(url)
    response.raise_for_status()
    
    municipios = response.json()
    
    # Mapeamento de código UF para sigla
    uf_map = {
        11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO',
        21: 'MA', 22: 'PI', 23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA',
        31: 'MG', 32: 'ES', 33: 'RJ', 35: 'SP',
        41: 'PR', 42: 'SC', 43: 'RS',
        50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF'
    }
    
    # Cria DataFrame com os dados
    dados = []
    for mun in municipios:
        codigo_uf = int(str(mun['id'])[:2])
        uf_sigla = uf_map.get(codigo_uf, '')
        
        dados.append({
            'codigo_ibge': mun['id'],
            'nome': mun['nome'],
            'codigo_uf': codigo_uf,
            'uf': uf_sigla
        })
    
    df = pd.DataFrame(dados)
    
    # Salva em CSV
    df.to_csv('municipios.csv', index=False, encoding='utf-8')
    
    print(f"\n✅ Arquivo criado com {len(df)} municípios!")
    print(f"\nPrimeiros 10 municípios:")
    for i, row in df.head(10).iterrows():
        print(f"  {i+1}. {row['nome']} ({row['uf']}) - Código: {row['codigo_ibge']}")
    
except Exception as e:
    print(f"❌ Erro ao baixar dados: {e}")
