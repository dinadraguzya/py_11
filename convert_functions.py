import os
import osa
import math


def load_file(file_path):
    with open(file_path) as opened_file:
        return opened_file.read()


def convert_temperature_from_fahrenheit_to_celsius(data):
    client = osa.Client('http://www.webservicex.net/ConvertTemperature.asmx?WSDL')
    temperatures_list = data.replace(' F', '').split('\n')
    converted_temperatures_list = list()
    for temperature in temperatures_list:
        converted_temperatures_list.append(client.service.ConvertTemp(temperature, 'degreeFahrenheit', 'degreeCelsius'))
    return converted_temperatures_list


def get_average_weekly_temperature(temperatures_list):
    return round(sum(temperatures_list)/len(temperatures_list), 2)


def transform_data_to_dict(data):
    data = data.replace(':', '').split('\n')
    data_dict = dict()
    for item in data:
        item_list = item.split(' ')
        data_dict[item_list[0]] = [item_list[1], item_list[2]]
    return data_dict


def convert_currency(currency_dict):
    client = osa.Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')
    for key, value in currency_dict.items():
        if value[1] not in 'RUB':
            converted_value = client.service.ConvertToNum('', value[1], 'RUB', value[0], True, '', '')
            currency_dict[key] = [math.ceil(converted_value), 'RUB']
    return currency_dict


def convert_distance(distance_dict):
    client = osa.Client('http://www.webservicex.net/length.asmx?WSDL')
    for key, value in distance_dict.items():
        converted_value = client.service.ChangeLengthUnit(value[0].replace(',', ''), 'Miles', 'Kilometers')
        distance_dict[key] = [converted_value, 'km']
    return distance_dict


def get_total_distance(distance_dict):
    sum = 0
    for item in distance_dict.values():
        sum += item[0]
    return round(sum, 2)


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Paths to files
    temps_data = load_file(current_dir + '/temps.txt')
    currencies_data = load_file(current_dir + '/currencies.txt')
    distances_data = load_file(current_dir + '/travel.txt')
    # Transform data
    temps_list = convert_temperature_from_fahrenheit_to_celsius(temps_data)
    currencies_dict = transform_data_to_dict(currencies_data)
    converted_currencies = convert_currency(currencies_dict)
    distances_dict = transform_data_to_dict(distances_data)
    converted_distances = convert_distance(distances_dict)

    print('Средняя арифметическая температура за неделю по Цельсию составляет: ',
          get_average_weekly_temperature(temps_list))
    print('\nЗатраты на путешествия в рублях: ')
    for key, value in converted_currencies.items():
        print(f'{key}: {value[0]} {value[1]}')
    print('\nСуммарное расстояние пути в километрах составляет: ', get_total_distance(converted_distances))