from models.Car import Car
from stringUtils import transformCarNumber


class User:
    def __init__(self, last_name='', first_name='', middle_name='', phone='', flat='', cars=None):
        if cars is None:
            cars = []
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.phone = phone
        self.flat = flat
        self.cars = cars

    def setupByDict(self, dictionary):
        self.last_name = dictionary['last_name']
        self.first_name = dictionary['first_name']
        self.middle_name = dictionary['middle_name']
        self.phone = dictionary['phone']
        self.flat = dictionary['flat']
        car_numbers = dictionary.get("car_numbers", None)
        if car_numbers is not None:
            cars = []
            for number in car_numbers:
                cars.append(Car(transformCarNumber(number)))
            self.cars = cars

