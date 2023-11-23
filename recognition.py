import re


def extract_route(text):
    text = text.replace('-', ' ')
    pattern = r'([а-яА-Я]+\s*\d+)\s*в\s*([а-яА-Я]+\s*\d+)'
    match = re.search(pattern, text)

    if match:
        start = match.group(1).replace(' ', '-')
        end = match.group(2).replace(' ', '-')
        return f'{start} {end}'
    else:
        return None



#route = extract_route(text)
#if route:
#    print(route)
#else:
#    print('Маршрут не найден.')
