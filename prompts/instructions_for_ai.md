# Instruções para Assistentes de IA (AI-Native Growth Agent)

Este projeto foi construído para ser "AI-Native". Se você está operando como um assistente de IA (Claude Code, Cursor, Gemini, GPT personalizado, etc.) auxiliando um analista de growth do Méliuz, siga as instruções abaixo para realizar análises consistentes e interagir com esta base de código.

---

## 1. O que você (a IA) deve fazer

Quando o usuário solicitar para analisar um novo teste A/B ou indicar um arquivo de dados:
1. **Execute a CLI da aplicação** para gerar os cálculos e o relatório executivo em Markdown.
2. **Leia o relatório executivo gerado** na pasta `reports/` (ex: `reports/relatorio_parceiro_a.md`).
3. **Resuma os resultados e a recomendação final** para o usuário em linguagem natural e tom de negócios de Growth.
4. **Responda à pergunta central:** *"Dado esse teste A/B, qual variante de cashback devemos escalar para 100% do tráfego?"*
5. **Se solicitado, registre o teste** na planilha local/Google Sheets acionando o respectivo parâmetro da CLI ou através do painel visual.

---

## 2. Comandos que você pode rodar no terminal

Para rodar a análise de forma direta:
```bash
python main.py --file data/parceiro_a.csv
```

Você também pode especificar parâmetros adicionais:
- `--name "Nome do Teste"`: Nome legível para o histórico.
- `--desc "Sua descrição"`: Contexto curto sobre a hipótese do teste.

*Exemplo completo:*
```bash
python main.py --file data/parceiro_b.csv --name "Méliuz - Parceiro B - Jan 2026" --desc "Testando cashback de 3.0% e 6.5% vs controle de 1.5%"
```

---

## 3. Guia de Interpretação das Métricas (Para a IA)

Você deve basear sua análise nas métricas financeiras e estatísticas calculadas pelo sistema:
- **Lucro Líquido (Comissão - Cashback):** É a métrica mais importante para o negócio do Méliuz. Aumentar o GMV a custo de queimar margem (lucro menor que o controle) **não** é recomendável.
- **ROI (Lucro / Cashback):** Avalia a eficiência do capital. Cashback maior pode trazer mais compradores, mas se o ROI desabar drasticamente, o canal torna-se ineficiente.
- **p-value (Significância Estatística):**
  - **p-value < 0.05:** Diferença sólida e comprovada estatisticamente (95% de confiança). Altamente recomendável escalar.
  - **p-value entre 0.05 e 0.10:** Relevância marginal. Recomenda-se escalar com monitoramento rigoroso.
  - **p-value > 0.10:** Diferença provavelmente fruto de ruído diário. Recomenda-se **manter o controle** ou rodar o teste por mais tempo.

---

## 4. Estrutura de Resposta Recomendada ao Usuário

Ao terminar a execução, estruture sua resposta ao usuário da seguinte forma:

```markdown
### 🎯 Decisão sobre o Teste: [Escalar Grupo X para 100% / Manter Controle]

**Resumo da Decisão:**
[Insira 2-3 frases resumindo os motivos e a relevância estatística do lucro do grupo vencedor.]

#### 📊 Principais Métricas Comparativas
- **Controle ([Nome do Controle])**: Lucro de R$ [X], ROI de [X]% e [X] compradores.
- **Tratamento ([Nome da Variante])**: Lucro de R$ [Y] ([+X]% vs controle), ROI de [Y]% e [Y] compradores.

#### 🔬 Análise de Significância
- O teste T de Welch indicou um p-value de **[P-VALUE]** para o Lucro Diário. [Explicar se é estatisticamente significativo].

#### ⚠️ Riscos e Próximos Passos
- [Mapear riscos de saturação de cashback ou unit economics negativos].
- [Indicar a ação de escalabilidade ou descarte do teste].
```
