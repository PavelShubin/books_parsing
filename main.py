from bs4 import BeautifulSoup
from time import time
import json, csv
import requests


start = time()
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

result_data = []

for i in range(1, 17):
    url = f'https://www.labirint.ru/genres/2308/?available=3&page={i}&histlab=9470600351'
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')

    main_block = soup.find('div', class_="inner-catalog")
    items = main_block.find_all('div', class_="genres-carousel__item")
    for item in items:
        title = item.find(class_='product-title').text.strip()
        autor = item.find(class_="product-author")
        if autor:
            autor = autor.text.strip()
        else:
            autor = '-'

        published = item.find(class_="product-pubhouse").text.strip()

        new_price = int(item.find(class_="price-val").find('span').text.strip().replace(' ', ''))

        old_price = item.find(class_="price-old")
        book_sale = 0
        if old_price:
            old_price = int(old_price.text.replace(' ', ''))
            book_sale = 100 - int(round((new_price/old_price), 2) * 100)
        else:
            old_price = new_price

        result_data.append({
            'book_title': title,
            'book_autor': autor,
            'new_price': new_price,
            'old_price': old_price,
            'book_sale': book_sale
        })
    print(f'Обработка страницы {i}/16 завершена')


with open('data/data.json', 'w', encoding='utf-8') as file:
    json.dump(result_data, file, ensure_ascii=False, indent=4)
    print("Запись в data.json завершена")


with open('data/data.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    main_row = result_data[0].keys()
    writer.writerow(main_row)
    for item in result_data:
        row = list(item.values())
        writer.writerow(row)
    print('Запись в data.csv завершена')

print(f'Затраченное время: {time() - start}')