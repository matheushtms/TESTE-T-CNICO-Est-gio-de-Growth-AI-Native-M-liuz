# Relatório de Teste A/B de Cashback – Méliuz
**Parceiro Analisado:** Parceiro A  
**Período do Experimento:** 2011-01-01 a 2011-04-02 (92 dias)  
**Data da Análise:** 2026-06-11 19:35:46  

---

## 1. Resumo Executivo
Foi analisado o teste A/B para o parceiro **Parceiro A** com o objetivo de determinar qual variante de cashback oferece o melhor equilíbrio entre volume de vendas (GMV), rentabilidade e retorno sobre investimento (ROI).

> [!IMPORTANT]
> **RECOMENDAÇÃO FINAL: Manter o Controle (Grupo 1) em 100%**  
> *Justificativa:* Nenhuma das variantes de tratamento superou o grupo de controle em lucro líquido total ou apresentou ROI sustentável. Portanto, a recomendação mais segura e rentável é manter o grupo de controle.

## 2. Resultados Consolidados
A tabela abaixo apresenta os resultados agregados de cada variante durante todo o período do experimento:

| Variante | Compradores | GMV Total | Comissão | Cashback | Lucro Líquido | ROI | Cashback/Comissão (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Grupo 1** | 9.633 | R$ 5.605.173,00 | R$ 638.135,00 | R$ 233.424,00 | **R$ 404.711,00** | **173.4%** | 36.6% |
| **Grupo 2** | 10.814 | R$ 6.423.096,00 | R$ 728.178,00 | R$ 370.659,00 | **R$ 357.519,00** | **96.5%** | 50.9% |
| **Grupo 3** | 11.410 | R$ 6.785.856,00 | R$ 767.887,00 | R$ 503.600,00 | **R$ 264.287,00** | **52.5%** | 65.6% |

## 3. Eficiência e Unit Economics
Métricas médias por comprador único para entender o comportamento de consumo e a eficiência do incentivo:

| Variante | GMV por Comprador (Ticket Médio) | Comissão por Comprador | Cashback por Comprador | Lucro por Comprador |
| :--- | :--- | :--- | :--- | :--- |
| **Grupo 1** | R$ 581,87 | R$ 66,24 | R$ 24,23 | **R$ 42,01** |
| **Grupo 2** | R$ 593,96 | R$ 67,34 | R$ 34,28 | **R$ 33,06** |
| **Grupo 3** | R$ 594,73 | R$ 67,30 | R$ 44,14 | **R$ 23,16** |

## 4. Análise de Significância Estatística
Para certificar de que os resultados observados não são fruto de oscilações casuais (ruído), realizamos testes de hipóteses estatísticas comparando a distribuição diária das variantes de tratamento contra o grupo de controle.

**Grupo de Controle (Linha de Base):** `Grupo 1`

### Comparação: `Grupo 2` vs `Grupo 1`
Abaixo estão os resultados do teste T de Welch (comparação de médias diárias) e do teste não-paramétrico de Mann-Whitney U:

| Métrica Testada | Dif. Média | % Var. | p-value (Welch T-Test) | p-value (Mann-Whitney) | Significativo (95%?) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lucro Diário** | R$ -512,96 | -11.7% | 0.1315 | 0.1450 | ❌ Não (p >= 0.05) |
| **ROI Diário** | -97.5 p.p. | -48.9% | 0.0000 | 0.0000 | ✅ Sim (p < 0.05) |
| **GMV por Comprador Diário** | +R$ 8,73 | +1.5% | 0.5242 | 0.5657 | ❌ Não (p >= 0.05) |

> [!NOTE]
> **Insight:** As diferenças de lucro entre `Grupo 2` e `Grupo 1` não são estatisticamente significativas (p-value = 0.131). Isso sugere que o comportamento de compra e as margens são semelhantes às atuais e os ganhos nominais podem ser flutuações temporárias.

### Comparação: `Grupo 3` vs `Grupo 1`
Abaixo estão os resultados do teste T de Welch (comparação de médias diárias) e do teste não-paramétrico de Mann-Whitney U:

| Métrica Testada | Dif. Média | % Var. | p-value (Welch T-Test) | p-value (Mann-Whitney) | Significativo (95%?) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lucro Diário** | R$ -1.526,35 | -34.7% | 0.0000 | 0.0000 | ✅ Sim (p < 0.05) |
| **ROI Diário** | -121.9 p.p. | -61.1% | 0.0000 | 0.0000 | ✅ Sim (p < 0.05) |
| **GMV por Comprador Diário** | +R$ 7,70 | +1.3% | 0.5488 | 0.3090 | ❌ Não (p >= 0.05) |

> [!WARNING]
> **Insight:** O grupo `Grupo 3` causou uma redução estatisticamente significativa no lucro diário. A estratégia é prejudicial ao negócio.

## 5. Insights de Negócio e Análise de Risco
- **Inviabilidade Econômica de `Grupo 2`**: Apesar de um possível aumento de compradores ou GMV, a variante reduziu a rentabilidade geral da operação devido ao peso do cashback (custo superou o retorno da comissão).
- **Inviabilidade Econômica de `Grupo 3`**: Apesar de um possível aumento de compradores ou GMV, a variante reduziu a rentabilidade geral da operação devido ao peso do cashback (custo superou o retorno da comissão).

**Riscos Identificados:**
1. **Saturação de Cashback**: Aumentar as taxas de cashback atrai mais clientes no curto prazo, mas reduz o ROI caso as vendas adicionais não diluam o custo do benefício.
2. **Fidelidade da Variante**: Usuários atraídos puramente por cashback elevado tendem a apresentar menor LTV (lifetime value) recorrente quando os incentivos diminuem.

## 6. Conclusão
Com base na análise quantitativa e nos testes de significância estatística, a decisão tomada é:

### **`Manter o Controle (Grupo 1) em 100%`**

*Próximos passos:*
1. Encerrar o experimento sem escalar a variante de cashback avaliada.
2. Estruturar uma nova modelagem de taxas de cashback com limites de custo superiores para o próximo ciclo de testes.
3. Avaliar se o parceiro pode oferecer uma comissão maior para viabilizar taxas de cashback mais agressivas.