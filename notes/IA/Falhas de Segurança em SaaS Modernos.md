#ia #security 

A maioria das invasões em aplicações web não acontece por vulnerabilidades “sofisticadas”.  
Elas acontecem porque fundamentos básicos de segurança foram ignorados durante o desenvolvimento.

Este artigo reúne 31 erros extremamente comuns em APIs, aplicações SaaS e produtos modernos — especialmente em stacks com React, Next.js, Node.js, Python, Supabase, Firebase, OpenAI APIs e arquiteturas cloud.

---

# Autenticação e Autorização

## a) No authentication on private routes

Rotas privadas sem autenticação permitem acesso direto a recursos internos.

Exemplo:

```
GET /api/admin/users
```

Sem validação de sessão, qualquer usuário consegue acessar dados sensíveis.

### Correção

- Middleware obrigatório de autenticação
- Bloqueio server-side
- Nunca confiar apenas no frontend

---

## b) Admin routes protected only in frontend

Ocultar telas administrativas no React não protege nada.

Se a API aceita:

```
POST /api/admin/delete-user
```

qualquer pessoa pode chamar essa rota manualmente via Postman ou curl.

### Correção

- Validar permissões no backend
- Implementar RBAC
- Checar roles no servidor

---

## c) Missing server-side authorisation checks

Mesmo autenticado, o usuário não deveria acessar recursos de outros usuários.

Exemplo inseguro:

```
GET /api/invoices/123
```

Sem verificar ownership, basta trocar IDs.

### Correção

- Validar tenant/user ownership
- Aplicar checks em TODAS as rotas

---

# JWT e Sessão

## d) JWT stored in localStorage

`localStorage` é vulnerável a XSS.

Se houver qualquer script malicioso:

```
localStorage.getItem("token")
```

o atacante rouba sessões.

### Correção

- Preferir cookies HttpOnly
- SameSite + Secure
- Reduzir superfície XSS

---

## e) JWT secret copied from a tutorial

Segredos previsíveis quebram toda a autenticação.

Exemplo comum:

```
JWT_SECRET=secret123
```

ou:

```
JWT_SECRET=myappsecret
```

### Correção

Gerar secrets criptograficamente fortes:

```
openssl rand -base64 64
```

---

## f) Tokens with no expiry

Tokens eternos significam sessões eternamente válidas.

Se vazarem, o acesso permanece indefinidamente.

### Correção

- Expiração curta
- Refresh tokens rotativos
- Revogação de sessão

---

## g) Logout that only clears browser state

Apagar o token do frontend não invalida sessões roubadas.

### Correção

- Revogar refresh tokens
- Invalidar sessões server-side
- Blacklist de tokens quando necessário

---

# Rate Limiting e Abuse Protection

## h) No rate limiting on login/signup

Sem limitação:

- brute force
- credential stuffing
- criação massiva de contas

### Correção

- Rate limiting por IP
- CAPTCHA adaptativo
- Proteção contra automação

---

## i) No throttling on expensive APIs

Endpoints caros podem derrubar sua infraestrutura.

Exemplo:

- geração IA
- exportações
- queries analíticas
- embeddings

### Correção

- Limites por usuário
- Queue
- Cotas de consumo

---

## j) No abuse limits on AI/API usage

Sem limites, usuários podem consumir milhares de dólares em APIs.

Muito comum com OpenAI APIs.

### Correção

- Billing quotas
- Daily/monthly caps
- Alertas de consumo

---

# Gestão de Segredos

## k) API keys exposed in frontend code

Tudo enviado ao browser é público.

Mesmo minificado.

### Correção

- Nunca colocar secrets no frontend
- Proxy server-side
- Variáveis privadas apenas no backend

---

## l) API keys committed to GitHub

Bots escaneiam GitHub constantemente.

Uma chave publicada pode ser explorada em minutos.

### Correção

- `.gitignore`
- Secret scanning
- Rotação imediata

---

## m) Secrets shared in prompts or screenshots

Capturas de tela frequentemente vazam:

- tokens
- URLs internas
- credenciais
- variáveis de ambiente

### Correção

- Sanitizar screenshots
- Nunca compartilhar `.env`
- Redigir dados sensíveis

---

# Banco de Dados

## n) Database exposed to the public internet

Banco aberto diretamente para internet pública é um desastre esperando acontecer.

### Correção

- Private networking
- VPN/Bastion
- Security groups restritivos

---

## o) Weak database password

Senhas fracas continuam extremamente comuns.

### Correção

- Password managers
- Secrets manager
- Rotação periódica

---

## p) App using root DB credentials

Comprometer a aplicação significa comprometer o banco inteiro.

### Correção

Criar usuários específicos:

- leitura
- escrita
- migração
- analytics

Princípio do menor privilégio.

---

## q) Missing row-level security policies

Muito comum em Supabase/Postgres.

Sem RLS:

```
SELECT * FROM users;
```

retorna tudo para qualquer usuário autenticado.

### Correção

Aplicar políticas explícitas:

```
CREATE POLICY ...
```

---

## r) Users can change IDs and access other data

O clássico IDOR (Insecure Direct Object Reference).

Exemplo:

```
/api/orders/1001
```

troca para:

```
/api/orders/1002
```

e acessa pedido de outro usuário.

### Correção

- Validar ownership
- Nunca confiar no ID enviado pelo cliente

---

# Validação e Input Handling

## s) Inputs passed directly into SQL queries

SQL Injection ainda existe em 2026.

Código inseguro:

```
query = f"SELECT * FROM users WHERE email = '{email}'"
```

### Correção

- Prepared statements
- ORM seguro
- Query parametrizada

---

## t) No validation on request body fields

Usuários podem enviar:

- campos inesperados
- payloads gigantes
- tipos inválidos
- objetos maliciosos

### Correção

Validar schemas:

- Zod
- Pydantic
- Joi
- Yup

---

## u) File uploads without type and size checks

Uploads inseguros permitem:

- malware
- DoS
- execução remota
- storage abuse

### Correção

- Limite de tamanho
- MIME validation
- Antivirus scanning

---

# Storage e Buckets

## v) Public buckets storing private user files

Buckets públicos frequentemente vazam:

- documentos
- contratos
- fotos
- backups

### Correção

- Buckets privados
- Signed URLs
- Expiração curta

---

# Infraestrutura e Rede

## w) Wildcard CORS on authenticated APIs

Configuração insegura:

```
Access-Control-Allow-Origin: *
```

### Correção

Permitir apenas domínios específicos.

---

## x) No HTTPS enforcement

Sem HTTPS:

- session hijacking
- MITM
- vazamento de credenciais

### Correção

- Redirect HTTP → HTTPS
- HSTS
- TLS moderno

---

## y) No DDoS or bot protection at the edge

Bots conseguem:

- derrubar APIs
- consumir recursos
- gerar custos

### Correção

Usar:

- Cloudflare
- AWS Shield
- WAF
- bot mitigation

---

## z) Open admin panels and debug endpoints

Exemplos perigosos:

```
/admin/debug/phpinfo/swagger/graphql-playground
```

### Correção

- Remover em produção
- VPN/IP allowlist
- autenticação forte

---

# Observabilidade e Operação

## aa) Error messages leaking stack traces

Stack traces revelam:

- estrutura interna
- bibliotecas
- caminhos de arquivos
- queries

### Correção

Retornar erros genéricos ao cliente.

---

## ab) Dependencies never scanned after install

Dependências vulneráveis envelhecem rápido.

### Correção

Ferramentas:

- Dependabot
- Snyk
- Trivy
- npm audit

---

## ac) No logs for auth, deletes, and payments

Sem logs você não consegue:

- investigar incidentes
- detectar fraude
- auditar ações

### Correção

Logar:

- login
- logout
- exclusões
- pagamentos
- mudanças administrativas

---

## ad) No backup and restore test

Backup sem teste de restore não é backup.

### Correção

- Testes periódicos
- Restore automatizado
- Disaster recovery drills

---

## ae) No rollback plan when production breaks

Deploy sem rollback vira incidente.

### Correção

- Blue/green deploy
- Feature flags
- Versionamento
- Rollback automatizado

---

# Conclusão

A maioria desses problemas não exige hackers avançados.

Eles exploram:

- defaults inseguros
- validações ausentes
- excesso de confiança no frontend
- má gestão operacional

Segurança moderna é menos sobre “blindagem absoluta” e mais sobre:

- reduzir superfície de ataque
- limitar impacto
- detectar rapidamente
- recuperar rápido

Se um SaaS corrige consistentemente os pontos acima, ele já fica muito acima da média do mercado.