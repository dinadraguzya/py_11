import sys
import os


def load_cook_book(file_path):
  cook_book = dict()
  with open(file_path) as recipe_book:
    for line in recipe_book:
      dish_name = line.strip().lower()
      cook_book[dish_name] = list()
      ingridients_quantity = int(recipe_book.readline())
      for line in range(ingridients_quantity):
        ingridient = recipe_book.readline().split(' | ')
        ingridient_dict = dict()
        ingridient_dict['ingridient_name'] = ingridient[0]
        ingridient_dict['quantity'] = ingridient[1]
        ingridient_dict['measure'] = ingridient[2].strip()
        cook_book[dish_name].append(ingridient_dict)
      recipe_book.readline()
    return cook_book


def get_shop_list_by_dishes(cook_book, dishes, person_count):
  shop_list = {}
  for dish in dishes:
    for ingridient in cook_book[dish]:
      new_shop_list_item = dict(ingridient)

      new_shop_list_item['quantity'] *= person_count
      if new_shop_list_item['ingridient_name'] not in shop_list:
        shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
      else:
        shop_list[new_shop_list_item['ingridient_name']]['quantity'] += new_shop_list_item['quantity']
  return shop_list


def print_shop_list(shop_list):
  for shop_list_item in shop_list.values():
    print('{} {} {}'.format(shop_list_item['ingridient_name'], shop_list_item['quantity'],
                            shop_list_item['measure']))


def create_shop_list(cook_book):
  person_count = int(input('Введите количество человек: '))
  dishes = input('Введите блюда в расчете на одного человека (через запятую): ') \
    .lower().split(', ')
  shop_list = get_shop_list_by_dishes(cook_book, dishes, person_count)
  print_shop_list(shop_list)


if __name__ == '__main__':
  recipe_file_path = sys.argv[1]
  if os.path.exists(recipe_file_path) and os.path.isfile(recipe_file_path):
    cook_book = load_cook_book(recipe_file_path)
    create_shop_list(cook_book)
  else:
      print("The file doesn't exist!")