from models.Car import Car
from stringUtils import transformCarNumber


class User:
    def __init__(self, chat_id='', last_name='', first_name='', middle_name='', phone='', flat='', cars=None):
        if cars is None:
            cars = []
        self.chat_id = chat_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.phone = phone
        self.flat = flat
        self.cars = cars

    def setupByDict(self, dictionary):
        self.chat_id = dictionary.get("chat_id", "")
        self.last_name = dictionary.get("last_name", "")
        self.first_name = dictionary.get("first_name", "")
        self.middle_name = dictionary.get("middle_name", "")
        self.phone = dictionary.get("phone", "")
        self.flat = dictionary.get("flat", "")
        car_numbers = dictionary.get("car_numbers", None)
        if car_numbers is not None:
            cars = []
            for number in car_numbers:
                cars.append(Car(transformCarNumber(number)))
            self.cars = cars

