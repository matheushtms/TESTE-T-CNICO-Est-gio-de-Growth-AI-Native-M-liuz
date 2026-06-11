# Méliuz Cashback A/B Test Analyzer 💰

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-Planilha%20Oficial-34A853?logo=googlesheets&logoColor=white)](https://docs.google.com/spreadsheets/d/1QznZnlbodHLE-JAENu0m6w9VgoFHZloDghs2gGNX3YI/edit?usp=sharing)
[![Statistical Tests](https://img.shields.io/badge/Estatística-Welch%20T--Test%20%7C%20Mann--Whitney-orange)](https://en.wikipedia.org/wiki/A/B_testing)

Esta é uma solução modular, estatisticamente rigorosa e reutilizável para a análise automatizada de testes A/B de cashback do **Méliuz**. O sistema calcula métricas financeiras essenciais (Lucro Líquido, ROI, Unit Economics), realiza testes de hipóteses estatísticas diárias (Welch's T-Test e Mann-Whitney U-Test) para validar se os resultados são estatisticamente significativos, gera relatórios executivos em Markdown e registra os resultados em uma planilha do Google Sheets e em um histórico CSV local.

A solução também acompanha um **Dashboard visual em Streamlit** e um **guia para agentes de IA** para interação em linguagem natural.

---

## 🔗 Recursos Principais e Planilhas

> [!TIP]
> * **Planilha Oficial de Acompanhamento (Google Sheets - Acesso de Leitura):** [Acesse os resultados e histórico dos experimentos](https://docs.google.com/spreadsheets/d/1QznZnlbodHLE-JAENu0m6w9VgoFHZloDghs2gGNX3YI/edit?usp=sharing)
> * **Histórico CSV Local (Preenchido):** [historico_testes.csv](./output/historico_testes.csv)
> * **Instruções para Agentes de IA:** [instructions_for_ai.md](./prompts/instructions_for_ai.md)

---

## 📄 Relatórios dos Testes A/B Gerados (Resultados Reais)

Abaixo estão os resumos executivos e tabelas de resultados reais consolidados dos testes A/B gerados pelo pipeline para os três parceiros:

### 🤝 Parceiro A
* **Período do Experimento:** 01/01/2011 a 02/04/2011 (92 dias)
* **Relatório Completo:** [relatorio_parceiro_a.md](./reports/relatorio_parceiro_a.md)
* **Recomendação Final:** **Manter o Controle (Grupo 1) em 100%**
* **Justificativa Estatística:** Nenhuma das variantes superou o controle em lucro líquido total ou apresentou ROI sustentável. O Grupo 3 causou redução de lucro estatisticamente significativa ($p < 0.05$).

#### Tabela de Resultados Consolidados (Parceiro A)
| Variante | Compradores | GMV Total | Comissão | Cashback | Lucro Líquido | ROI |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Grupo 1 (Controle)** | 9.633 | R$ 5.605.173,00 | R$ 638.135,00 | R$ 233.424,00 | **R$ 404.711,00** | **173.4%** |
| **Grupo 2** | 10.814 | R$ 6.423.096,00 | R$ 728.178,00 | R$ 370.659,00 | **R$ 357.519,00** | **96.5%** |
| **Grupo 3** | 11.410 | R$ 6.785.856,00 | R$ 767.887,00 | R$ 503.600,00 | **R$ 264.287,00** | **52.5%** |

---

### 🤝 Parceiro B
* **Período do Experimento:** 01/05/2011 a 30/06/2011 (61 dias)
* **Relatório Completo:** [relatorio_parceiro_b.md](./reports/relatorio_parceiro_b.md)
* **Recomendação Final:** **Manter o Controle (Grupo 1) em 100%**
* **Justificativa Estatística:** Ambas as variantes de tratamento causaram queda acentuada e estatisticamente significativa no lucro diário ($p < 0.05$).

#### Tabela de Resultados Consolidados (Parceiro B)
| Variante | Compradores | GMV Total | Comissão | Cashback | Lucro Líquido | ROI |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Grupo 1 (Controle)** | 7.990 | R$ 4.093.818,00 | R$ 450.321,00 | R$ 163.751,00 | **R$ 286.570,00** | **175.0%** |
| **Grupo 2** | 5.452 | R$ 2.863.019,00 | R$ 314.935,00 | R$ 171.778,00 | **R$ 143.157,00** | **83.3%** |
| **Grupo 3** | 5.029 | R$ 2.629.963,00 | R$ 289.290,00 | R$ 236.697,00 | **R$ 52.593,00** | **22.2%** |

---

### 🤝 Parceiro C
* **Período do Experimento:** 01/07/2011 a 14/08/2011 (45 dias)
* **Relatório Completo:** [relatorio_parceiro_c.md](./reports/relatorio_parceiro_c.md)
* **Recomendação Final:** **Manter o Controle (Grupo 1) em 100%**
* **Justificativa Estatística:** O Grupo 2 reduziu o lucro líquido a zero (ROI de 0.0%), com uma queda diária de lucro estatisticamente significativa ($p < 0.05$).

#### Tabela de Resultados Consolidados (Parceiro C)
| Variante | Compradores | GMV Total | Comissão | Cashback | Lucro Líquido | ROI |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Grupo 1 (Controle)** | 4.549 | R$ 1.738.460,00 | R$ 121.693,00 | R$ 86.924,00 | **R$ 34.769,00** | **40.0%** |
| **Grupo 2** | 4.522 | R$ 1.685.235,00 | R$ 117.967,00 | R$ 117.967,00 | **R$ 0,00** | **0.0%** |

---

## ⚙️ A Solução (Arquitetura e Scripts)

A solução está estruturada de forma modular para fácil manutenção e reuso. Os principais arquivos e suas respectivas responsabilidades são:

* **Entrypoint do Sistema:**
  * 🖥️ [main.py](./main.py): CLI principal que orquestra todo o fluxo, desde o carregamento dos dados até a gravação na planilha.
* **Componentes de Código (em [src/](./src)):**
  * 📥 [loader.py](./src/loader.py): Limpeza de moedas (R$ -> float) e carregamento inicial dos datasets CSV.
  * 🛡️ [validator.py](./src/validator.py): Validador de consistência (valida colunas obrigatórias, formatos e integridade dos dados).
  * 📈 [metrics.py](./src/metrics.py): Módulo para cálculo de Lucro Líquido, ROI e métricas de Unit Economics agregadas ou diárias.
  * 🔬 [analyzer.py](./src/analyzer.py): Motor estatístico que executa os testes de significância (Welch's T-Test e Mann-Whitney U-Test) e aplica a árvore heurística de decisão de Growth.
  * ✍️ [report_generator.py](./src/report_generator.py): Exportador de relatórios executivos estruturados em Markdown.
  * 🔌 [sheets.py](./src/sheets.py): Integração para gravação dos resultados localmente (CSV) e no Google Sheets (via Apps Script Web App ou Conta de Serviço).
  * 📊 [dashboard.py](./src/dashboard.py): Dashboard interativo em Streamlit para exploração visual das métricas e distribuições.
  * 🎲 [mock_generator.py](./src/mock_generator.py): Gerador opcional de datasets de teste sintéticos.

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
   * **Data**: Data do registro (`YYYY-MM-DD`).
   * **Grupos de usuários**: Identificador do grupo (ex: `Grupo 1`, `Grupo 2`, `Grupo 3`).
   * **Parceiro**: Nome do parceiro.
   * **compradores**: Quantidade de compradores únicos no dia.
   * **comissão**: Comissão recebida (formato string com `R$`).
   * **cashback**: Cashback distribuído aos usuários (formato string com `R$`).
   * **vendas totais**: GMV gerado (formato string com `R$`).
2. Rode o comando passando o caminho do novo arquivo:
   ```bash
   python main.py --file caminho/do/seu/novo_arquivo.csv
   ```
3. A pipeline validará o schema, identificará os grupos e executará os testes estatísticos e de decisão de forma 100% autônoma!

---

## 🔬 Metodologia de Análise de Growth

Muitos testes A/B limitam-se a comparar o somatório do GMV ou volume de compradores, ignorando os custos envolvidos. A nossa solução aplica uma tomada de decisão focada em **lucro líquido sustentável** e **estatística rigorosa**:

### 1. Modelagem das Métricas
* **Lucro Líquido (Receita - Custo):** `Comissão Total - Cashback Total`. O cashback é um custo de incentivo de marketing que reduz a margem do Méliuz. Aumentar o GMV gerando prejuízo operacional não é escalável.
* **ROI (Retorno sobre Investimento):** `Lucro Líquido ÷ Cashback Total`. Mede a eficiência operacional de cada real investido em cashback.
* **Unit Economics:** Calcula as médias por comprador único (`GMV por comprador`, `Cashback por comprador` e `Lucro por comprador`).

### 2. Validação Estatística (Hypothesis Testing)
Tratando os registros diários como observações independentes, aplicamos testes estatísticos na distribuição de lucro e ROI das variantes contra a base de controle (`Grupo 1`):
* **T-Test de Welch (Student para variâncias desiguais):** Compara a média diária de lucro líquido das variantes, medindo a probabilidade (p-value) de a variação observada ser ruído estatístico.
* **Teste de Mann-Whitney U:** Teste não-paramétrico que serve como fallback robusto para distribuições de vendas diárias que não seguem uma curva normal (presença de picos e sazonalidades de fim de semana).

### 3. Motor de Decisão (Decision Heuristic)
A decisão de recomendar a variante vencedora é orientada por uma árvore de decisão de Growth:
1. **Qualificação como Candidato:** O grupo de tratamento precisa ter Lucro Líquido total maior que o controle (`lucro_diff > 0`) e manter um ROI positivo.
2. **Avaliação de Significância:**
   * Se o candidato possui ganho estatisticamente significativo ($p < 0.05$), ele é a recomendação principal para **Escalar para 100%**.
   * Se possui ganho de tendência forte mas sem significância estatística, avalia-se o tamanho do ganho nominal. Se o ganho de lucro líquido for maior que 5% e o ROI for saudável, recomenda-se escalar com **cautela e monitoramento**; caso contrário, recomenda-se **Manter o Controle (Grupo 1)** para mitigar riscos de queima de caixa.
   * Variantes com lucro menor que o controle ou ROI negativo são descartadas.

---

## 📝 Integração com o Google Sheets

A aplicação grava cada novo teste analisado no histórico de experimentos. Por padrão, ela grava em um arquivo CSV local em `output/historico_testes.csv`. Caso queira salvar diretamente na planilha do Google Sheets, a solução oferece suporte à gravação em tempo real na planilha oficial do projeto:

> [!IMPORTANT]
> A planilha oficial configurada para este projeto é a seguinte:
> **Planilha de Histórico:** [Cópia de Historico de Testes A/B - Meliuz (Google Sheets)](https://docs.google.com/spreadsheets/d/1QznZnlbodHLE-JAENu0m6w9VgoFHZloDghs2gGNX3YI/edit?usp=sharing)
>
> Ela é alimentada de forma transparente por qualquer um dos dois métodos a seguir.

### Método 1: Integração via Google Apps Script Web App (Recomendado - Sem Google Cloud)

Ideal por ser extremamente simples e não exigir nenhuma configuração no Google Cloud Console:
1. Abra a planilha oficial no seu navegador.
2. No menu superior da planilha, vá em **Extensões** > **Apps Script**.
3. Apague o código padrão e cole o script localizado abaixo (função `doPost(e)` que recebe o JSON de testes e insere na planilha):
   ```javascript
   function doPost(e) {
     var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
     var data = JSON.parse(e.postData.contents);
     
     // Adicionar linha
     sheet.appendRow([
       data.test_name,
       data.partner,
       data.date_str,
       data.period,
       data.winner,
       data.roi_str,
       data.profit_str,
       data.decision,
       data.description
     ]);
     
     return ContentService.createTextOutput(JSON.stringify({status: "success"}))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```
4. Clique em **Implantar** > **Nova implantação** no canto superior direito.
5. Selecione o tipo de implantação como **App da Web** (Web App). Configure:
   * **Executar como:** `Eu` (sua conta Google)
   * **Who has access:** `Qualquer pessoa` (permite que o script envie os dados via requisição HTTP)
6. Clique em **Implantar**, conceda as autorizações necessárias e copie a **URL do App da Web** gerada.
7. Cole a URL no arquivo `.env` na raiz do projeto:
   ```env
   GOOGLE_WEB_APP_URL=sua_url_do_web_app_gerada_aqui
   ```

---

### Método 2: Conta de Serviço clássica (Com Google Cloud)

Caso prefira usar o fluxo tradicional do Google Cloud Console:
1. Use o ID da planilha oficial: `1QznZnlbodHLE-JAENu0m6w9VgoFHZloDghs2gGNX3YI`.
2. Adicione o ID no arquivo `.env` na raiz do projeto:
   ```env
   GOOGLE_SHEET_ID=1QznZnlbodHLE-JAENu0m6w9VgoFHZloDghs2gGNX3YI
   ```
3. Crie um projeto no **Google Cloud Console**, ative a **Google Sheets API** e a **Google Drive API**.
4. Crie uma **Service Account** (Conta de Serviço), gere uma chave no formato **JSON**, faça o download e salve-a na raiz do projeto com o nome `service_account.json`.
5. Compartilhe a planilha oficial com o e-mail da Conta de Serviço gerada dando permissão de **Editor**.

---

*Observação: Caso nenhum dos parâmetros acima esteja presente no arquivo `.env`, o sistema executará normalmente e fará o fallback de segurança salvando localmente em formato CSV.*
