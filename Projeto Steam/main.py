from extract.extract import buscar_promocoes_gerais, MIN_PRICE_BR, MAX_PRICE_BR
from tranform.transform import transform_to_dataframe
from shipping.shipping import send_email_report
from pathlib import Path


def main():
    jogos = buscar_promocoes_gerais()
    if not jogos:
        print('Nenhum jogo encontrado. Cancelando a transformação e envio.')
        return

    df, excel_path = transform_to_dataframe(jogos, output_path='steam_promocoes.xlsx')
    if df is None or excel_path is None:
        print('Falha ao gerar o Excel.')
        return

    subject = f'Relatório de jogos Steam acima de R$ {MIN_PRICE_BR:.2f}'
    body = f'Foram encontrados {len(df)} jogos que atendem ao filtro de preço. O arquivo Excel está em anexo.'
    success = send_email_report(subject, body, attachment_path=excel_path)
    if not success:
        print('O relatório foi gerado, mas o envio de email falhou.')
    else:
        try:
            Path(excel_path).unlink()
            print(f'🗑️ Arquivo removido após envio: {excel_path}')
        except Exception as e:
            print(f'Não foi possível remover o arquivo: {e}')


if __name__ == '__main__':
    main()
