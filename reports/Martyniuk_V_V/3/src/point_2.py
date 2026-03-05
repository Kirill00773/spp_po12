from abc import ABC, abstractmethod


class Level(ABC):
    @abstractmethod
    def desc(self) -> str:
        pass

    @abstractmethod
    def discount(self) -> float:
        pass

    @abstractmethod
    def preorder(self) -> bool:
        pass

    @abstractmethod
    def exclusive(self) -> bool:
        pass


class Base(Level):
    def desc(self) -> str:
        return "Base"

    def discount(self) -> float:
        return 0

    def preorder(self) -> bool:
        return False

    def exclusive(self) -> bool:
        return False


class Silver(Level):
    def desc(self) -> str:
        return "Silver"

    def discount(self) -> float:
        return 0.05

    def preorder(self) -> bool:
        return True

    def exclusive(self) -> bool:
        return False


class Gold(Level):
    def desc(self) -> str:
        return "Gold"

    def discount(self) -> float:
        return 0.1

    def preorder(self) -> bool:
        return True

    def exclusive(self) -> bool:
        return True


class Platinum(Level):
    def desc(self) -> str:
        return "Platinum"

    def discount(self) -> float:
        return 0.15

    def preorder(self) -> bool:
        return True

    def exclusive(self) -> bool:
        return True


class User:
    def __init__(self, name: str):
        self.name = name
        self.spent = 0
        self.level = Base()

    def buy(self, amount: float):
        self.spent += amount
        self.update_level()

    def update_level(self):
        if self.spent >= 50000:
            self.level = Platinum()
        elif self.spent >= 20000:
            self.level = Gold()
        elif self.spent >= 5000:
            self.level = Silver()

    def show(self):
        print(f"{self.name}: {self.level.desc()}")
        print(f"  Discount: {self.level.discount() * 100}%")
        print(f"  Preorder: {self.level.preorder()}")
        print(f"  Exclusive: {self.level.exclusive()}")


if __name__ == "__main__":
    user = User("John")
    user.show()

    user.buy(6000)
    user.show()

    user.buy(20000)
    user.show()

    user.buy(30000)
    user.show()
