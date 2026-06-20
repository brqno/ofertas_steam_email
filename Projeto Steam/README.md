# Projeto Steam

Esse projeto busca promoções na Steam usando a API do CheapShark, gera um relatório Excel e envia por email.

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

1. Crie e ative seu ambiente virtual:
   - Windows PowerShell:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

2. Instale as dependências:
   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Configure variáveis de ambiente:
   - Copie o arquivo de exemplo:
     ```powershell
     copy .env.example .env
     ```
   - Edite `.env` com suas credenciais SMTP e ajustes de filtro.

## Executando

```powershell
python main.py
```

## Variáveis de ambiente suportadas

- `SMTP_HOST` - host SMTP (padrão: `smtp.gmail.com`)
- `SMTP_PORT` - porta SMTP (padrão: `465`)
- `SMTP_USER` - usuário do SMTP
- `SMTP_PASSWORD` - senha ou app password
- `EMAIL_FROM` - remetente do email
- `EMAIL_TO` - destinatário do email
- `MIN_PRICE_BR` - preço mínimo em reais para filtrar jogos
- `MAX_PRICE_BR` - preço máximo em reais (deixe vazio para sem limite)
- `WISHLIST_LIMIT` - quantidade de ofertas a validar na CheapShark

## GitHub

- `.env` está incluído no `.gitignore` para evitar vazar credenciais sensíveis.
- Use `.env.example` como referência para configurar seu ambiente local.
