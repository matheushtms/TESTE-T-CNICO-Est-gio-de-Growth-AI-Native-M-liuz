# Méliuz Cashback A/B Test Analyzer 💰

Esta é uma solução modular, estatisticamente rigorosa e reutilizável para a análise automatizada de testes A/B de cashback do **Méliuz**. O sistema calcula métricas financeiras essenciais (Lucro Líquido, ROI, Unit Economics), realiza testes de hipóteses estatísticas diárias (Welch's T-Test e Mann-Whitney U-Test) para validar se os resultados são estatisticamente significativos, gera relatórios executivos em Markdown e registra os resultados em uma planilha do Google Sheets e em um histórico CSV local.

A solução também acompanha um **Dashboard visual em Streamlit** e um **guia para agentes de IA** para interação em linguagem natural.

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.10 ou superior** instalado na sua máquina.

### 2. Instalação das Dependências
Clone este repositório, navegue até a pasta do projeto e instale as bibliotecas necessárias:

```bash
# Criar um ambiente virtual (recomendado)
python -m venv .venv
.venv\Scripts\activate      # No Windows (PowerShell)
# source .venv/bin/activate # No Linux/macOS

# Instalar dependências
pip install -r requirements.txt
```

### 3. Rodando o CLI (Análise Principal)
Você pode rodar a análise de qualquer dataset que siga o schema definido passando o caminho do arquivo no parâmetro `--file`:

```bash
# Rodar análise do Parceiro A
python main.py --file data/parceiro_a.csv

# Rodar análise do Parceiro B com nome e descrição customizados para o histórico
python main.py --file data/parceiro_b.csv --name "Parceiro B - Campanha de Verão" --desc "Testando taxas agressivas de cashback"
```

A CLI exibirá um resumo executivo direto no terminal e criará um relatório Markdown detalhado e apresentável a gestores na pasta `reports/` (ex: `reports/relatorio_parceiro_a.md`).

### 4. Rodando o Dashboard Visual (Streamlit)
Para uma experiência visual interativa com gráficos de tendências, séries temporais acumuladas de GMV, distribuições de lucro e tabela interativa de testes estatísticos:

```bash
streamlit run src/dashboard.py
```

O dashboard será aberto no seu navegador padrão (geralmente em `http://localhost:8501`). Nele, você pode fazer upload de qualquer arquivo de teste A/B novo e ver os resultados dinamicamente.

---

## 📊 Estrutura de Arquivos e Pastas

```text
growth-ab-test/
├── data/                       # Armazena os CSVs dos parceiros (A, B e C)
├── reports/                    # Relatórios executivos gerados em Markdown (.md)
├── output/                     # Histórico consolidado em CSV local (historico_testes.csv)
├── prompts/                    # Instruções estruturadas para uso por Agentes de IA
│   └── instructions_for_ai.md
├── src/                        # Código-fonte modular
│   ├── loader.py               # Carregamento e limpeza de dados monetários (R$ -> float)
│   ├── validator.py            # Validação do schema e consistência dos registros
│   ├── metrics.py              # Cálculo de métricas gerais e séries temporais diárias
│   ├── analyzer.py             # Motores de testes estatísticos e decisão heurística
│   ├── report_generator.py     # Geração automatizada do relatório executivo Markdown
│   ├── sheets.py               # Sincronização com CSV e integração com API do Google Sheets
│   ├── dashboard.py            # Interface gráfica em Streamlit
│   └── mock_generator.py       # Gerador de dados fictícios para testes locais
├── tests/                      # Testes automatizados unitários
│   └── test_pipeline.py
├── main.py                     # CLI principal (Entrypoint)
├── requirements.txt            # Dependências do Python
├── .env.example                # Template de variáveis de ambiente para o Google Sheets
└── README.md                   # Esta documentação
```

---

## 🛠️ Reuso para Qualquer Novo Dataset (Sem alterar o código)

A pipeline foi projetada de forma genérica. Para analisar um novo teste A/B:
1. Garanta que o novo arquivo CSV siga o mesmo schema exigido:
   - **Data**: Data do registro (`YYYY-MM-DD`).
   - **Grupos de usuários**: Identificador do grupo (ex: `Grupo 1`, `Grupo 2`, `Grupo 3`).
   - **Parceiro**: Nome do parceiro.
   - **compradores**: Quantidade de compradores únicos no dia.
   - **comissão**: Comissão recebida (formato string com `R$`).
   - **cashback**: Cashback distribuído aos usuários (formato string com `R$`).
   - **vendas totais**: GMV gerado (formato string com `R$`).
2. Rode o comando passando o caminho do novo arquivo:
   `python main.py --file caminho/do/seu/novo_arquivo.csv`
3. A pipeline validará o schema, identificará os grupos e executará os testes estatísticos e de decisão de forma 100% autônoma!

---

## 🔬 Metodologia de Análise de Growth

Muitos testes A/B limitam-se a comparar o somatório do GMV ou volume de compradores, ignorando os custos envolvidos. A nossa solução aplica uma tomada de decisão focada em **lucro líquido sustentável** e **estatística rigorosa**:

### 1. Modelagem das Métricas
- **Lucro Líquido (Receita - Custo)**: `Comissão Total - Cashback Total`. O cashback é um custo de incentivo de marketing que reduz a margem do Méliuz. Aumentar o GMV gerando prejuízo operacional não é escalável.
- **ROI (Retorno sobre Investimento)**: `Lucro Líquido ÷ Cashback Total`. Mede a eficiência operacional de cada real investido em cashback.
- **Unit Economics**: Calcula as médias por comprador único (`GMV por comprador`, `Cashback por comprador` e `Lucro por comprador`).

### 2. Validação Estatística (Hypothesis Testing)
Tratando os registros diários como observações independentes, aplicamos testes estatísticos na distribuição de lucro e ROI das variantes contra a base de controle (`Grupo 1`):
- **T-Test de Welch (Student para variâncias desiguais)**: Compara a média diária de lucro líquido das variantes, medindo a probabilidade (p-value) de a variação observada ser ruído estatístico.
- **Teste de Mann-Whitney U**: Teste não-paramétrico que serve como fallback robusto para distribuições de vendas diárias que não seguem uma curva normal (presença de picos e sazonalidades de fim de semana).

### 3. Motor de Decisão (Decision Heuristic)
A decisão de recomendar a variante vencedora é orientada por uma árvore de decisão de Growth:
1. **Qualificação como Candidato**: O grupo de tratamento precisa ter Lucro Líquido total maior que o controle (`lucro_diff > 0`) e manter um ROI positivo.
2. **Avaliação de Significância**:
   - Se o candidato possui ganho estatisticamente significativo ($p < 0.05$), ele é a recomendação principal para **Escalar para 100%**.
   - Se possui ganho de tendência forte mas sem significância estatística, avalia-se o tamanho do ganho nominal. Se o ganho de lucro líquido for maior que 5% e o ROI for saudável, recomenda-se escalar com **cautela e monitoramento**; caso contrário, recomenda-se **Manter o Controle (Grupo 1)** para mitigar riscos de queima de caixa.
   - Variantes com lucro menor que o controle ou ROI negativo são descartadas.

---

## 📝 Integração com o Google Sheets

A aplicação grava cada novo teste analisado no histórico de experimentos. Por padrão, ela grava em um arquivo CSV local em `output/historico_testes.csv`. Caso queira salvar diretamente na planilha do Google Sheets, a solução oferece dois métodos:

### Método 1: Integração via Google Apps Script Web App (Recomendado - Sem Google Cloud)
Ideal por ser extremamente simples e não exigir nenhuma configuração no Google Cloud Console:
1. Crie uma planilha no seu **Google Drive**.
2. No menu superior da planilha, vá em **Extensões** > **Apps Script**.
3. Apague o código padrão e cole o script localizado na seção do manual do desenvolvedor (função `doPost(e)` que recebe o JSON de testes e insere na planilha).
4. Clique em **Implantar** > **Nova implantação** no canto superior direito.
5. Selecione o tipo de implantação como **App da Web** (Web App). Configure:
   - **Executar como:** `Eu` (sua conta Google)
   - **Quem tem acesso:** `Qualquer pessoa` (permite que o script envie os dados via requisição HTTP)
6. Clique em **Implantar**, conceda as autorizações necessárias e copie a **URL do App da Web** gerada.
7. Cole a URL no arquivo `.env` na raiz do projeto:
   `GOOGLE_WEB_APP_URL=sua_url_aqui`

---

### Método 2: Conta de Serviço clássica (Com Google Cloud)
Caso prefira usar o fluxo tradicional do Google Cloud Console:
1. Crie uma planilha no seu **Google Drive** e copie o ID da planilha localizado na URL (entre `/d/` e `/edit`).
2. Adicione o ID no arquivo `.env` na raiz do projeto:
   `GOOGLE_SHEET_ID=seu_sheet_id_aqui`
3. Crie um projeto no **Google Cloud Console**, ative a **Google Sheets API** e a **Google Drive API**.
4. Crie uma **Service Account** (Conta de Serviço), gere uma chave no formato **JSON**, faça o download e salve-a na raiz do projeto com o nome `service_account.json`.
5. Compartilhe a sua planilha do Google Sheets com o e-mail da Conta de Serviço gerada dando permissão de **Editor**.

---

*Observação: Caso nenhum dos parâmetros acima esteja presente no arquivo `.env`, o sistema executará normalmente e fará o fallback de segurança salvando localmente em formato CSV.*
