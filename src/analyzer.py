import pandas as pd
import numpy as np
from scipy import stats

def perform_statistical_tests(df_daily, control_group=None):
    """
    Realiza testes estatísticos comparativos (Welch's T-Test e Mann-Whitney U-Test) entre todas as variantes.
    Se um grupo de controle for especificado, compara todos os tratamentos em relação ao controle.
    """
    groups = sorted(df_daily['grupo'].unique())
    if len(groups) < 2:
        return {}
        
    # Se o grupo de controle não for especificado, tenta inferi-lo
    if control_group not in groups:
        control_candidates = [g for g in groups if '1' in g.lower() or 'control' in g.lower() or 'controle' in g.lower()]
        if control_candidates:
            control_group = control_candidates[0]
        else:
            control_group = groups[0]
            
    comparisons = {}
    
    # Realizar comparações de cada grupo de tratamento contra o grupo de controle
    for group in groups:
        if group == control_group:
            continue
            
        ctrl_data = df_daily[df_daily['grupo'] == control_group]
        treat_data = df_daily[df_daily['grupo'] == group]
        
        comp_key = f"{group} vs {control_group}"
        comparisons[comp_key] = {
            'control': control_group,
            'treatment': group,
            'metrics': {}
        }
        
        # Testamos três variáveis de séries temporais: lucro_diario, roi_diario, gmv_por_comprador_diario
        vars_to_test = {
            'lucro_diario': 'Lucro Diário',
            'roi_diario': 'ROI Diário',
            'gmv_por_comprador_diario': 'GMV por Comprador Diário'
        }
        
        for var, label in vars_to_test.items():
            ctrl_series = ctrl_data[var].dropna()
            treat_series = treat_data[var].dropna()
            
            ctrl_mean = ctrl_series.mean()
            treat_mean = treat_series.mean()
            mean_diff = treat_mean - ctrl_mean
            pct_diff = (mean_diff / ctrl_mean) if ctrl_mean != 0 else 0.0
            
            # Welch's t-test (variâncias desiguais)
            t_stat, t_p = np.nan, np.nan
            if ctrl_series.var() > 0 or treat_series.var() > 0:
                try:
                    t_stat, t_p = stats.ttest_ind(treat_series, ctrl_series, equal_var=False)
                except Exception:
                    pass
                    
            # Mann-Whitney U test (não-paramétrico, robusto para distribuições não-normais)
            u_stat, u_p = np.nan, np.nan
            if len(ctrl_series) > 0 and len(treat_series) > 0:
                try:
                    u_stat, u_p = stats.mannwhitneyu(treat_series, ctrl_series, alternative='two-sided')
                except Exception:
                    pass
                    
            comparisons[comp_key]['metrics'][var] = {
                'label': label,
                'control_mean': ctrl_mean,
                'treatment_mean': treat_mean,
                'mean_diff': mean_diff,
                'pct_diff': pct_diff,
                't_stat': t_stat,
                't_p_value': t_p,
                'u_stat': u_stat,
                'u_p_value': u_p,
                'significant_t_05': t_p < 0.05 if not np.isnan(t_p) else False,
                'significant_t_10': t_p < 0.10 if not np.isnan(t_p) else False,
            }
            
    return comparisons

def make_decision(agg_metrics, statistical_tests, control_group=None):
    """
    Aplica heurísticas de negócios e análises estatísticas para propor uma recomendação.
    Prioridades de decisão:
    1. Maximizar o Lucro Líquido total é o objetivo primário.
    2. O ROI deve ser positivo e sustentável (evitar queima de caixa ineficiente).
    3. Significância estatística (p-value < 0.05 ou 0.10) indica se a mudança é real ou ruído.
    """
    groups = list(agg_metrics.index)
    
    # Identificar o grupo de controle
    if control_group not in groups:
        control_candidates = [g for g in groups if '1' in g.lower() or 'control' in g.lower() or 'controle' in g.lower()]
        if control_candidates:
            control_group = control_candidates[0]
        else:
            control_group = sorted(groups)[0]
            
    control_profit = agg_metrics.loc[control_group, 'lucro_total']
    control_roi = agg_metrics.loc[control_group, 'roi']
    
    recommendation = {
        'control_group': control_group,
        'winner_group': None,
        'decision': "Não escalar nenhuma variante",
        'reason': "",
        'details': [],
        'scores': {}
    }
    
    candidates = []
    
    for comp_name, comp in statistical_tests.items():
        treatment = comp['treatment']
        
        treat_profit = agg_metrics.loc[treatment, 'lucro_total']
        treat_roi = agg_metrics.loc[treatment, 'roi']
        treat_gmv = agg_metrics.loc[treatment, 'gmv_total']
        
        profit_diff = treat_profit - control_profit
        profit_pct_diff = (profit_diff / control_profit) if control_profit != 0 else 0.0
        
        # Obter resultados dos testes estatísticos para o lucro
        profit_stats = comp['metrics'].get('lucro_diario', {})
        p_val_profit = profit_stats.get('t_p_value', np.nan)
        is_sig_05 = profit_stats.get('significant_t_05', False)
        is_sig_10 = profit_stats.get('significant_t_10', False)
        
        # Obter resultados dos testes estatísticos para o GMV por comprador
        gmv_stats = comp['metrics'].get('gmv_por_comprador_diario', {})
        is_gmv_sig_05 = gmv_stats.get('significant_t_05', False)
        
        # Qualificação do candidato:
        # 1. Lucro total deve ser maior que o controle (profit_diff > 0).
        # 2. ROI total da variante deve ser positivo (ROI > 0). Se for negativo, é queima de margem ineficiente.
        is_candidate = profit_diff > 0 and treat_profit > 0 and treat_roi > 0
        
        candidate_info = {
            'group': treatment,
            'profit_diff': profit_diff,
            'profit_pct_diff': profit_pct_diff,
            'roi': treat_roi,
            'roi_diff': treat_roi - control_roi,
            'p_value_profit': p_val_profit,
            'is_sig_05': is_sig_05,
            'is_sig_10': is_sig_10,
            'is_gmv_sig_05': is_gmv_sig_05,
            'is_candidate': is_candidate,
            'gmv_total': treat_gmv
        }
        candidates.append(candidate_info)
        
    # Filtrar candidatos viáveis
    viable_candidates = [c for c in candidates if c['is_candidate']]
    
    if not viable_candidates:
        # Caso 1: Nenhum tratamento foi melhor ou rentável
        # Verificar se o próprio controle dá prejuízo
        if control_profit < 0:
            recommendation['decision'] = "Não escalar nenhuma variante neste momento"
            recommendation['reason'] = (
                f"Todas as variantes de cashback testadas (incluindo o grupo de controle '{control_group}') "
                f"apresentaram prejuízo líquido total para a empresa. Recomenda-se pausar a campanha e revisar o modelo."
            )
        else:
            recommendation['winner_group'] = control_group
            recommendation['decision'] = f"Manter o Controle ({control_group}) em 100%"
            recommendation['reason'] = (
                "Nenhuma das variantes de tratamento superou o grupo de controle em lucro líquido total ou apresentou ROI sustentável. "
                "Portanto, a recomendação mais segura e rentável é manter o grupo de controle."
            )
        recommendation['details'].append("Nenhum grupo de tratamento apresentou ganho financeiro líquido positivo em relação ao controle.")
        
    else:
        # Temos candidatos viáveis. Vamos selecionar o melhor com base nas heurísticas.
        # Priorizar ganhos de lucro estatisticamente significativos (p < 0.05).
        sig_candidates = [c for c in viable_candidates if c['is_sig_05']]
        marginal_candidates = [c for c in viable_candidates if c['is_sig_10']]
        
        selected = None
        
        if sig_candidates:
            # Seleciona o que tem maior ganho de lucro absoluto entre os estatisticamente significativos
            selected = max(sig_candidates, key=lambda x: x['profit_diff'])
            reason_prefix = f"Escalar {selected['group']} para 100% (Recomendado - Estatisticamente Significativo)."
            reason_desc = (
                f"O grupo {selected['group']} gerou um aumento de R$ {selected['profit_diff']:,.2f} (+{selected['profit_pct_diff']*100:.1f}%) "
                f"no Lucro Líquido em relação ao controle, com significância estatística robusta (p-value = {selected['p_value_profit']:.4f}). "
                f"O ROI deste grupo é de {selected['roi']*100:.1f}%."
            )
        elif marginal_candidates:
            selected = max(marginal_candidates, key=lambda x: x['profit_diff'])
            reason_prefix = f"Escalar {selected['group']} para 100% (Marginalmente Significativo)."
            reason_desc = (
                f"O grupo {selected['group']} apresentou melhora de R$ {selected['profit_diff']:,.2f} (+{selected['profit_pct_diff']*100:.1f}%) "
                f"no Lucro Líquido com indícios de significância (p-value = {selected['p_value_profit']:.4f}). "
                f"A recomendação é escalar com monitoramento contínuo."
            )
        else:
            # Sem resultado de significância forte, mas com tendência positiva clara (> 5% de melhoria de margem)
            best_by_profit = max(viable_candidates, key=lambda x: x['profit_diff'])
            
            # Se o ganho de lucro nominal for superior a 5% e o ROI for saudável, escala-se com cautela
            if best_by_profit['profit_pct_diff'] > 0.05:
                selected = best_by_profit
                reason_prefix = f"Escalar {selected['group']} para 100% com cautela (Ausência de Significância Estatística)."
                reason_desc = (
                    f"O grupo {selected['group']} apresentou uma tendência positiva de aumento de R$ {selected['profit_diff']:,.2f} "
                    f"(+{selected['profit_pct_diff']*100:.1f}%) no Lucro Líquido, mas a diferença não é estatisticamente significativa "
                    f"(p-value = {selected['p_value_profit']:.4f}), indicando risco de que o resultado seja ruído. "
                    f"Como o ganho prático é relevante e o ROI é de {selected['roi']*100:.1f}%, recomenda-se escalar com monitoramento próximo."
                )
            else:
                # O ganho de lucro é muito pequeno e não significativo. Mantém-se o controle.
                recommendation['winner_group'] = control_group
                recommendation['decision'] = f"Manter o Controle ({control_group}) em 100%"
                recommendation['reason'] = (
                    f"Embora algumas variantes tenham mostrado leve melhora nominal, nenhuma diferença foi estatisticamente significativa "
                    f"e os ganhos foram muito pequenos (< 5%). Recomenda-se manter o grupo de controle para evitar custos adicionais de cashback."
                )
                recommendation['details'].append("Os grupos de tratamento mostraram melhora insignificante e sem relevância estatística.")
                
        if selected:
            recommendation['winner_group'] = selected['group']
            recommendation['decision'] = f"Escalar {selected['group']} para 100% do tráfego"
            recommendation['reason'] = f"{reason_prefix} {reason_desc}"
            recommendation['details'].append(f"Aumento absoluto de Lucro Líquido: R$ {selected['profit_diff']:,.2f}")
            recommendation['details'].append(f"ROI da variante vencedora: {selected['roi']*100:.1f}% (vs {control_roi*100:.1f}% do controle)")
            
    # Incluir dados dos outros candidatos no retorno para exibição nos relatórios
    recommendation['candidates_raw'] = candidates
    return recommendation
