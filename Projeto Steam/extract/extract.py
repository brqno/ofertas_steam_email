import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()


def _get_env_float(key, default=None):
    value = os.environ.get(key, '')
    if value is None or value.strip() == '':
        return default
    try:
        return float(value)
    except ValueError:
        print(f"Valor inválido para {key}: {value}. Usando padrão {default}.")
        return default


def _get_env_int(key, default=None):
    value = os.environ.get(key, '')
    if value is None or value.strip() == '':
        return default
    try:
        return int(value)
    except ValueError:
        print(f"Valor inválido para {key}: {value}. Usando padrão {default}.")
        return default


MIN_PRICE_BR = _get_env_float('MIN_PRICE_BR', 10.00)  # jogará apenas jogos com preço maior que esse valor
MAX_PRICE_BR = _get_env_float('MAX_PRICE_BR', None)  # use um número para limitar por cima, ou deixe None para sem limite
WISHLIST_LIMIT = _get_env_int('WISHLIST_LIMIT', 15)  # número de resultados da CheapShark a validar


def buscar_promocoes_gerais():
    print("🤖 Buscando jogos em promoção na CheapShark...")
    url_cheapshark = "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=5"

    try:
        response = requests.get(url_cheapshark)
        response.raise_for_status()
        deals = response.json()
        jogos_validados = []

        print(f"Encontrados {len(deals)} candidatos. Validando preços em Reais na Steam...")

        for item in deals[:WISHLIST_LIMIT]:
            appid = item.get('steamAppID')
            nome_jogo = item.get('title')
            if not appid:
                continue

            url_steam = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=br&l=portuguese"
            res_steam = requests.get(url_steam)
            if res_steam.status_code != 200:
                continue

            dados_steam = res_steam.json()
            app_data = dados_steam.get(str(appid), {})
            if not app_data.get('success'):
                continue

            info = app_data.get('data', {})
            price_info = info.get('price_overview')
            if not price_info:
                continue

            preco_real = price_info['final'] / 100
            aprovado = preco_real > MIN_PRICE_BR and (MAX_PRICE_BR is None or preco_real <= MAX_PRICE_BR)
            if not aprovado:
                continue

            limite_texto = f"acima de R$ {MIN_PRICE_BR:.2f}"
            if MAX_PRICE_BR is not None:
                limite_texto += f" e até R$ {MAX_PRICE_BR:.2f}"
            print(f"✅ {nome_jogo} aprovado! Preço: R$ {preco_real:.2f} ({limite_texto})")

            jogos_validados.append({
                'appid': appid,
                'nome': nome_jogo,
                'preco': price_info['final_formatted'],
                'preco_valor': preco_real,
                'desconto': f"{price_info['discount_percent']}%",
                'link': f"https://store.steampowered.com/app/{appid}"
            })

            time.sleep(1.5)

        return jogos_validados

    except Exception as e:
        print(f"Ocorreu um erro no processo: {e}")
        return []


if __name__ == '__main__':
    jogos_filtrados = buscar_promocoes_gerais()
    if MAX_PRICE_BR is None:
        print(f"\n🎯 Total de jogos encontrados acima de R$ {MIN_PRICE_BR:.2f}: {len(jogos_filtrados)}")
    else:
        print(f"\n🎯 Total de jogos encontrados entre R$ {MIN_PRICE_BR:.2f} e R$ {MAX_PRICE_BR:.2f}: {len(jogos_filtrados)}")