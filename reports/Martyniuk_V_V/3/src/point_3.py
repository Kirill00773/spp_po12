from abc import ABC, abstractmethod


class ATMState(ABC):
    def __init__(self, atm):
        self.atm = atm

    @abstractmethod
    def insert_card(self):
        pass

    @abstractmethod
    def enter_pin(self, pin):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def eject_card(self):
        pass


class IdleState(ATMState):
    def insert_card(self):
        print("Карта вставлена")
        self.atm.state = self.atm.card_inserted

    def enter_pin(self, pin):
        print("Сначала вставьте карту")

    def withdraw(self, amount):
        print("Сначала вставьте карту")

    def eject_card(self):
        print("Нет карты")


class CardInsertedState(ATMState):
    def insert_card(self):
        print("Карта уже вставлена")

    def enter_pin(self, pin):
        if pin == "1234":
            print("Пин принят")
            self.atm.state = self.atm.authenticated
        else:
            print("Неверный пин")
            self.atm.attempts += 1
            if self.atm.attempts >= 3:
                print("Карта заблокирована")
                self.atm.state = self.atm.blocked

    def withdraw(self, amount):
        print("Введите пин")

    def eject_card(self):
        print("Карта извлечена")
        self.atm.state = self.atm.idle
        self.atm.attempts = 0


class AuthenticatedState(ATMState):
    def insert_card(self):
        print("Карта уже вставлена")

    def enter_pin(self, pin):
        print("Пин уже введен")

    def withdraw(self, amount):
        if amount > self.atm.balance:
            print(f"Недостаточно. Доступно: {self.atm.balance}")
            return

        if amount > self.atm.daily_limit:
            print(f"Лимит {self.atm.daily_limit}")
            return

        self.atm.balance -= amount
        print(f"Выдано {amount}. Остаток: {self.atm.balance}")

        if self.atm.balance == 0:
            print("Деньги закончились")
            self.atm.state = self.atm.empty

    def eject_card(self):
        print("Карта извлечена")
        self.atm.state = self.atm.idle
        self.atm.attempts = 0


class EmptyState(ATMState):
    def insert_card(self):
        print("Нет денег")

    def enter_pin(self, pin):
        print("Нет денег")

    def withdraw(self, amount):
        print("Нет денег")

    def eject_card(self):
        print("Карта извлечена")
        self.atm.state = self.atm.idle


class BlockedState(ATMState):
    def insert_card(self):
        print("Карта заблокирована")

    def enter_pin(self, pin):
        print("Карта заблокирована")

    def withdraw(self, amount):
        print("Карта заблокирована")

    def eject_card(self):
        print("Извлечение невозможно")


class ATM:
    def __init__(self, atm_id, balance):
        self.atm_id = atm_id
        self.balance = balance
        self.daily_limit = 10000
        self.attempts = 0

        self.idle = IdleState(self)
        self.card_inserted = CardInsertedState(self)
        self.authenticated = AuthenticatedState(self)
        self.empty = EmptyState(self)
        self.blocked = BlockedState(self)

        self.state = self.idle

    def insert_card(self):
        self.state.insert_card()

    def enter_pin(self, pin):
        self.state.enter_pin(pin)

    def withdraw(self, amount):
        self.state.withdraw(amount)

    def eject_card(self):
        self.state.eject_card()

    def status(self):
        print(f"\nATM {self.atm_id}")
        print(f"State: {self.state.__class__.__name__}")
        print(f"Balance: {self.balance}")
        print(f"Attempts: {self.attempts}")


if __name__ == "__main__":
    atm1 = ATM("ATM001", 5000)

    print("=== Сценарий 1: Успешная операция ===")
    atm1.insert_card()
    atm1.enter_pin("1234")
    atm1.withdraw(2000)
    atm1.eject_card()

    print("\n=== Сценарий 2: Неверный пин ===")
    atm1.insert_card()
    atm1.enter_pin("0000")
    atm1.enter_pin("1111")
    atm1.enter_pin("2222")
    atm1.insert_card()

    print("\n=== Сценарий 3: Снятие больше чем есть ===")
    atm2 = ATM("ATM002", 1000)
    atm2.insert_card()
    atm2.enter_pin("1234")
    atm2.withdraw(2000)
    atm2.withdraw(500)
    atm2.eject_card()

    print("\n=== Сценарий 4: Пустой банкомат ===")
    atm3 = ATM("ATM003", 500)
    atm3.insert_card()
    atm3.enter_pin("1234")
    atm3.withdraw(500)
    atm3.insert_card()
    atm3.enter_pin("1234")
