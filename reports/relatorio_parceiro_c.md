# Relatório de Teste A/B de Cashback – Méliuz
**Parceiro Analisado:** Parceiro C  
**Período do Experimento:** 2011-07-01 a 2011-08-14 (45 dias)  
**Data da Análise:** 2026-06-11 15:15:47  

---

## 1. Resumo Executivo
Foi analisado o teste A/B para o parceiro **Parceiro C** com o objetivo de determinar qual variante de cashback oferece o melhor equilíbrio entre volume de vendas (GMV), rentabilidade e retorno sobre investimento (ROI).

> [!IMPORTANT]
> **RECOMENDAÇÃO FINAL: Manter o Controle (Grupo 1) em 100%**  
> *Justificativa:* Nenhuma das variantes de tratamento superou o grupo de controle em lucro líquido total ou apresentou ROI sustentável. Portanto, a recomendação mais segura e rentável é manter o grupo de controle.

## 2. Resultados Consolidados
A tabela abaixo apresenta os resultados agregados de cada variante durante todo o período do experimento:

| Variante | Compradores | GMV Total | Comissão | Cashback | Lucro Líquido | ROI | Cashback/Comissão (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Grupo 1** | 4.549 | R$ 1.738.460,00 | R$ 121.693,00 | R$ 86.924,00 | **R$ 34.769,00** | **40.0%** | 71.4% |
| **Grupo 2** | 4.522 | R$ 1.685.235,00 | R$ 117.967,00 | R$ 117.967,00 | **R$ 0,00** | **0.0%** | 100.0% |

## 3. Eficiência e Unit Economics
Métricas médias por comprador único para entender o comportamento de consumo e a eficiência do incentivo:

| Variante | GMV por Comprador (Ticket Médio) | Comissão por Comprador | Cashback por Comprador | Lucro por Comprador |
| :--- | :--- | :--- | :--- | :--- |
| **Grupo 1** | R$ 382,16 | R$ 26,75 | R$ 19,11 | **R$ 7,64** |
| **Grupo 2** | R$ 372,67 | R$ 26,09 | R$ 26,09 | **R$ 0,00** |

## 4. Análise de Significância Estatística
Para certificar de que os resultados observados não são fruto de oscilações casuais (ruído), realizamos testes de hipóteses estatísticas comparando a distribuição diária das variantes de tratamento contra o grupo de controle.

**Grupo de Controle (Linha de Base):** `Grupo 1`

### Comparação: `Grupo 2` vs `Grupo 1`
Abaixo estão os resultados do teste T de Welch (comparação de médias diárias) e do teste não-paramétrico de Mann-Whitney U:

| Métrica Testada | Dif. Média | % Var. | p-value (Welch T-Test) | p-value (Mann-Whitney) | Significativo (95%?) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lucro Diário** | R$ -772,64 | -100.0% | 0.0000 | 0.0000 | ✅ Sim (p < 0.05) |
| **ROI Diário** | -40.0 p.p. | -100.0% | 0.0000 | 0.0000 | ✅ Sim (p < 0.05) |
| **GMV por Comprador Diário** | R$ -10,18 | -2.7% | 0.2663 | 0.2831 | ❌ Não (p >= 0.05) |

> [!WARNING]
> **Insight:** O grupo `Grupo 2` causou uma redução estatisticamente significativa no lucro diário. A estratégia é prejudicial ao negócio.

## 5. Insights de Negócio e Análise de Risco
- **Inviabilidade Econômica de `Grupo 2`**: Apesar de um possível aumento de compradores ou GMV, a variante reduziu a rentabilidade geral da operação devido ao peso do cashback (custo superou o retorno da comissão).

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