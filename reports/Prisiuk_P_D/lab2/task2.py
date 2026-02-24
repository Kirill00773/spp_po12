"""
Модуль, реализующий систему 'Железнодорожная касса' (Задание 2).
"""

from typing import List, Optional
from datetime import datetime


class Request:
    """Класс заявки пассажира."""

    # pylint: disable=too-few-public-methods

    def __init__(self, destination: str, travel_date: datetime):
        self.destination = destination
        self.travel_date = travel_date

    def __str__(self) -> str:
        date_str = self.travel_date.strftime("%Y-%m-%d %H:%M")
        return f"Заявка: станция '{self.destination}', дата {date_str}"


class Train:
    """Класс поезда."""

    def __init__(self, number: str, route: List[str],
                 departure_time: datetime, price: float):
        self.number = number
        self.route = route  # Список станций (промежуточные и конечная)
        self.departure_time = departure_time
        self.price = price

    def serves_station(self, station: str) -> bool:
        """Проверяет, проходит ли поезд через указанную станцию."""
        return station in self.route

    def __str__(self) -> str:
        return f"Поезд {self.number} (Маршрут: {' -> '.join(self.route)})"


class Invoice:
    """Класс счета на оплату."""

    def __init__(self, passenger_name: str, train: Train, amount: float):
        self.passenger_name = passenger_name
        self.train = train
        self.amount = amount
        self.is_paid = False

    def pay(self) -> None:
        """Оплатить счет."""
        self.is_paid = True
        print(f"Счет на {self.amount} руб. успешно оплачен.")

    def __str__(self) -> str:
        status = "Оплачен" if self.is_paid else "Не оплачен"
        return (f"Счет для {self.passenger_name} | {self.train} | "
                f"Сумма: {self.amount} | Статус: {status}")


class User:
    """Базовый класс пользователя (Обобщение)."""

    # pylint: disable=too-few-public-methods

    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name


class Administrator(User):
    """Класс администратора системы."""

    # pylint: disable=too-few-public-methods

    def add_train(self, system: 'RailwaySystem', train: Train) -> None:
        """Добавляет поезд в систему."""
        system.register_train(train)
        print(f"Администратор {self.name} добавил {train}.")


class Passenger(User):
    """Класс пассажира."""

    def create_request(self, destination: str, date: datetime) -> Request:
        """Создает заявку."""
        return Request(destination, date)

    def choose_train(self, trains: List[Train], index: int) -> Optional[Train]:
        """Выбирает поезд из предложенного списка."""
        if 0 <= index < len(trains):
            return trains[index]
        return None


class RailwaySystem:
    """Главный класс системы кассы (Агрегация поездов)."""

    def __init__(self) -> None:
        self._trains: List[Train] = []

    def register_train(self, train: Train) -> None:
        """Регистрация поезда в системе."""
        self._trains.append(train)

    def find_trains(self, request: Request) -> List[Train]:
        """Поиск поездов по заявке."""
        found = []
        for train in self._trains:
            if (train.serves_station(request.destination) and
                    train.departure_time.date() == request.travel_date.date()):
                found.append(train)
        return found

    def issue_invoice(self, passenger: Passenger, train: Train) -> Invoice:
        """Формирование счета на оплату."""
        return Invoice(passenger.name, train, train.price)


def main() -> None:
    """Главная функция для демонстрации работы системы."""
    print("\n--- Задание 2 ---")

    # 1. Инициализация системы
    sys = RailwaySystem()

    # 2. Действия Администратора
    admin = Administrator(1, "Иван Петрович")
    date1 = datetime(2023, 12, 1, 10, 0)
    date2 = datetime(2023, 12, 1, 15, 30)

    train1 = Train(
        "001А", ["Москва", "Тверь", "Санкт-Петербург"], date1, 3500.0
    )
    train2 = Train(
        "054Ч", ["Москва", "Владимир", "Нижний Новгород"], date2, 2100.0
    )

    admin.add_train(sys, train1)
    admin.add_train(sys, train2)

    # 3. Действия Пассажира
    passenger = Passenger(101, "Алексей")
    req = passenger.create_request(
        "Санкт-Петербург", datetime(2023, 12, 1, 9, 0)
    )
    print(f"\nПассажир {passenger.name} сделал заявку: {req}")

    # 4. Система ищет подходящие поезда
    available_trains = sys.find_trains(req)
    print(f"Найдено подходящих поездов: {len(available_trains)}")
    for i, trn in enumerate(available_trains):
        print(f"[{i}] {trn} - {trn.price} руб.")

    # 5. Пассажир выбирает поезд и получает счет
    if available_trains:
        chosen = passenger.choose_train(available_trains, 0)
        if chosen:
            print(f"\nПассажир выбрал: {chosen.number}")
            invoice = sys.issue_invoice(passenger, chosen)
            print(invoice)

            # Оплата
            invoice.pay()
            print(invoice)


if __name__ == "__main__":
    main()
