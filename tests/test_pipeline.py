import os
import sys
import unittest
import pandas as pd

# Adiciona o diretório src ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from loader import clean_currency
from validator import validate_data
from metrics import calculate_aggregate_metrics
from analyzer import make_decision

class TestPipeline(unittest.TestCase):
    
    def test_clean_currency(self):
        # Testes básicos de moeda
        self.assertEqual(clean_currency("R$ 1.250,50"), 1250.5)
        self.assertEqual(clean_currency("R$150,00"), 150.0)
        self.assertEqual(clean_currency("R$ 0,00"), 0.0)
        
        # Números negativos e notações contábeis
        self.assertEqual(clean_currency("-R$ 10,00"), -10.0)
        self.assertEqual(clean_currency("(R$ 100,50)"), -100.5)
        
        # Entradas numéricas (float e int)
        self.assertEqual(clean_currency(1234.56), 1234.56)
        self.assertEqual(clean_currency(100), 100.0)
        
        # Valores ausentes ou nulos
        self.assertEqual(clean_currency(None), 0.0)
        self.assertEqual(clean_currency("nan"), 0.0)
        self.assertEqual(clean_currency(""), 0.0)
        
    def test_validator_valid_and_invalid(self):
        # Cria um dataframe válido
        valid_data = {
            'data': ['2026-01-01', '2026-01-01'],
            'grupo': ['Grupo 1', 'Grupo 2'],
            'parceiro': ['Parceiro X', 'Parceiro X'],
            'compradores': [100, 150],
            'comissao': [200.0, 300.0],
            'cashback': [50.0, 80.0],
            'vendas_totais': [2000.0, 3000.0]
        }
        df_valid = pd.DataFrame(valid_data)
        is_valid, errors, warnings = validate_data(df_valid)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Teste com colunas ausentes
        invalid_data = {
            'data': ['2026-01-01'],
            'grupo': ['Grupo 1'],
            # 'parceiro' ausente
            'compradores': [100],
            'comissao': [200.0],
            'cashback': [50.0],
            'vendas_totais': [2000.0]
        }
        df_invalid = pd.DataFrame(invalid_data)
        is_valid, errors, warnings = validate_data(df_invalid)
        self.assertFalse(is_valid)
        self.assertTrue(any("parceiro" in err for err in errors))
        
    def test_metrics_calculation(self):
        # Dados de teste de amostra
        test_data = {
            'data': ['2026-01-01', '2026-01-02', '2026-01-01', '2026-01-02'],
            'grupo': ['Grupo 1', 'Grupo 1', 'Grupo 2', 'Grupo 2'],
            'parceiro': ['Parceiro A', 'Parceiro A', 'Parceiro A', 'Parceiro A'],
            'compradores': [10, 20, 15, 25],
            'comissao': [100.0, 200.0, 150.0, 250.0],
            'cashback': [20.0, 40.0, 50.0, 70.0],
            'vendas_totais': [1000.0, 2000.0, 1500.0, 2500.0]
        }
        df = pd.DataFrame(test_data)
        metrics = calculate_aggregate_metrics(df)
        
        # Verifica os totais do Grupo 1:
        # compradores = 30
        # comissao = 300
        # cashback = 60
        # lucro = 300 - 60 = 240
        # roi = 240 / 60 = 4.0 (400%)
        # gmv = 3000
        self.assertEqual(metrics.loc['Grupo 1', 'compradores_total'], 30)
        self.assertEqual(metrics.loc['Grupo 1', 'lucro_total'], 240.0)
        self.assertEqual(metrics.loc['Grupo 1', 'roi'], 4.0)
        self.assertEqual(metrics.loc['Grupo 1', 'gmv_por_comprador'], 100.0)
        
    def test_decision_engine(self):
        # Caso A: Tratamento tem lucro maior, ROI maior e é estatisticamente significativo
        # Simulamos as métricas e os testes diretamente
        agg_metrics = pd.DataFrame({
            'compradores_total': [1000, 1200],
            'comissao_total': [1000.0, 1500.0],
            'cashback_total': [200.0, 300.0],
            'gmv_total': [10000.0, 15000.0],
            'lucro_total': [800.0, 1200.0], # Vencedor tem lucro maior (1200 > 800)
            'roi': [4.0, 4.0]
        }, index=['Grupo 1', 'Grupo 2'])
        
        stat_tests = {
            'Grupo 2 vs Grupo 1': {
                'control': 'Grupo 1',
                'treatment': 'Grupo 2',
                'metrics': {
                    'lucro_diario': {
                        'label': 'Lucro Diário',
                        'control_mean': 40.0,
                        'treatment_mean': 60.0,
                        'mean_diff': 20.0,
                        'pct_diff': 0.5,
                        't_p_value': 0.01, # ESTATISTICAMENTE SIGNIFICATIVO
                        'significant_t_05': True,
                        'significant_t_10': True
                    },
                    'roi_diario': {
                        'label': 'ROI Diário',
                        'control_mean': 4.0,
                        'treatment_mean': 4.0,
                        'mean_diff': 0.0,
                        'pct_diff': 0.0,
                        't_p_value': 0.9,
                        'significant_t_05': False
                    },
                    'gmv_por_comprador_diario': {
                        'label': 'GMV por Comprador Diário',
                        'control_mean': 10.0,
                        'treatment_mean': 12.5,
                        'mean_diff': 2.5,
                        'pct_diff': 0.25,
                        't_p_value': 0.01,
                        'significant_t_05': True
                    }
                }
            }
        }
        
        rec = make_decision(agg_metrics, stat_tests, control_group='Grupo 1')
        self.assertEqual(rec['winner_group'], 'Grupo 2')
        self.assertIn("Escalar Grupo 2", rec['decision'])
        self.assertIn("Estatisticamente Significativo", rec['reason'])
        
        # Caso B: Tratamento tem GMV maior, mas lucro total menor devido ao alto cashback
        agg_metrics_costly = pd.DataFrame({
            'compradores_total': [1000, 1800],
            'comissao_total': [1000.0, 1800.0],
            'cashback_total': [200.0, 1700.0], # Queima massiva de cashback!
            'gmv_total': [10000.0, 18000.0],
            'lucro_total': [800.0, 100.0], # Lucro do tratamento é apenas 100 (vs 800 no controle)
            'roi': [4.0, 0.05]
        }, index=['Grupo 1', 'Grupo 2'])
        
        stat_tests_costly = {
            'Grupo 2 vs Grupo 1': {
                'control': 'Grupo 1',
                'treatment': 'Grupo 2',
                'metrics': {
                    'lucro_diario': {
                        'label': 'Lucro Diário',
                        'control_mean': 40.0,
                        'treatment_mean': 5.0,
                        'mean_diff': -35.0,
                        'pct_diff': -0.875,
                        't_p_value': 0.001,
                        'significant_t_05': True,
                        'significant_t_10': True
                    },
                    'roi_diario': {
                        'label': 'ROI Diário',
                        'control_mean': 4.0,
                        'treatment_mean': 0.05,
                        'mean_diff': -3.95,
                        'pct_diff': -0.98,
                        't_p_value': 0.001,
                        'significant_t_05': True,
                        'significant_t_10': True
                    },
                    'gmv_por_comprador_diario': {
                        'label': 'GMV por Comprador Diário',
                        'control_mean': 10.0,
                        'treatment_mean': 10.0,
                        'mean_diff': 0.0,
                        'pct_diff': 0.0,
                        't_p_value': 0.9,
                        'significant_t_05': False,
                        'significant_t_10': False
                    }
                }
            }
        }
        
        rec_costly = make_decision(agg_metrics_costly, stat_tests_costly, control_group='Grupo 1')
        self.assertEqual(rec_costly['winner_group'], 'Grupo 1')
        self.assertIn("Manter o Controle", rec_costly['decision'])

if __name__ == '__main__':
    unittest.main()
