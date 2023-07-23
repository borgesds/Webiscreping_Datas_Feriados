import requests
from bs4 import BeautifulSoup
import re

response = requests.get('https://www.feriados.com.br/feriados-serranopolis_de_minas-mg.php?ano=2023')

content = response.content

site = BeautifulSoup(content, 'html.parser')

states = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT',
    'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO',
    'RR', 'SC', 'SP', 'SE', 'TO'
]

for state in states:
    state = state.lower()

# Localization city -------------------
name_location = site.find('div', attrs={'class': 'rounded_borders'})

title = name_location.find('h2')

title_holiday = title.get_text()

first_space = title_holiday.find(' ')
last_space = title_holiday.rfind(' ')

title_holiday = title_holiday[first_space+1:last_space]

# Holiday table -------------------
holidays_div = site.select('ul.multi-column div')

data_holiday = []

for div in holidays_div:
    type_holiday = div.get('title')
    type_holiday = re.sub(r'<.*?>', '', type_holiday).strip()

    text_holiday = div.get_text(strip=True)

    if ' - ' in text_holiday:
        date_holiday, name_holiday = text_holiday.split(' - ', 1)
    else:
        date_holiday = None
        name_holiday = text_holiday

    info = {
        'tipo_feriado': type_holiday,
        'data': date_holiday,
        'nome_feriado': name_holiday,
        'municipio': title_holiday
    }

    data_holiday.append(info)

# Data processing
for data in data_holiday:
    if data['data'] is None:
        date_from_name = re.search(
            r'(\d{2}/\d{2}/\d{4})', data['nome_feriado']
        )
        if date_from_name:
            data['data'] = date_from_name.group(1)
            data['nome_feriado'] = data['nome_feriado'].replace(
                                                        data['data'], ''
                                                        ).replace('-', ''
                                                                  ).strip()


#for data in data_holiday:
#    print(data)




