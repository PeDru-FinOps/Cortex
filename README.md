# Cortex

Repositorio local de notas Markdown correlacionadas por pastas e hashtags.

## Funcionalidades

- Login com usuario e senha definidos no `.env`
- Diretorio de pastas, subpastas e arquivos `.md`
- Criacao, leitura e alteracao de notas Markdown
- Pre-visualizacao em HTML
- Grafo gerado a partir de diretorios e hashtags

## Como rodar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

Depois acesse `http://127.0.0.1:5000`.

Edite o arquivo `.env` antes de usar em um ambiente real.
