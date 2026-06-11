import pandas as pd
import numpy as np

def clean_currency(val):
    """
    Limpa strings de moedas no formato brasileiro (ex: 'R$ 1.250,50' ou 'R$150,00' ou '-R$ 10,00')
    e as converte para valores em float (ex: 1250.50, 150.00, -10.00).
    """
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    
    val_str = str(val).strip()
    if not val_str or val_str.lower() == 'nan':
        return 0.0
        
    # Remover R$ e espaços em branco
    val_str = val_str.replace("R$", "").replace(" ", "")
    
    # Verificar se o valor é negativo
    is_negative = False
    if val_str.startswith("-"):
        is_negative = True
        val_str = val_str.replace("-", "")
    elif val_str.startswith("("):  # formato contábil negativo, ex: (R$ 10,00)
        is_negative = True
        val_str = val_str.replace("(", "").replace(")", "")
        
    # Substituir ponto (separador de milhar) por vazio, e vírgula (separador decimal) por ponto
    val_str = val_str.replace(".", "").replace(",", ".")
    
    try:
        num = float(val_str)
        return -num if is_negative else num
    except ValueError:
        return 0.0

def load_data(file_path):
    """
    Carrega o arquivo CSV do teste A/B, limpa as colunas de moeda e padroniza o schema.
    Retorna:
        pd.DataFrame: DataFrame com dados limpos e tipados corretamente.
    """
    # Carregar usando pandas (auto-detectar separador como tab, vírgula ou ponto e vírgula)
    df = pd.read_csv(file_path, sep=None, engine='python')
    
    # Padronizar o mapeamento de colunas (ignora maiúsculas/minúsculas e espaços extras)
    # Colunas esperadas: Data, Grupos de usuários, Parceiro, compradores, comissão, cashback, vendas totais
    column_mapping = {}
    for col in df.columns:
        col_clean = col.strip().lower()
        if col_clean in ['data', 'date']:
            column_mapping[col] = 'data'
        elif col_clean in ['grupos de usuários', 'grupos de usuarios', 'grupo', 'group', 'groups']:
            column_mapping[col] = 'grupo'
        elif col_clean in ['parceiro', 'partner']:
            column_mapping[col] = 'parceiro'
        elif col_clean in ['compradores', 'buyers']:
            column_mapping[col] = 'compradores'
        elif col_clean in ['comissão', 'comissao', 'commission']:
            column_mapping[col] = 'comissao'
        elif col_clean in ['cashback']:
            column_mapping[col] = 'cashback'
        elif col_clean in ['vendas totais', 'vendas_totais', 'sales', 'gmv']:
            column_mapping[col] = 'vendas_totais'
            
    df = df.rename(columns=column_mapping)
    
    # Verificar se todas as colunas essenciais foram mapeadas
    essential_cols = ['data', 'grupo', 'parceiro', 'compradores', 'comissao', 'cashback', 'vendas_totais']
    missing_cols = [c for c in essential_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"O dataset está faltando colunas obrigatórias ou não pôde mapeá-las: {missing_cols}")
        
    # Padronizar tipos de dados e limpar valores
    df['data'] = pd.to_datetime(df['data']).dt.strftime('%Y-%m-%d')
    df['grupo'] = df['grupo'].astype(str).str.strip()
    df['parceiro'] = df['parceiro'].astype(str).str.strip()
    
    # Preencher NaN em compradores com 0
    df['compradores'] = df['compradores'].fillna(0).astype(int)
    
    # Limpar as colunas monetárias
    currency_cols = ['comissao', 'cashback', 'vendas_totais']
    for col in currency_cols:
        df[col] = df[col].apply(clean_currency)
        
    # Ordenar por data e grupo para consistência
    df = df.sort_values(by=['data', 'grupo']).reset_index(drop=True)
    
    return df
