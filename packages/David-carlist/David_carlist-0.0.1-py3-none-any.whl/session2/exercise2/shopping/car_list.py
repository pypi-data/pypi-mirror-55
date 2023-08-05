from session2.exercise2.cars.sample import bmw, mercedes, renault


def list_cars_by_brand(brand_name):
    brand_list = {
        'bmw': bmw,
        'mercedes': mercedes,
        'renault': renault
    }

    if brand_name.lower() in brand_list.keys():
        for model in brand_list[brand_name.lower()].car_models:
            print(model)
    else:
        print('This car is not in our catalogue')


while True:
    brand = input('Type a brand name to list cars: ')
    if brand == 'exit': break
    list_cars_by_brand(brand)
