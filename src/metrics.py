import pandas as pd
import numpy as np

def calculate_aggregate_metrics(df):
    """
    Calculates aggregated business metrics for each variant group in the test.
    Calcula as métricas de negócio agregadas para cada grupo de variante no teste A/B.
    Argumentos:
        df (pd.DataFrame): Dados limpos e validados.
    Retorna:
        pd.DataFrame: Um DataFrame indexado por grupo com as métricas agregadas.
    """
    # Número de dias no experimento
    num_days = df['data'].nunique()
    
    # Agregando os totais
    grouped = df.groupby('grupo').agg({
        'compradores': 'sum',
        'comissao': 'sum',
        'cashback': 'sum',
        'vendas_totais': 'sum'
    })
    
    # Renomear colunas para maior clareza
    grouped = grouped.rename(columns={
        'compradores': 'compradores_total',
        'comissao': 'comissao_total',
        'cashback': 'cashback_total',
        'vendas_totais': 'gmv_total'
    })
    
    # Calcular KPIs financeiros derivados
    grouped['lucro_total'] = grouped['comissao_total'] - grouped['cashback_total']
    
    # ROI: Lucro Líquido / Cashback
    grouped['roi'] = np.where(
        grouped['cashback_total'] > 0,
        grouped['lucro_total'] / grouped['cashback_total'],
        0.0
    )
    
    # Unit Economics (Métricas por comprador)
    grouped['comissao_por_comprador'] = np.where(
        grouped['compradores_total'] > 0,
        grouped['comissao_total'] / grouped['compradores_total'],
        0.0
    )
    
    grouped['cashback_por_comprador'] = np.where(
        grouped['compradores_total'] > 0,
        grouped['cashback_total'] / grouped['compradores_total'],
        0.0
    )
    
    grouped['gmv_por_comprador'] = np.where(
        grouped['compradores_total'] > 0,
        grouped['gmv_total'] / grouped['compradores_total'],
        0.0
    )
    
    grouped['lucro_por_comprador'] = np.where(
        grouped['compradores_total'] > 0,
        grouped['lucro_total'] / grouped['compradores_total'],
        0.0
    )
    
    # Métricas médias diárias
    grouped['compradores_diarios_medio'] = grouped['compradores_total'] / num_days
    grouped['gmv_diario_medio'] = grouped['gmv_total'] / num_days
    grouped['lucro_diario_medio'] = grouped['lucro_total'] / num_days
    
    # Índice de queima de caixa (Cashburn): Cashback / Comissão (% da receita repassada como cashback)
    grouped['cashback_sobre_comissao'] = np.where(
        grouped['comissao_total'] > 0,
        grouped['cashback_total'] / grouped['comissao_total'],
        0.0
    )
    
    return grouped

def calculate_daily_metrics(df):
    """
    Calcula as séries temporais diárias para cada grupo,
    útil para gráficos de tendência e testes de hipóteses estatísticas.
    """
    df_daily = df.copy()
    
    df_daily['lucro_diario'] = df_daily['comissao'] - df_daily['cashback']
    
    df_daily['roi_diario'] = np.where(
        df_daily['cashback'] > 0,
        df_daily['lucro_diario'] / df_daily['cashback'],
        0.0
    )
    
    df_daily['gmv_por_comprador_diario'] = np.where(
        df_daily['compradores'] > 0,
        df_daily['vendas_totais'] / df_daily['compradores'],
        0.0
    )
    
    df_daily['cashback_por_comprador_diario'] = np.where(
        df_daily['compradores'] > 0,
        df_daily['cashback'] / df_daily['compradores'],
        0.0
    )
    
    return df_daily
