import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
EMAIL_FROM = os.environ.get('EMAIL_FROM', SMTP_USER)
EMAIL_TO = os.environ.get('EMAIL_TO', '')


def send_email_report(subject, body, attachment_path=None):
    if not SMTP_USER or not SMTP_PASSWORD or not EMAIL_TO:
        print('Configuração SMTP incompleta. Defina SMTP_USER, SMTP_PASSWORD e EMAIL_TO nas variáveis de ambiente.')
        return False

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg.set_content(body)

    if attachment_path:
        attachment_path = Path(attachment_path)
        if not attachment_path.exists():
            print(f'Anexo não encontrado: {attachment_path}')
            return False
        with attachment_path.open('rb') as f:
            data = f.read()
        msg.add_attachment(
            data,
            maintype='application',
            subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=attachment_path.name,
        )

    try:
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()

        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f'📧 Email enviado para {EMAIL_TO}')
        return True
    except Exception as e:
        print(f'Falha ao enviar email: {e}')
        return False
