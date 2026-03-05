from abc import ABC, abstractmethod


class Car:
    def __init__(self, brand: str, model: str, body_type: str, engine: str):
        self.brand = brand
        self.model = model
        self.body_type = body_type
        self.engine = engine
        self.options = []

    def add_option(self, option: str):
        self.options.append(option)

    def get_info(self) -> str:
        options = f", options: {', '.join(self.options)}" if self.options else ""
        return f"{self.brand} {self.model} ({self.body_type}) - {self.engine}{options}"


class Factory(ABC):
    @abstractmethod
    def create_car(self, body_type: str, model: str) -> Car:
        pass


class ToyotaFactory(Factory):
    def create_car(self, body_type: str, model: str) -> Car:
        specs = {
            "sedan": {"engine": "2.5L Hybrid", "options": ["Safety Sense", "Climate control"]},
            "suv": {"engine": "3.5L V6", "options": ["4WD", "360 camera"]},
            "hatchback": {"engine": "1.8L", "options": ["Park sensors"]},
            "sports": {"engine": "3.0L Twin-Turbo", "options":
                ["Sport suspension", "Carbon brakes"]},
        }

        spec = specs.get(body_type.lower(), {"engine": "2.0L", "options": []})
        car = Car("Toyota", model, body_type, spec["engine"])

        for option in spec["options"]:
            car.add_option(option)

        return car


class BMWFactory(Factory):
    def create_car(self, body_type: str, model: str) -> Car:
        specs = {
            "sedan": {"engine": "2.0L TwinPower Turbo", "options": ["xDrive", "Laser lights"]},
            "suv": {"engine": "4.4L V8", "options": ["Air suspension", "Off-road package"]},
            "hatchback": {"engine": "1.5L", "options": ["Panoramic roof"]},
            "sports": {"engine": "4.0L V8", "options": ["M Performance", "Carbon body"]},
        }

        spec = specs.get(body_type.lower(), {"engine": "2.0L", "options": []})
        car = Car("BMW", model, body_type, spec["engine"])

        for option in spec["options"]:
            car.add_option(option)

        return car


class TeslaFactory(Factory):
    def create_car(self, body_type: str, model: str) -> Car:
        specs = {
            "sedan": {"engine": "Dual Motor Electric", "options": ["Autopilot", "Glass roof"]},
            "suv": {"engine": "Plaid Electric", "options": ["Falcon doors", "Bio defense"]},
            "hatchback": {"engine": "Electric", "options": ["Minimalist interior"]},
            "sports": {"engine": "Roadster Electric", "options": ["SpaceX package", "Insane mode"]},
        }

        spec = specs.get(body_type.lower(), {"engine": "Electric", "options": []})
        car = Car("Tesla", model, body_type, spec["engine"])

        for option in spec["options"]:
            car.add_option(option)

        return car


class Dealership:
    def __init__(self, factory: Factory):
        self.factory = factory
        self.inventory = []

    def order_car(self, body_type: str, model: str) -> Car:
        car = self.factory.create_car(body_type, model)
        self.inventory.append(car)
        return car

    def show_inventory(self):
        for car in self.inventory:
            print(car.get_info())


if __name__ == "__main__":
    toyota_dealer = Dealership(ToyotaFactory())
    bmw_dealer = Dealership(BMWFactory())

    toyota_dealer.order_car("sedan", "Camry")
    toyota_dealer.order_car("suv", "Highlander")
    bmw_dealer.order_car("sedan", "3 Series")
    bmw_dealer.order_car("sports", "M4")

    toyota_dealer.show_inventory()
    bmw_dealer.show_inventory()
