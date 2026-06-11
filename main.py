import os
import sys
import argparse
from datetime import datetime

# Forçar o stdout a usar codificação UTF-8 para evitar erros no terminal Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Adicionar dinamicamente a pasta src ao sys.path para permitir importações limpas
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar módulos locais do pipeline
from loader import load_data
from validator import validate_data
from metrics import calculate_aggregate_metrics, calculate_daily_metrics
from analyzer import perform_statistical_tests, make_decision
from report_generator import generate_markdown_report, format_br_currency
from sheets import register_test_result

def main():
    parser = argparse.ArgumentParser(
        description="Méliuz Cashback A/B Test CLI Analyzer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--file", 
        required=True, 
        help="Caminho para o arquivo CSV do dataset de teste A/B."
    )
    
    parser.add_argument(
        "--name", 
        help="Nome amigável para registrar o teste no histórico. Se omitido, usará o nome do parceiro."
    )
    
    parser.add_argument(
        "--desc", 
        default="Análise automatizada de teste A/B de cashback.", 
        help="Descrição resumida do teste para registrar no histórico."
    )
    
    args = parser.parse_args()
    
    csv_path = args.file
    if not os.path.exists(csv_path):
        print(f"Erro: O arquivo '{csv_path}' não foi encontrado.")
        sys.exit(1)
        
    print(f"\n========================================================")
    print(f"📊 INICIANDO ANÁLISE DE TESTE A/B: {os.path.basename(csv_path)}")
    print(f"========================================================\n")
    
    # 1. Carregamento de dados
    try:
        df = load_data(csv_path)
    except Exception as e:
        print(f"❌ Erro crítico ao carregar arquivo: {str(e)}")
        sys.exit(1)
        
    # 2. Validação dos dados
    is_valid, errors, warnings = validate_data(df)
    
    if not is_valid:
        print("❌ O arquivo não passou nas validações críticas e não pode ser processado:")
        for err in errors:
            print(f"   - {err}")
        sys.exit(1)
        
    if warnings:
        print("⚠️ Avisos de Validação (Não-críticos):")
        for warn in warnings:
            print(f"   - {warn}")
        print()
        
    partner = df['parceiro'].iloc[0]
    start_date = df['data'].min()
    end_date = df['data'].max()
    period = f"{start_date} a {end_date}"
    
    test_name = args.name if args.name else f"Teste A/B {partner}"
    
    # 3. Cálculos e Análise
    agg_metrics = calculate_aggregate_metrics(df)
    df_daily = calculate_daily_metrics(df)
    stat_tests = perform_statistical_tests(df_daily)
    decision = make_decision(agg_metrics, stat_tests)
    
    # 4. Salvar o relatório em arquivo
    report_filename = f"relatorio_{partner.lower().replace(' ', '_')}.md"
    report_path = os.path.join("reports", report_filename)
    
    # Gerar e salvar relatório
    generate_markdown_report(df, agg_metrics, stat_tests, decision, report_path)
    
    # 5. Exibir resumo no console
    winner = decision['winner_group']
    decision_text = decision['decision']
    reason = decision['reason']
    
    print("\n--------------------------------------------------------")
    print("📈 RESUMO DOS RESULTADOS")
    print("--------------------------------------------------------")
    for group, row in agg_metrics.iterrows():
        roi_pct = f"{row['roi']*100:.1f}%"
        profit_str = format_br_currency(row['lucro_total'])
        gmv_str = format_br_currency(row['gmv_total'])
        print(f"Variante: {group:10} | Compradores: {int(row['compradores_total']):5d} | GMV: {gmv_str:13} | Lucro: {profit_str:12} | ROI: {roi_pct}")
    print("--------------------------------------------------------")
    
    print(f"\n🎯 DECISÃO RECOMENDADA:")
    print(f"👉 {decision_text}")
    print(f"\n📝 JUSTIFICATIVA:")
    print(f"{reason}\n")
    
    # 6. Gravação de histórico
    winner_roi = agg_metrics.loc[winner, 'roi'] if winner and winner in agg_metrics.index else 0.0
    winner_profit = agg_metrics.loc[winner, 'lucro_total'] if winner and winner in agg_metrics.index else 0.0
    
    # Encurtar a justificativa para caber na planilha de forma legível
    justification_summary = reason[:160] + "..." if len(reason) > 160 else reason
    full_description = f"{args.desc} | {justification_summary}"
    
    print("💾 Registrando resultado no histórico...")
    local_ok, sheet_ok = register_test_result(
        test_name=test_name,
        partner=partner,
        period=period,
        winner=winner,
        roi=winner_roi,
        profit=winner_profit,
        decision=decision_text,
        description=full_description
    )
    
    print(f"\n========================================================")
    print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
    print(f"Relatório gerado em: {report_path}")
    print(f"========================================================\n")

if __name__ == "__main__":
    main()
