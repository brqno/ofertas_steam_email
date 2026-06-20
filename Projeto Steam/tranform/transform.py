import pandas as pd
from pathlib import Path


def transform_to_dataframe(jogos, output_path=None):
    if not jogos:
        print('Nenhum jogo disponível para transformar.')
        return None, None

    df = pd.DataFrame(jogos)
    output_path = Path(output_path or Path.cwd() / 'steam_promocoes.xlsx')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f'✅ Excel salvo em: {output_path}')
    return df, output_path
