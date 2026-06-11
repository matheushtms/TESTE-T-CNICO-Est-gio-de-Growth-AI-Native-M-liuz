import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente atualizadas
load_dotenv(override=True)

# Importa o código do pipeline local
from loader import load_data, clean_currency
from validator import validate_data
from metrics import calculate_aggregate_metrics, calculate_daily_metrics
from analyzer import perform_statistical_tests, make_decision
from report_generator import generate_markdown_report
from sheets import register_test_result

st.set_page_config(
    page_title="Méliuz Cashback A/B Test Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajustes de estilo premium (inspirado no design do usuário)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }
    
    h1 {
        background: linear-gradient(135deg, #ff0055 0%, #a200ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px !important;
    }
    
    /* Card de Métricas Premium */
    [data-testid="metric-container"] {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        border: 1px solid rgba(128, 128, 128, 0.15);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
        border-color: #ff0055;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        color: var(--text-color);
        opacity: 0.8;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
    }

    /* Botão de gravação premium */
    div.stButton > button {
        background: linear-gradient(135deg, #ff0055 0%, #a200ff 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(255, 0, 85, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 0, 85, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares para gerar gráficos dinâmicos com Plotly
def create_daily_profit_chart(df_daily):
    fig = go.Figure()
    colors = {
        'Grupo 1': '#7b2cbf', # Controle (roxo)
        'Grupo 2': '#ff0055', # Tratamento (rosa)
        'Grupo 3': '#00b4d8'  # Tratamento (azul)
    }
    fill_colors = {
        'Grupo 1': 'rgba(123, 44, 191, 0.08)',
        'Grupo 2': 'rgba(255, 0, 85, 0.08)',
        'Grupo 3': 'rgba(0, 180, 216, 0.08)'
    }
    
    df_pivot = df_daily.pivot(index='data', columns='grupo', values='lucro_diario')
    
    for col in df_pivot.columns:
        fig.add_trace(go.Scatter(
            x=df_pivot.index,
            y=df_pivot[col],
            mode='lines',
            name=col,
            line=dict(color=colors.get(col, '#9d4edd'), width=3, shape='spline'),
            fill='tozeroy',
            fillcolor=fill_colors.get(col, 'rgba(157, 78, 221, 0.08)'),
            hovertemplate="<b>%{x}</b><br>" + f"{col}: R$ %{{y:,.2f}}<extra></extra>"
        ))
        
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)', tickformat='%d/%m'),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)', tickprefix='R$ '),
        font=dict(family='Outfit, sans-serif')
    )
    return fig

def create_cumulative_gmv_chart(df_daily):
    fig = go.Figure()
    colors = {
        'Grupo 1': '#7b2cbf',
        'Grupo 2': '#ff0055',
        'Grupo 3': '#00b4d8'
    }
    fill_colors = {
        'Grupo 1': 'rgba(123, 44, 191, 0.08)',
        'Grupo 2': 'rgba(255, 0, 85, 0.08)',
        'Grupo 3': 'rgba(0, 180, 216, 0.08)'
    }
    
    df_pivot = df_daily.pivot(index='data', columns='grupo', values='vendas_totais')
    df_cum = df_pivot.cumsum()
    
    for col in df_cum.columns:
        fig.add_trace(go.Scatter(
            x=df_cum.index,
            y=df_cum[col],
            mode='lines',
            name=col,
            line=dict(color=colors.get(col, '#9d4edd'), width=3, shape='spline'),
            fill='tozeroy',
            fillcolor=fill_colors.get(col, 'rgba(157, 78, 221, 0.08)'),
            hovertemplate="<b>%{x}</b><br>" + f"{col}: R$ %{{y:,.2f}}<extra></extra>"
        ))
        
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)', tickformat='%d/%m'),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)', tickprefix='R$ '),
        font=dict(family='Outfit, sans-serif')
    )
    return fig

def create_profit_donut_chart(agg_metrics):
    colors = {
        'Grupo 1': '#7b2cbf',
        'Grupo 2': '#ff0055',
        'Grupo 3': '#00b4d8'
    }
    color_list = [colors.get(g, '#9d4edd') for g in agg_metrics.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=agg_metrics.index,
        values=agg_metrics['lucro_total'],
        hole=.6,
        marker=dict(colors=color_list, line=dict(color='rgba(128, 128, 128, 0.2)', width=1)),
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Lucro: R$ %{value:,.2f}<br>Participação: %{percent}<extra></extra>"
    )])
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit, sans-serif'),
        title=dict(text="Participação no Lucro Líquido Total", font=dict(size=16, family='Outfit, sans-serif'), x=0.5, xanchor='center')
    )
    return fig

def create_roi_bar_chart(agg_metrics):
    colors = {
        'Grupo 1': '#7b2cbf',
        'Grupo 2': '#ff0055',
        'Grupo 3': '#00b4d8'
    }
    color_list = [colors.get(g, '#9d4edd') for g in agg_metrics.index]
    
    fig = go.Figure(data=[go.Bar(
        x=agg_metrics.index,
        y=agg_metrics['roi'] * 100,
        marker_color=color_list,
        marker_line=dict(color='rgba(128,128,128,0.2)', width=1),
        hovertemplate="<b>%{x}</b><br>ROI: %{y:.1f}%<extra></extra>"
    )])
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)', ticksuffix='%'),
        font=dict(family='Outfit, sans-serif'),
        title=dict(text="Eficiência de Retorno sobre Investimento (ROI)", font=dict(size=16, family='Outfit, sans-serif'), x=0.5, xanchor='center')
    )
    return fig

st.title("💰 Méliuz Cashback A/B Test Analyzer")
st.markdown("Ferramenta para análise automatizada de testes A/B de cashback com fundamentação estatística e tomada de decisão de Growth.")

# Controles da barra lateral
st.sidebar.header("📁 Importar Dataset")

# Opção 1: Escolher conjuntos de dados mock se disponíveis
data_dir = "data"
mock_files = []
if os.path.exists(data_dir):
    mock_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

option = st.sidebar.selectbox(
    "Escolha o dataset para analisar:",
    ["Carregar novo arquivo (CSV)"] + [f"data/{f}" for f in mock_files]
)

uploaded_file = None
if option == "Carregar novo arquivo (CSV)":
    uploaded_file = st.sidebar.file_uploader("Upload do arquivo CSV", type=["csv"])
else:
    uploaded_file = option

# Formulário de detalhes do teste
st.sidebar.markdown("---")
st.sidebar.header("📝 Detalhes do Teste")
test_name = st.sidebar.text_input("Nome do Teste", value="Teste Cashback")
test_description = st.sidebar.text_area("Descrição", value="Avaliação de aumento de cashback para otimização de lucro líquido.")

if uploaded_file is not None:
    try:
        # Carrega os dados
        if isinstance(uploaded_file, str):
            # É um caminho de arquivo
            df = load_data(uploaded_file)
            file_name = os.path.basename(uploaded_file)
        else:
            # É um objeto de arquivo enviado
            # Salva o arquivo temporário para processamento
            temp_path = "temp_uploaded.csv"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            df = load_data(temp_path)
            file_name = uploaded_file.name
            
        # Executa as validações
        is_valid, errors, warnings = validate_data(df)
        
        if not is_valid:
            st.error("🚨 Erros críticos de validação encontrados no arquivo:")
            for err in errors:
                st.write(f"- {err}")
        else:
            # Mostra avisos, se houver
            if warnings:
                with st.expander("⚠️ Avisos de Validação (Não-Críticos)"):
                    for warn in warnings:
                        st.markdown(f"- {warn}")
            
            # Executa os cálculos
            partner = df['parceiro'].iloc[0]
            agg_metrics = calculate_aggregate_metrics(df)
            df_daily = calculate_daily_metrics(df)
            stat_tests = perform_statistical_tests(df_daily)
            decision = make_decision(agg_metrics, stat_tests)
            
            # --- LAYOUT DO PAINEL ---
            
            # Banner principal para a decisão
            winner = decision['winner_group']
            decision_text = decision['decision']
            reason = decision['reason']
            
            if "Escalar" in decision_text:
                st.success(f"🎯 **RECOMENDAÇÃO: {decision_text}**\n\n{reason}")
            else:
                st.info(f"⚖️ **RECOMENDAÇÃO: {decision_text}**\n\n{reason}")
                
            # Cartões de KPI
            st.subheader("📊 Métricas de Negócio Consolidadas")
            
            # Queremos exibir as principais métricas do controle e do vencedor, ou de todos os grupos lado a lado
            groups = list(agg_metrics.index)
            cols = st.columns(len(groups))
            
            for i, group in enumerate(groups):
                row = agg_metrics.loc[group]
                roi_pct = f"{row['roi']*100:.1f}%"
                profit_str = f"R$ {row['lucro_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                gmv_str = f"R$ {row['gmv_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                buyers_str = f"{int(row['compradores_total']):,}".replace(",", ".")
                cashback_ratio = f"{row['cashback_sobre_comissao']*100:.1f}%"
                
                with cols[i]:
                    st.markdown(f"### **{group}**")
                    st.metric(label="Lucro Líquido", value=profit_str)
                    st.metric(label="ROI da Variante", value=roi_pct)
                    st.metric(label="GMV Total", value=gmv_str)
                    st.metric(label="Compradores Únicos", value=buyers_str)
                    st.metric(label="Cashback / Comissão", value=cashback_ratio)
            
            # Seção de gráficos
            st.markdown("---")
            st.subheader("📈 Análise Visual e Tendências Diárias")
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown("#### Lucro Diário por Variante")
                st.plotly_chart(create_daily_profit_chart(df_daily), use_container_width=True)
                
            with chart_col2:
                st.markdown("#### GMV Diário Acumulado")
                st.plotly_chart(create_cumulative_gmv_chart(df_daily), use_container_width=True)
                
            # Gráficos agregados
            st.markdown("---")
            st.subheader("📊 Métricas Acumuladas Consolidadas")
            
            bar_col1, bar_col2 = st.columns(2)
            
            with bar_col1:
                st.plotly_chart(create_profit_donut_chart(agg_metrics), use_container_width=True)
                
            with bar_col2:
                st.plotly_chart(create_roi_bar_chart(agg_metrics), use_container_width=True)
            
            # Tabela de significância estatística
            st.markdown("---")
            st.subheader("🔬 Resultados dos Testes de Hipóteses")
            
            for comp_name, comp in stat_tests.items():
                st.markdown(f"#### Comparação: **{comp_name}**")
                
                rows_data = []
                for var, test_info in comp['metrics'].items():
                    rows_data.append({
                        "Métrica": test_info['label'],
                        "Média Controle": f"{test_info['control_mean']:,.2f}",
                        "Média Tratamento": f"{test_info['treatment_mean']:,.2f}",
                        "Diferença": f"{test_info['mean_diff']:+,.2f}",
                        "Variação %": f"{test_info['pct_diff']*100:+.1f}%",
                        "p-value (Welch T)": f"{test_info['t_p_value']:.4f}",
                        "Significativo (95%)": "✅ Sim" if test_info['significant_t_05'] else "❌ Não"
                    })
                st.table(pd.DataFrame(rows_data))
                
            # Geração de relatório executivo
            st.markdown("---")
            st.subheader("📄 Relatório Executivo Gerado")
            
            report_md = generate_markdown_report(df, agg_metrics, stat_tests, decision)
            st.markdown(report_md)
            
            # Botão de download do relatório
            report_filename = f"relatorio_{partner.lower().replace(' ', '_')}.md"
            st.download_button(
                label="📥 Baixar Relatório em Markdown",
                data=report_md,
                file_name=report_filename,
                mime="text/markdown"
            )
            
            # Registro do teste na planilha/CSV
            st.sidebar.markdown("---")
            st.sidebar.subheader("💾 Salvar Resultado")
            if st.sidebar.button("Registrar na Planilha"):
                period = f"{df['data'].min()} a {df['data'].max()}"
                winner_group = decision['winner_group']
                winner_roi = agg_metrics.loc[winner_group, 'roi'] if winner_group else 0.0
                winner_profit = agg_metrics.loc[winner_group, 'lucro_total'] if winner_group else 0.0
                
                # Trunca a descrição para legibilidade na planilha
                desc_summary = decision['reason'][:200] + "..." if len(decision['reason']) > 200 else decision['reason']
                
                local_ok, sheet_ok = register_test_result(
                    test_name,
                    partner,
                    period,
                    winner_group,
                    winner_roi,
                    winner_profit,
                    decision_text,
                    test_description + " | " + desc_summary
                )
                
                if local_ok:
                    st.sidebar.success("Gravado em output/historico_testes.csv!")
                
                # Feedback detalhado para a integração do Google Sheets
                load_dotenv(override=True)
                sheet_id = os.getenv("GOOGLE_SHEET_ID")
                creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
                web_app_url = os.getenv("GOOGLE_WEB_APP_URL")
                
                if sheet_ok:
                    st.sidebar.success("Enviado para o Google Sheets!")
                elif web_app_url and web_app_url != "sua_url_do_web_app_aqui":
                    st.sidebar.error("Erro ao enviar para o Google Sheets via Web App API. Verifique a URL do script ou sua conexão.")
                elif not sheet_id:
                    st.sidebar.info("Aviso: GOOGLE_SHEET_ID não configurado no arquivo .env.")
                elif not os.path.exists(creds_file):
                    st.sidebar.warning("Aviso: Arquivo 'service_account.json' de credenciais não encontrado na raiz do projeto.")
                else:
                    st.sidebar.error("Erro ao enviar para Google Sheets. Verifique o ID da planilha e se ela está compartilhada com o e-mail da service account.")
                    
            # Limpa o arquivo temporário
            if not isinstance(uploaded_file, str) and os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {str(e)}")
        st.info("Certifique-se de que o arquivo segue o schema obrigatório de colunas.")
else:
    st.info("Aguardando importação de dataset na barra lateral.")
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80", caption="Análise Estatística de Crescimento", width=600)
