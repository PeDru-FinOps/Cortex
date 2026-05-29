#finops #gcp #cloudcomputing 

## Como o GKE Cost Allocation funciona

O recurso “GKE Cost Allocation” adiciona labels Kubernetes nas linhas do billing exportado. Isso permite [[Gerenciar recursos de GKE usando tags]]

Após habilitar no cluster:

- o billing export no BigQuery recebe labels extras;
- surgem campos como:
    - `k8s-workload-name`
    - labels customizadas do Kubernetes;
- torna-se possível agrupar custo por:
    - deployment;
    - namespace;
    - squad;
    - projeto;
    - ambiente.

Exemplo citado:

```
SELECT  sku.description AS sku,  label.value AS workload_name,  SUM(cost) AS costFROM  [YOUR-DETAILED-BILLING-EXPORT],  UNNEST(labels) labelWHERE  label.key = 'k8s-workload-name'GROUP BY  sku,  label.valueORDER BY  cost DESC
```

A ideia é usar:

- Billing Export → BigQuery
- SQL → dashboards
- Looker / Sheets / BI tools

para criar visibilidade granular de custos.

---

# Pontos técnicos importantes

## 1. Billing baseado em resource requests

O ponto mais crítico do artigo:

> GKE Cost Allocation usa _resource requests_, não uso real.

Ou seja:

- o custo é distribuído com base no:
    - `requests.cpu`
    - `requests.memory`

e não no consumo efetivo.

Exemplo:

- Pod pede 4 vCPU;
- usa 0.5 vCPU;
- billing considera 4 vCPU reservadas.

Isso cria distorções relevantes.

---

## 2. Overprovisioning gera custo inflado

Se os times definem requests exagerados:

```
resources:  requests:    cpu: "4"
```

o modelo de custo atribui mais custo ao workload, mesmo sem utilização real.

Consequências:

- chargeback incorreto;
- squads parecem mais caras do que realmente são;
- dificuldade de identificar desperdício real.

---

## 3. Labels viram dimensão de FinOps

O artigo enfatiza que labels Kubernetes são fundamentais para governança financeira.

Exemplo:

```
labels:  team: payments  environment: prod  initiative: fraud-detection
```

Isso permite:

- custo por squad;
- custo por produto;
- custo por feature;
- accountability financeira.

É uma visão fortemente alinhada a:

- FinOps operacional;
- ownership distribuído;
- engenharia responsável por custo.

---

# Limitações apontadas

## Pods sem workload

Pods criados diretamente (sem Deployment/StatefulSet/Job) podem ficar:

- sem attribution;
- parcialmente invisíveis no billing.

---

## Custos não atribuídos

Alguns custos ficam fora do modelo:

- system pods;
- overhead do cluster;
- networking;
- storage compartilhado;
- custos de control plane;
- DaemonSets;
- idle capacity.

Isso faz com que:

- soma dos workloads ≠ custo total do cluster.

---

## Limite de labels

O artigo cita uma limitação importante:

- workloads com mais de 50 labels Kubernetes
- podem perder export de labels para billing.

---

# Arquitetura FinOps recomendada implicitamente

O artigo praticamente sugere esta arquitetura:

```
GKE  ↓Billing Export  ↓BigQuery  ↓Transformações SQL  ↓Dashboards / Alertas  ↓Chargeback / Showback
```

Com enriquecimento via:

- labels Kubernetes;
- taxonomia organizacional;
- ownership por time.
## Referência

https://followrabbit.ai/blog/gke-cost-allocation-master-kubernetes-spending