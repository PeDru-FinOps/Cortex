#ia #finops #agent #model #cloudcomputing 
# Analista FinOps Sênior — Planejamento Orçamentário e Migração Multi-Cloud (v3)

## Sobre a posição

Buscamos um(a) **Analista FinOps Sênior** para atuar como referência técnica e financeira em programas de migração cloud de alta complexidade — seja **cross-cloud** (AWS ↔ Azure ↔ GCP ↔ OCI) ou **Datacenter On-Premises → Cloud**. A pessoa será responsável por estruturar o planejamento orçamentário do programa, acompanhar o desembolso financeiro ao longo do cronograma de waves de migração, e garantir que cada BC (Business Case) de migração se sustente do ponto de vista de TCO (Total Cost of Ownership), unit economics e eficiência operacional pós-migração.

Esta não é uma vaga de analista de billing. Procuramos alguém que já tenha sentado na mesa com CFO, CTO e liderança de infraestrutura durante um programa de migração, defendendo forecast, explicando variance e ajustando a estratégia de commitments — SP (Savings Plans), RI (Reserved Instances), CUD (Committed Use Discounts) — ao ritmo real de decommissioning do legado.

## Responsabilidades principais

- Construir, manter e defender o **modelo financeiro do programa de migração**, incluindo CAPEX (Capital Expenditure) residual do datacenter, OPEX (Operational Expenditure) projetado em cloud, custos paralelos durante o período de dual-run, e ponto de equilíbrio de decommissioning.
- Estabelecer e acompanhar o **orçamento mensal/trimestral** por wave, aplicação, business unit e cost center, garantindo visibilidade contínua de *budget vs. actual vs. forecast*.
- Produzir **variance narratives** (análises de desvio) para liderança executiva, conectando causas técnicas — mudança de escopo, atraso de wave, re-architecting, spike de egress — a impacto financeiro mensurável, incluindo reavaliação contínua de ROI (Return on Investment) do programa.
- Desenhar a **estratégia de commitments** sincronizada com o cronograma de migração, cobrindo:
  - AWS: SP, RI, e negociação de PPA (Private Pricing Addendum/Agreement), sucessor do antigo EDP (Enterprise Discount Program).
  - Azure: Reservations, Savings Plans for Compute, Azure Hybrid Benefit e acompanhamento de MACC (Microsoft Azure Consumption Commitment), geralmente vinculado a EA (Enterprise Agreement) ou MCA (Microsoft Customer Agreement).
  - GCP: CUD (resource-based e spend-based) e aproveitamento de SUD (Sustained Use Discounts).
  - OCI: Annual Universal Credits e Pay-As-You-Go, incluindo gestão de Oracle Support Rewards quando aplicável.
- Evitar over-commitment precoce e under-commitment em steady state, mitigando CLR (Commitment Lock-in Risk) e shortfall penalties em qualquer um dos contratos acima.
- Implementar e evoluir **políticas de tagging, chargeback e showback** multi-cloud, garantindo rastreabilidade financeira desde o primeiro workload migrado.
- Operar plataformas de **FinOps multi-cloud** para consolidação de custos, anomaly detection, forecasting e rightsizing entre provedores.
- Atuar como **ponte entre TI, Finanças, PMO e áreas de negócio**, traduzindo decisões arquiteturais em impacto de P&L (Profit and Loss) e vice-versa.
- Apoiar **negociações com provedores de cloud** com base em dados de projeção do programa de migração, incluindo incentivos de migração como AWS MAP (Migration Acceleration Program), Azure Migrate and Modernize e Google Rapid Migration Program (RaMP).
- Definir e acompanhar KPIs (Key Performance Indicators) de FinOps: forecast accuracy, ESR (Effective Savings Rate), CLR, unit cost por workload, cost per transaction.

## Gestão de licenças e modelos comerciais de software

Parte central desta posição é o acompanhamento e a **recomendação financeira de estratégias de licenciamento** de sistemas operacionais, bancos de dados e componentes de aplicação (Windows Server, SQL Server, RHEL, Oracle Database, WebLogic, middleware de integração, soluções de backup, etc.), considerando:

- **Avaliação de renovação vs. compra nova vs. substituição** de licenças em cenários de migração, comparando impacto em TCO e ROI sob horizontes de 3 e 5 anos.
- Análise comparativa entre **BYOL (Bring Your Own License)**, aquisição via cloud marketplace (AWS Marketplace, Azure Marketplace, Google Cloud Marketplace, OCI Marketplace) e compra direta com fabricante ou distribuidor autorizado.
- Domínio dos diferentes **modelos de licenciamento**:
  - Term License (licença por tempo determinado, tipicamente 1 a 5 anos).
  - Licenças perpétuas com contratos de suporte/manutenção recorrentes.
  - ULA (Unlimited License Agreement), como o modelo praticado pela Oracle, incluindo avaliação estratégica do momento de certificação e saída do ULA.
  - Modelos de subscription e SaaS (Software as a Service) com métricas de consumo (por usuário, por core, por processamento, por throughput).
- Consideração de **benefícios de portabilidade e vantagens híbridas**, como Azure Hybrid Benefit, AWS License Included vs. BYOL e políticas de licenciamento Oracle em ambientes cloud autorizados.
- Integração do planejamento de licenças ao **ciclo orçamentário**, antecipando marcos contratuais (true-up, true-down, renovações) e impacto no fluxo de caixa.
- Colaboração com ITAM (IT Asset Management), jurídico e procurement na estruturação de business cases de renovação, consolidação ou substituição de fornecedores.

## Requisitos obrigatórios

- **5+ anos de experiência em FinOps, Cloud Cost Management ou Controladoria de TI**, com atuação sênior em ambientes de grande porte.
- **Experiência comprovada em planejamento orçamentário** de programas plurianuais de TI, incluindo elaboração de BC, modelagem financeira, forecasting e análise de variance.
- **Experiência prática em acompanhamento financeiro de cronograma de migrações cloud**, seja cross-cloud ou Datacenter-to-Cloud, com domínio de conceitos como dual-run cost, decommissioning plan, hidden costs de migração (egress, re-platform, re-architect) e TCO comparativo.
- **Domínio técnico e financeiro de AWS** — pricing models, billing, Cost Explorer, CUR (Cost and Usage Report) e CUR 2.0, SP, RI, organizations/linked accounts, PPA/EDP.
- **Experiência obrigatória com pelo menos uma plataforma de FinOps multi-cloud**. Consideramos como referências de mercado:
  - **Cloud8** — plataforma brasileira de FinOps multi-cloud e multi-SaaS, com cobertura AWS, Azure, GCP, OCI e Huawei.
  - **Cloudability (Apptio)** — plataforma americana de referência histórica em cloud financial management.
  - **Flexera One** — plataforma americana com forte atuação em ITAM combinado com FinOps híbrido.
  - Também consideramos experiência em CloudHealth (VMware Aria Cost), Finout, ProsperOps, nOps, Vantage ou equivalentes.
- **Conhecimento de modelos de licenciamento de software** em cenários de migração cloud, incluindo BYOL, marketplace, compra direta, term licenses, licenças perpétuas e ULA.
- Capacidade analítica avançada com **SQL (Structured Query Language) e ferramentas de BI (Business Intelligence)** como Power BI, Tableau, QuickSight, Looker ou similar.
- **Comunicação executiva** — capacidade de apresentar trade-offs financeiros para audiências técnicas e não técnicas, do engenheiro ao CFO.

## Requisitos desejáveis

- Experiência prática em **GCP, Azure e/ou OCI**, idealmente em ambientes onde mais de um provedor opera simultaneamente.
- **Certificações FinOps Foundation**: FOCP (FinOps Certified Practitioner), FCP (FinOps Certified Professional), FinOps Certified Engineer ou FOCUS Analyst.
- Certificações de cloud: AWS Certified Cloud Practitioner / Solutions Architect, Azure Fundamentals / Administrator, Google Cloud Digital Leader / Cloud Architect, OCI Foundations.
- Experiência com **IaC (Infrastructure as Code)** — Terraform, CloudFormation, Bicep — o suficiente para ler, interpretar e correlacionar decisões arquiteturais com impacto de custo.
- Vivência em **programas de migração com frameworks estruturados** — AWS MAP, Azure Migrate and Modernize, Google RaMP (Rapid Migration Program), Oracle SCM (Support Rewards / Cloud Lift) — incluindo o componente financeiro de incentivos de migração.
- Conhecimento do **FinOps Framework** oficial (Princípios, Personas, Phases: Inform / Optimize / Operate, Capabilities e Domains).
- Experiência com **FOCUS (FinOps Open Cost and Usage Specification)** para normalização de dados de faturamento entre provedores.
- Experiência prévia em **FP&A (Financial Planning & Analysis)** ou controladoria corporativa é um diferencial relevante.
- Inglês intermediário a avançado — leitura técnica obrigatória; conversação é diferencial para interação com vendors e comunidade FinOps internacional.
- Formação em Ciências Contábeis, Administração, Economia, Engenharia, Sistemas de Informação, Ciência da Computação ou áreas correlatas. Pós-graduação ou MBA em Finanças, Gestão de TI ou Governança de TI é diferencial.

## O que você vai entregar nos primeiros 12 meses

- Um **modelo de forecast mensal** do programa de migração, com acurácia superior a 90% no horizonte de 90 dias.
- Rituais de **FinOps mensais** com stakeholders técnicos e financeiros, com variance narrative executiva.
- **Política de commitments** dimensionada e revisada trimestralmente, com ESR documentado e CLR sob controle.
- **Plano de licenciamento integrado** ao roadmap de migração, com recomendações formais de BYOL, marketplace ou compra direta por workload.
- **Taxonomia de tags e chargeback** operando em produção, cobrindo todos os workloads migrados.
- **Dashboard consolidado multi-cloud** em operação, fonte única de verdade para custos de cloud da companhia.

## Perfil comportamental

Buscamos uma pessoa que pense como FP&A mas entenda infraestrutura como engenheiro; que trate o custo de cloud como um produto a ser gerenciado continuamente, e não como uma fatura a ser reagida. Autonomia, rigor analítico, capacidade de influenciar sem autoridade formal e tolerância à ambiguidade típica de programas de migração são essenciais.

---

**Observação para recrutadores**: esta descrição foi construída a partir de referências públicas de vagas de FinOps do mercado brasileiro e internacional (FinOps Foundation Job Board, Indeed, Glassdoor, Visa, Autodesk, Ânima, Alelo, CSG, entre outras), do framework oficial da FinOps Foundation, e de documentação pública de programas de commitment dos hyperscalers (AWS PPA, Microsoft MACC, GCP CUD, OCI Annual Universal Credits).

---

## Versão curta para post no LinkedIn

🚀 **Vaga: Analista FinOps Sênior — Cloud8**

Estamos contratando um(a) FinOps Sênior para atuar em programas de migração cloud de alta complexidade — cross-cloud (AWS ↔ Azure ↔ GCP ↔ OCI) e Datacenter → Cloud.

**O que você vai fazer:**
▸ Estruturar planejamento orçamentário plurianual de programas de migração
▸ Acompanhar o desembolso financeiro ao longo do cronograma de waves
▸ Construir e defender business cases de migração (TCO, ROI, unit economics)
▸ Desenhar estratégia de commitments: AWS SP/RI/PPA, Azure MACC, GCP CUD, OCI Annual Universal Credits
▸ Recomendar estratégias de licenciamento (BYOL, marketplace, compra direta) para Windows Server, SQL Server, Oracle Database e afins
▸ Atuar com CFO, CTO, PMO e áreas de negócio traduzindo arquitetura em P&L

**Requisitos:**
✅ 5+ anos em FinOps, Cloud Cost Management ou Controladoria de TI
✅ Experiência comprovada em planejamento orçamentário e acompanhamento financeiro de migrações cloud
✅ AWS obrigatório (Cost Explorer, CUR, SP, RI, PPA/EDP)
✅ Experiência com plataforma de FinOps multi-cloud — Cloud8, Cloudability, Flexera One ou equivalente
✅ Conhecimento de modelos de licenciamento (BYOL, term license, perpétua, ULA)
✅ SQL + BI (Power BI, Tableau, QuickSight ou Looker)

**Diferenciais:** GCP/Azure/OCI, certificações FOCP/FCP, inglês avançado, experiência com AWS MAP / Azure Migrate / GCP RaMP.

Interessados(as), comentem ou me chamem no inbox. 💬
Indicações são muito bem-vindas!

---

## Versão curta para WhatsApp / LinkedIn Inbox

Oi! Tudo bem?

Estamos com uma vaga de **Analista FinOps Sênior** na Cloud8 e achei que poderia te interessar (ou alguém da sua rede).

Resumo rápido:
• Atuação em programas de migração cloud — cross-cloud e Datacenter → Cloud
• Planejamento orçamentário plurianual, business cases, TCO/ROI, estratégia de commitments (AWS PPA, Azure MACC, GCP CUD, OCI Annual Universal Credits)
• Também cobre recomendação de licenciamento (BYOL, marketplace, compra direta, ULA etc.)
• Requer 5+ anos de experiência, AWS obrigatório, experiência com plataforma de FinOps multi-cloud (Cloud8, Cloudability, Flexera One ou equivalente)
• Interlocução com CFO, CTO e PMO faz parte do escopo

Descrição completa no post do LinkedIn: [COLAR_LINK_DO_POST_AQUI]

Se fizer sentido pra você ou quiser indicar alguém, me avisa que te passo os próximos passos. 🙏
