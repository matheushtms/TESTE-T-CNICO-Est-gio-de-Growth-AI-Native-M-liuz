import pandas as pd
import numpy as np

def validate_data(df):
    """
    Valida o DataFrame carregado e limpo.
    Retorna:
        is_valid (bool): True se não existirem erros críticos, False caso contrário.
        errors (list): Lista de erros críticos que impedem a análise.
        warnings (list): Lista de avisos (problemas não-críticos).
    """
    errors = []
    warnings = []
    
    # Verificar se está vazio
    if df.empty:
        errors.append("O dataset está vazio.")
        return False, errors, warnings
        
    # Verificar se as colunas essenciais existem
    essential_cols = ['data', 'grupo', 'parceiro', 'compradores', 'comissao', 'cashback', 'vendas_totais']
    for col in essential_cols:
        if col not in df.columns:
            errors.append(f"Coluna obrigatória ausente: '{col}'")
            
    if errors:
        return False, errors, warnings
        
    # Verificar por valores nulos ou ausentes
    null_counts = df[essential_cols].isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            warnings.append(f"A coluna '{col}' possui {count} valores nulos/NaN. Eles foram tratados.")
            
    # Verificar os tipos de dados
    if not pd.api.types.is_integer_dtype(df['compradores']):
        errors.append("A coluna 'compradores' deve conter apenas números inteiros.")
        
    # Verificar se há valores negativos
    neg_buyers = (df['compradores'] < 0).sum()
    if neg_buyers > 0:
        warnings.append(f"Detectados {neg_buyers} registros com quantidade de compradores negativa. Valores devem ser não-negativos.")
        
    neg_vendas = (df['vendas_totais'] < 0).sum()
    if neg_vendas > 0:
        warnings.append(f"Detectados {neg_vendas} registros com vendas totais (GMV) negativas.")
        
    neg_comissao = (df['comissao'] < 0).sum()
    if neg_comissao > 0:
        warnings.append(f"Detectados {neg_comissao} registros com comissão negativa.")
        
    neg_cashback = (df['cashback'] < 0).sum()
    if neg_cashback > 0:
        warnings.append(f"Detectados {neg_cashback} registros com cashback negativo.")
        
    # Verificar se a comissão é menor que o cashback (lucro operacional negativo no dia)
    unprofitable_days = (df['comissao'] < df['cashback']).sum()
    if unprofitable_days > 0:
        warnings.append(f"Detectados {unprofitable_days} registros onde o cashback distribuído no dia foi maior que a comissão recebida (prejuízo operacional diário).")
        
    # Verificar quantidade de parceiros no arquivo
    unique_partners = df['parceiro'].unique()
    if len(unique_partners) > 1:
        warnings.append(f"O dataset contém dados de múltiplos parceiros: {list(unique_partners)}. O recomendado é um parceiro por arquivo.")
        
    # Verificar quantidade de grupos (variantes) no teste A/B
    unique_groups = df['grupo'].unique()
    if len(unique_groups) < 2:
        errors.append(f"O teste A/B precisa de pelo menos 2 grupos de usuários para comparação. Encontrado apenas: {list(unique_groups)}")
        
    is_valid = len(errors) == 0
    return is_valid, errors, warnings
