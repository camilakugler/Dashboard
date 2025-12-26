# Dashboard

Painel interativo em Streamlit para explorar anúncios de veículos usados.

## Rápido: rodar localmente 🔧

1. Criar e ativar o ambiente virtual (PowerShell):

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

2. Instalar dependências:

```powershell
pip install -r requirements.txt
```

3. Executar o app (porta padrão 8501):

```powershell
python -m streamlit run app.py --server.port 8501 --server.headless true
```

Abra no navegador: `http://localhost:8501`

## Observações 💡
- O projeto inclui `vehicles.csv`. Se o arquivo for muito grande, use amostra no `app.py` durante o desenvolvimento (`pd.read_csv('vehicles.csv', nrows=10000)`).
- Recomenda-se não commitar ambientes virtuais (ex.: `.venv/`) — já incluído no `.gitignore`.
- Para grandes arquivos de dados, considere usar Git LFS.

---

Se quiser, posso adicionar instruções extra (como como usar `git lfs`) ou um arquivo `requirements.txt` gerado automaticamente. Diga se quer que eu adicione isso.