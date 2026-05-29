#cloud8 #governance #security #data_governance 

A plataforma da Cloud8 possui a funcionalidade de auditar logs de atividades que alterem o estado de um recurso e estejam diretamente relacionados à execução de alguma funcionalidade da plataforma Cloud8.

A funcionalidade de _Auditing Logs_ da Cloud8 oferece aos administradores uma visão abrangente e estruturada das ações realizadas **tanto na plataforma quanto nos provedores de nuvem integrados**. Com a possibilidade de filtrar, analisar e exportar eventos relevantes, a ferramenta contribui para maior transparência operacional, reforça práticas de segurança e facilita o atendimento a requisitos de compliance. Dessa forma, os gestores conseguem monitorar impactos, identificar incidentes e manter o controle sobre todas as alterações que afetam os recursos gerenciados pela Cloud8.

**Atualmente há 3 tipos de atividade de log que são registradas:**

1. Painel do Cliente: todas as ações executadas no console da Cloud8, com exceção das ações de leitura.
2. Agendamentos do Cliente: todas as automações e agendamentos executadas no console da Cloud8.
3. Logs Externos: inclui ações executadas diretamente no cloud provider que tenham impacto sobre recursos ou serviços monitorados e gerenciados pela Cloud8.

Ainda que não seja o foco da ferramenta, a funcionalidade atende aos requisitos mínimos de compliance em segurança, permitindo que administradores monitorem o uso da plataforma e seu impacto nos recursos gerenciados através da mesma.

## Filtrando informações nos Logs de Auditoria

Através da funcionalidade Auditing Logs é possível visualizar todos os logs dentro de uma determinada janela temporal que pode ser configurada na coluna “Date”.

![Auditoria de Logs na Plataforma Cloud8](https://www.cloud8.com.br/wp-content/uploads/2021/06/cloud8-auditing-1.webp "Auditoria de Logs na Plataforma Cloud8")

Além do período, também é possível filtrar os seguintes campos clicando na seta no canto direito da coluna a ser filtrada:

- Level: grau de severidade do alerta.
- Provider: provider no qual o fato gerador do log ocorreu.
- User: usuário responsável pela ação que gerou o log.
- Category: categoria de serviço ao qual a ação pertence.
- Event: ocorrência que gerou o log.
- ID: identificador do recurso.
- Source: tipo de atividade de log.
- Message: resumo da ação registrada.
- IP: IP vinculado à ação, quando existir.
- Region: região do recurso.
- Availability Zona: zona de disponibilidade do recurso.

## Exportação de Logs de Auditoria

Ao realizar a filtragem dos logs que se deseja auditar, é possível exportar um relatório clicando em “Download data em CSV format, no canto superior direito da página.

![Auditoria de Logs na Plataforma Cloud8](https://www.cloud8.com.br/wp-content/uploads/2021/06/cloud8-auditing-2.webp "Auditoria de Logs na Plataforma Cloud8")

O relatório será gerado no formato CSV contendo exatamente os dados filtrados.