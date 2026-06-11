import os
from datetime import datetime
import numpy as np

def format_br_currency(val):
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def generate_markdown_report(df, agg_metrics, stat_results, decision, file_path=None):
    """
    Gera um relatório executivo premium em formato Markdown.
    """
    partner = df['parceiro'].iloc[0]
    start_date = df['data'].min()
    end_date = df['data'].max()
    num_days = df['data'].nunique()
    
    # Cabeçalho & Metadados
    report = []
    report.append(f"# Relatório de Teste A/B de Cashback – Méliuz")
    report.append(f"**Parceiro Analisado:** {partner}  ")
    report.append(f"**Período do Experimento:** {start_date} a {end_date} ({num_days} dias)  ")
    report.append(f"**Data da Análise:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
    
    report.append("---")
    report.append("\n## 1. Resumo Executivo")
    report.append(f"Foi analisado o teste A/B para o parceiro **{partner}** com o objetivo de determinar qual variante de cashback oferece o melhor equilíbrio entre volume de vendas (GMV), rentabilidade e retorno sobre investimento (ROI).")
    
    # Caixa de alerta de decisão
    winner = decision['winner_group']
    decision_text = decision['decision']
    reason = decision['reason']
    
    report.append("\n> [!IMPORTANT]")
    report.append(f"> **RECOMENDAÇÃO FINAL: {decision_text}**  ")
    report.append(f"> *Justificativa:* {reason}\n")
    
    # 2. Tabela de Resultados
    report.append("## 2. Resultados Consolidados")
    report.append("A tabela abaixo apresenta os resultados agregados de cada variante durante todo o período do experimento:\n")
    
    headers = [
        "Variante", 
        "Compradores", 
        "GMV Total", 
        "Comissão", 
        "Cashback", 
        "Lucro Líquido", 
        "ROI",
        "Cashback/Comissão (%)"
    ]
    
    report.append("| " + " | ".join(headers) + " |")
    report.append("|" + "|".join([" :--- " for _ in headers]) + "|")
    
    for group, row in agg_metrics.iterrows():
        roi_pct = f"{row['roi']*100:.1f}%"
        cashback_ratio = f"{row['cashback_sobre_comissao']*100:.1f}%"
        
        row_str = [
            f"**{group}**",
            f"{int(row['compradores_total']):,}".replace(",", "."),
            format_br_currency(row['gmv_total']),
            format_br_currency(row['comissao_total']),
            format_br_currency(row['cashback_total']),
            f"**{format_br_currency(row['lucro_total'])}**",
            f"**{roi_pct}**",
            cashback_ratio
        ]
        report.append("| " + " | ".join(row_str) + " |")
        
    # 3. Economia Unitária (Unit Economics)
    report.append("\n## 3. Eficiência e Unit Economics")
    report.append("Métricas médias por comprador único para entender o comportamento de consumo e a eficiência do incentivo:\n")
    
    headers_unit = [
        "Variante",
        "GMV por Comprador (Ticket Médio)",
        "Comissão por Comprador",
        "Cashback por Comprador",
        "Lucro por Comprador"
    ]
    
    report.append("| " + " | ".join(headers_unit) + " |")
    report.append("|" + "|".join([" :--- " for _ in headers_unit]) + "|")
    
    for group, row in agg_metrics.iterrows():
        row_str = [
            f"**{group}**",
            format_br_currency(row['gmv_por_comprador']),
            format_br_currency(row['comissao_por_comprador']),
            format_br_currency(row['cashback_por_comprador']),
            f"**{format_br_currency(row['lucro_por_comprador'])}**"
        ]
        report.append("| " + " | ".join(row_str) + " |")
        
    # 4. Análise Estatística (Significância)
    report.append("\n## 4. Análise de Significância Estatística")
    report.append("Para certificar de que os resultados observados não são fruto de oscilações casuais (ruído), realizamos testes de hipóteses estatísticas comparando a distribuição diária das variantes de tratamento contra o grupo de controle.\n")
    
    control_group = decision['control_group']
    report.append(f"**Grupo de Controle (Linha de Base):** `{control_group}`\n")
    
    for comp_name, comp in stat_results.items():
        treatment = comp['treatment']
        report.append(f"### Comparação: `{treatment}` vs `{control_group}`")
        
        profit_test = comp['metrics']['lucro_diario']
        roi_test = comp['metrics']['roi_diario']
        gmv_test = comp['metrics']['gmv_por_comprador_diario']
        
        report.append(f"Abaixo estão os resultados do teste T de Welch (comparação de médias diárias) e do teste não-paramétrico de Mann-Whitney U:\n")
        
        headers_stat = ["Métrica Testada", "Dif. Média", "% Var.", "p-value (Welch T-Test)", "p-value (Mann-Whitney)", "Significativo (95%?)"]
        
        report.append("| " + " | ".join(headers_stat) + " |")
        report.append("|" + "|".join([" :--- " for _ in headers_stat]) + "|")
        
        for metric_var, test_info in comp['metrics'].items():
            p_welch = f"{test_info['t_p_value']:.4f}" if not np.isnan(test_info['t_p_value']) else "N/A"
            p_mw = f"{test_info['u_p_value']:.4f}" if not np.isnan(test_info['u_p_value']) else "N/A"
            
            # Formata as diferenças
            if 'roi' in metric_var:
                diff_str = f"{test_info['mean_diff']*100:+.1f} p.p."
            else:
                diff_str = format_br_currency(test_info['mean_diff'])
                if test_info['mean_diff'] > 0:
                    diff_str = "+" + diff_str
                    
            sig_icon = "✅ Sim (p < 0.05)" if test_info['significant_t_05'] else "❌ Não (p >= 0.05)"
            
            row_str = [
                f"**{test_info['label']}**",
                diff_str,
                f"{test_info['pct_diff']*100:+.1f}%",
                p_welch,
                p_mw,
                sig_icon
            ]
            report.append("| " + " | ".join(row_str) + " |")
            
        report.append("")
        
        # Interpreta os resultados de lucro especificamente
        if profit_test['significant_t_05']:
            if profit_test['mean_diff'] > 0:
                report.append(f"> [!TIP]\n> **Insight:** O aumento de lucro observado no grupo `{treatment}` é estatisticamente significativo. A probabilidade desse aumento ser obra do acaso é inferior a 5%, o que dá suporte robusto para a escalabilidade da variante.")
            else:
                report.append(f"> [!WARNING]\n> **Insight:** O grupo `{treatment}` causou uma redução estatisticamente significativa no lucro diário. A estratégia é prejudicial ao negócio.")
        else:
            report.append(f"> [!NOTE]\n> **Insight:** As diferenças de lucro entre `{treatment}` e `{control_group}` não são estatisticamente significativas (p-value = {profit_test['t_p_value']:.3f}). Isso sugere que o comportamento de compra e as margens são semelhantes às atuais e os ganhos nominais podem ser flutuações temporárias.")
            
        report.append("")
        
    # 5. Insights & Riscos
    report.append("## 5. Insights de Negócio e Análise de Risco")
    
    # Insights específicos com base na análise
    for cand in decision['candidates_raw']:
        group = cand['group']
        if cand['profit_diff'] > 0:
            if cand['is_sig_05']:
                report.append(f"- **Vantagem Clara de `{group}`**: A variante demonstrou alta tração comercial com aumento estatisticamente confirmado de lucro líquido total. É a escolha mais lógica de negócio.")
            else:
                report.append(f"- **Melhora Nominal em `{group}`**: Apresentou tendência de alta no lucro, porém sem validação estatística forte. O risco de instabilidade ou variação sazonal nas próximas semanas existe.")
        else:
            report.append(f"- **Inviabilidade Econômica de `{group}`**: Apesar de um possível aumento de compradores ou GMV, a variante reduziu a rentabilidade geral da operação devido ao peso do cashback (custo superou o retorno da comissão).")
            
    # Verifica a sustentabilidade geral do ROI
    report.append("\n**Riscos Identificados:**")
    report.append("1. **Saturação de Cashback**: Aumentar as taxas de cashback atrai mais clientes no curto prazo, mas reduz o ROI caso as vendas adicionais não diluam o custo do benefício.")
    report.append("2. **Fidelidade da Variante**: Usuários atraídos puramente por cashback elevado tendem a apresentar menor LTV (lifetime value) recorrente quando os incentivos diminuem.")
    
    # 6. Resumo da Recomendação
    report.append("\n## 6. Conclusão")
    report.append(f"Com base na análise quantitativa e nos testes de significância estatística, a decisão tomada é:")
    report.append(f"\n### **`{decision_text}`**")
    report.append(f"\n*Próximos passos:*")
    if "Escalar" in decision_text:
        report.append(f"1. Direcionar progressivamente 100% do tráfego do parceiro **{partner}** para o **{winner}**.")
        report.append("2. Monitorar as métricas de conversão e lucro nas próximas 2 semanas para garantir a estabilidade.")
        report.append("3. Registrar formalmente o encerramento do teste no histórico de experimentos.")
    else:
        report.append("1. Encerrar o experimento sem escalar a variante de cashback avaliada.")
        report.append("2. Estruturar uma nova modelagem de taxas de cashback com limites de custo superiores para o próximo ciclo de testes.")
        report.append("3. Avaliar se o parceiro pode oferecer uma comissão maior para viabilizar taxas de cashback mais agressivas.")

    output_content = "\n".join(report)
    
    # Salva o arquivo se o caminho for fornecido
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"Relatório salvo em {file_path}")
        
    return output_content
