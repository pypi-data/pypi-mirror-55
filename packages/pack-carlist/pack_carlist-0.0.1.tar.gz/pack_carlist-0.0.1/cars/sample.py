from cars.bmw import BMW
from cars.volvo import Volvo
from cars.fiat import Fiat


bmw_class = BMW()

volvo_class = Volvo()

fiat_class = Fiat()


if __name__ == "__main__":
    print(bmw_class.get_cars())
    print(volvo_class.get_cars())
    print(fiat_class.get_cars())