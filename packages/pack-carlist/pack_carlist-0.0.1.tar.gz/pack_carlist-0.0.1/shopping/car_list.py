from cars.bmw import BMW
from cars.volvo import Volvo
from cars.fiat import Fiat


def get_cars_by_brand(brand_name):
    if brand_name.lower() == "bmw":
        bmw_class = BMW()
        return bmw_class.get_cars()
    elif brand_name.lower() == "volvo":
        volvo_class = Volvo()
        return volvo_class.get_cars()
    elif brand_name.lower() == 'fiat':
        fiat_class = Fiat()
        return fiat_class.get_cars()
    else:
        return "Class does not exist"


if __name__ == '__main__':
    brand = input("Which car brand would you like to see?")
    print(get_cars_by_brand(brand))