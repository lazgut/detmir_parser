import requests
import csv

# Заголовки запросов, чтобы не получить бан от detmir.ru
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://www.detmir.ru",
    "referer": "https://www.detmir.ru/",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/103.0.0.0 Safari/537.36",
    "x-requested-with": "detmir-ui"
}


def collect_data(page_name: str, city: str):  # Функция по сборы данных и записи в файл CSV
                                              # На вход получает имя страницы раздела и город
    url = f'https://api.detmir.ru/v2/products?filter=categories[].alias:{page_name};promo:false;withregion:RU-{city}' \
          f'&expand=meta.facet.ages.adults,meta.facet.gender.adults,webp&meta=*&limit=30&offset=0&sort=popularity:desc'
    result = []
    length = requests.get(url=url, headers=headers).json()['meta']['length']  # Для offset

    for i in range(0, (length // 30 + 1) * 30, 30):
        response = requests.get(url=f'https://api.detmir.ru/v2/products?filter=categories[].alias:{page_name};'
                                    f'promo:false;withregion:RU-{city}&expand=meta.facet.ages.adults,meta.facet.gender.'
                                    f'adults,webp&meta=*&limit=30&offset={i}&sort=popularity:desc', headers=headers)
        items = response.json()['items']

        for item in items:
            item_id = item['id']
            item_name = item['title']

            try:  # Узнаем есть промо цена или только обычная
                item_price = f"{item['old_price']['price']} {item['old_price']['currency']}"
                item_promo_price = f"{item['price']['price']} {item['price']['currency']}"
            except TypeError:
                item_price = f"{item['price']['price']} {item['price']['currency']}"
                item_promo_price = "Отсутствует"

            item_url = item['link']['web_url']

            result.append(
                [item_id, item_name, item_price, item_promo_price, item_url]
            )

    with open(f'{city}_{page_name}.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(  # Создаем строчку с названием столбцов
            (
                'id',
                'title',
                'price',
                'promo_price',
                'url'
            )
        )
        writer.writerows(  # Записываем наш полученный список значений
            result
        )


def main():
    collect_data('detskoe_oruzhie', 'MOW')
    collect_data('detskoe_oruzhie', 'SPE')
    collect_data('mashiny', 'MOW')
    collect_data('mashiny', 'SPE')
    collect_data('sets_cartoon_characters', 'MOW')
    collect_data('sets_cartoon_characters', 'SPE')


if __name__ == '__main__':
    main()
