import os
import csv
import random
from datetime import datetime, timedelta

def format_br_currency(value):
    """Formata um valor float para uma string de moeda do Real Brasileiro (R$ 1.250,50)"""
    # Formata para duas casas decimais
    formatted = f"{value:.2f}"
    # Substitui o ponto por vírgula
    parts = formatted.split('.')
    # Adiciona o separador de milhar
    integer_part = parts[0]
    decimal_part = parts[1]
    
    # Adiciona ponto para os milhares
    reversed_integer = integer_part[::-1]
    chunks = [reversed_integer[i:i+3] for i in range(0, len(reversed_integer), 3)]
    integer_part_formatted = ".".join(chunks)[::-1]
    
    return f"R$ {integer_part_formatted},{decimal_part}"

def generate_partner_data(filename, partner_name, start_date_str, days, groups_config):
    """
    Formato de groups_config: {
        'Grupo 1': {
            'base_buyers': 1000,
            'gmv_per_buyer_mean': 150,
            'commission_rate': 0.10,  # 10% de comissão
            'cashback_rate': 0.03,    # 3% de cashback
            'variance_factor': 0.1
        },
        ...
    }
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    
    headers = [
        "Data", 
        "Grupos de usuários", 
        "Parceiro", 
        "compradores", 
        "comissão", 
        "cashback", 
        "vendas totais"
    ]
    
    rows = []
    
    for d in range(days):
        current_date = start_date + timedelta(days=d)
        date_str = current_date.strftime("%Y-%m-%d")
        
        for group_name, cfg in groups_config.items():
            # Adiciona alguma variação aleatória
            vf = cfg['variance_factor']
            day_multiplier = 1.0 + random.uniform(-vf, vf)
            
            # Sazonalidade semanal (queda nos fins de semana)
            if current_date.weekday() in [5, 6]:  # Saturday, Sunday
                day_multiplier *= 0.7
                
            # Compradores
            buyers = int(cfg['base_buyers'] * day_multiplier)
            if buyers < 0:
                buyers = 0
                
            # GMV
            gmv_per_buyer = cfg['gmv_per_buyer_mean'] * (1.0 + random.uniform(-0.05, 0.05))
            vendas_totais = buyers * gmv_per_buyer
            
            # Comissão (comissão)
            comissao = vendas_totais * cfg['commission_rate']
            
            # Cashback
            cashback = vendas_totais * cfg['cashback_rate']
            
            # Formata para o formato de string R$
            comissao_str = format_br_currency(comissao)
            cashback_str = format_br_currency(cashback)
            vendas_totais_str = format_br_currency(vendas_totais)
            
            rows.append([
                date_str,
                group_name,
                partner_name,
                buyers,
                comissao_str,
                cashback_str,
                vendas_totais_str
            ])
            
    # Escreve no CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Generated {filename} with {len(rows)} rows.")

def main():
    # Define a semente (seed) para reprodutibilidade
    random.seed(42)
    
    # 1. Parceiro A: 2 Variantes (Grupo 1 vs Grupo 2)
    # Cenário: O tratamento (Grupo 2) tem cashback maior, o que aumenta a conversão e o GMV.
    # O lucro total do Grupo 2 é maior e o ROI continua muito forte. (Escalar tratamento!)
    config_a = {
        "Grupo 1": {
            "base_buyers": 500,
            "gmv_per_buyer_mean": 120.0,
            "commission_rate": 0.08,  # 8% de comissão
            "cashback_rate": 0.02,    # 2% de cashback
            "variance_factor": 0.15
        },
        "Grupo 2": {
            "base_buyers": 1100,       # aumento significativo de compradores
            "gmv_per_buyer_mean": 140.0, # ticket médio maior
            "commission_rate": 0.08,  # 8% de comissão
            "cashback_rate": 0.035,   # 3.5% de cashback (margem sustentável de 4.5%)
            "variance_factor": 0.15
        }
    }
    
    # 2. Parceiro B: 3 Variantes (Grupo 1 vs Grupo 2 vs Grupo 3)
    # Cenário: O Grupo 3 tem cashback muito alto (6.5%), o que aumenta o GMV e compradores,
    # mas a comissão (5%) é menor do que a taxa de cashback, tornando-o não lucrativo (lucro negativo)!
    # O Grupo 2 tem 3% de cashback e 6% de comissão, o que é lucrativo e melhor que o controle.
    # Recomendação de escalar o Grupo 2, NÃO o Grupo 3.
    config_b = {
        "Grupo 1": {
            "base_buyers": 800,
            "gmv_per_buyer_mean": 80.0,
            "commission_rate": 0.06,  # 6% de comissão
            "cashback_rate": 0.015,   # 1.5% de cashback
            "variance_factor": 0.1
        },
        "Grupo 2": {
            "base_buyers": 950,
            "gmv_per_buyer_mean": 85.0,
            "commission_rate": 0.06,  # 6% de comissão
            "cashback_rate": 0.03,    # 3.0% de cashback
            "variance_factor": 0.1
        },
        "Grupo 3": {
            "base_buyers": 1200,      # Muitos compradores, mas...
            "gmv_per_buyer_mean": 90.0,
            "commission_rate": 0.05,  # Parceiro espremeu a comissão para 5%
            "cashback_rate": 0.065,   # cashback de 6.5% (economia unitária negativa!)
            "variance_factor": 0.1
        }
    }
    
    # 3. Parceiro C: 2 Variantes (Grupo 1 vs Grupo 2)
    # Cenário: Teste inconclusivo. As diferenças entre o Grupo 1 e o Grupo 2 são puro ruído.
    # Estatisticamente insignificante (p-values devem ser altos). Recomendação de não escalar.
    config_c = {
        "Grupo 1": {
            "base_buyers": 400,
            "gmv_per_buyer_mean": 200.0,
            "commission_rate": 0.10,
            "cashback_rate": 0.03,    # 3.0% de cashback (margem líquida de 7.0%)
            "variance_factor": 0.2
        },
        "Grupo 2": {
            "base_buyers": 410,       # um pouco mais de compradores
            "gmv_per_buyer_mean": 200.0,
            "commission_rate": 0.10,
            "cashback_rate": 0.029,   # 2.9% de cashback (margem líquida de 7.1%)
            "variance_factor": 0.2
        }
    }
    
    generate_partner_data("data/parceiro_a.csv", "Parceiro A", "2026-01-01", 30, config_a)
    generate_partner_data("data/parceiro_b.csv", "Parceiro B", "2026-01-01", 45, config_b)
    generate_partner_data("data/parceiro_c.csv", "Parceiro C", "2026-01-01", 30, config_c)

if __name__ == "__main__":
    main()
