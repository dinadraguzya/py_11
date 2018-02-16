import os
import osa


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


def convert_currency(data):
    pass


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    temps_data = load_file(current_dir + '/temps.txt')
    temps_list = convert_temperature_from_fahrenheit_to_celsius(temps_data)
    print(get_average_weekly_temperature(temps_list))