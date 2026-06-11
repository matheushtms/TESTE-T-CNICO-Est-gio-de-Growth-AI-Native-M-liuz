# Relatório de Teste A/B de Cashback – Méliuz
**Parceiro Analisado:** Parceiro B  
**Período do Experimento:** 2011-05-01 a 2011-06-30 (61 dias)  
**Data da Análise:** 2026-06-11 15:15:23  

---

## 1. Resumo Executivo
Foi analisado o teste A/B para o parceiro **Parceiro B** com o objetivo de determinar qual variante de cashback oferece o melhor equilíbrio entre volume de vendas (GMV), rentabilidade e retorno sobre investimento (ROI).

> [!IMPORTANT]
> **RECOMENDAÇÃO FINAL: Manter o Controle (Grupo 1) em 100%**  
> *Justificativa:* Nenhuma das variantes de tratamento superou o grupo de controle em lucro líquido total ou apresentou ROI sustentável. Portanto, a recomendação mais segura e rentável é manter o grupo de controle.

## 2. Resultados Consolidados
A tabela abaixo apresenta os resultados agregados de cada variante durante todo o período do experimento:

| Variante | Compradores | GMV Total | Comissão | Cashback | Lucro Líquido | ROI | Cashback/Comissão (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Grupo 1** | 7.990 | R$ 4.093.818,00 | R$ 450.321,00 | R$ 163.751,00 | **R$ 286.570,00** | **175.0%** | 36.4% |
| **Grupo 2** | 5.452 | R$ 2.863.019,00 | R$ 314.935,00 | R$ 171.778,00 | **R$ 143.157,00** | **83.3%** | 54.5% |
| **Grupo 3** | 5.029 | R$ 2.629.963,00 | R$ 289.290,00 | R$ 236.697,00 | **R$ 52.593,00** | **22.2%** | 81.8% |

## 3. Eficiência e Unit Economics
Métricas médias por comprador único para entender o comportamento de consumo e a eficiência do incentivo:

| Variante | GMV por Comprador (Ticket Médio) | Comissão por Comprador | Cashback por Comprador | Lucro por Comprador |
| :--- | :--- | :--- | :--- | :--- |
| **Grupo 1** | R$ 512,37 | R$ 56,36 | R$ 20,49 | **R$ 35,87** |
| **Grupo 2** | R$ 525,13 | R$ 57,77 | R$ 31,51 | **R$ 26,26** |
| **Grupo 3** | R$ 522,96 | R$ 57,52 | R$ 47,07 | **R$ 10,46** |

## 4. Análise de Significância Estatística
Para certificar de que os resultados observados não são fruto de oscilações casuais (ruído), realizamos testes de hipóteses estatísticas comparando a distribuição diária das variantes de tratamento contra o grupo de controle.

**Grupo de Controle (Linha de Base):** `Grupo 1`

### Comparação: `Grupo 2` vs `Grupo 1`
Abaixo estão os resultados do teste T de Welch (comparação de médias diárias) e do teste não-paramétrico de Mann-Whitney U:

| Métrica Testada | Dif. Média | % Var. | p-value (Welch T-Test) | p-value (Mann-Whitney) | Significativo (95%?) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lucro Diário** | R$ -2.351,03 | -50.0% | 0.0000 | 0.0000 | ✅ Sim (p < 0.05) |
| **ROI Diário** | -91.7 p.p. | -52.4% | 0.0000 | 0.0000 | ✅ Sim (p < 0.05) |
| **GMV por Comprador Diário** | +R$ 14,97 | +2.9% | 0.1643 | 0.1732 | ❌ Não (p >= 0.05) |

> [!WARNING]
> **Insight:** O grupo `Grupo 2` causou uma redução estatisticamente significativa no lucro diário. A estratégia é prejudicial ao negócio.

### Comparação: `Grupo 3` vs `Grupo 1`
Abaixo estão os resultados do teste T de Welch (comparação de médias diárias) e do teste não-paramétrico de Mann-Whitney U:

| Métrica Testada | Dif. Média | % Var. | p-value (Welch T-Test) | p-value (Mann-Whitney) | Significativo (95%?) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lucro Diário** | R$ -3.835,69 | -81.6% | 0.0000 | 0.0000 | ✅ Sim (p < 0.05) |
| **ROI Diário** | -152.8 p.p. | -87.3% | 0.0000 | 0.0000 | ✅ Sim (p < 0.05) |
| **GMV por Comprador Diário** | +R$ 13,24 | +2.6% | 0.2319 | 0.2800 | ❌ Não (p >= 0.05) |

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