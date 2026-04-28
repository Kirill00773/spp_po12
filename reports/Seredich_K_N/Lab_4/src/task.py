"""
Анализ трендов GitHub-репозиториев.

Скрипт получает популярные репозитории по заданному языку
и строит график их популярности.
"""

import os
import datetime
import requests
import matplotlib.pyplot as plt


GITHUB_API_URL = "https://api.github.com/search/repositories"


def get_user_input():
    """Получение параметров от пользователя."""
    language = input("Введите язык программирования: ").strip()

    period_input = input("Введите период анализа (от 1 до 30 дней): ").strip()

    if not period_input.isdigit():
        raise ValueError("Период должен быть числом")

    period = int(period_input)

    if period < 1 or period > 30:
        raise ValueError("Период должен быть от 1 до 30 дней")

    min_stars_input = input("Минимальное количество звёзд (по желанию): ").strip()

    min_stars = int(min_stars_input) if min_stars_input else 0

    return language, period, min_stars


def build_query(language, period, min_stars):
    """Формирование поискового запроса."""
    date_from = datetime.datetime.now() - datetime.timedelta(days=period)
    date_str = date_from.strftime("%Y-%m-%d")

    query = f"language:{language} created:>{date_str} stars:>={min_stars}"
    return query


def fetch_repositories(query):
    """Получение репозиториев через GitHub API."""
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 10,
    }

    response = requests.get(GITHUB_API_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json().get("items", [])


def extract_repo_data(repos):
    """Извлечение нужных данных."""
    result = []

    for repo in repos:
        repo_info = {
            "name": repo["name"],
            "author": repo["owner"]["login"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo["language"],
            "description": repo["description"],
            "url": repo["html_url"],
        }
        result.append(repo_info)

    return result


def print_top_repositories(repos):
    """Вывод ТОП-5 репозиториев."""
    print("\nТОП-5 самых быстрорастущих проектов:")

    for index, repo in enumerate(repos[:5], start=1):
        print(
            f"{index}. **{repo['name']}** "
            f"({repo['stars']} ⭐) - {repo['description']}"
        )


def plot_results(repos, language):
    """Построение и сохранение графика."""
    if not repos:
        print("Нет данных для построения графика")
        return

    names = [repo["name"] for repo in repos[:5]]
    stars = [repo["stars"] for repo in repos[:5]]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, stars)

    plt.title(f"Топ репозиториев ({language})", fontsize=14)
    plt.xlabel("Репозитории")
    plt.ylabel("Количество звёзд")

    plt.xticks(rotation=30, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Подписи значений на столбцах
    for bar_item in bars:
        height = bar_item.get_height()
        plt.text(
            bar_item.get_x() + bar_item.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    filename = f"trending_{language.lower()}.png"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    plt.savefig(filepath)
    plt.close()

    print(f"\nГрафик сохранён в '{filepath}'")


def main():
    """Основная функция."""
    try:
        language, period, min_stars = get_user_input()

        print(
            f"\nАнализируем популярные репозитории на {language} "
            f"за последние {period} дней..."
        )

        query = build_query(language, period, min_stars)
        repos = fetch_repositories(query)
        repo_data = extract_repo_data(repos)

        print_top_repositories(repo_data)
        plot_results(repo_data, language)

    except Exception as error:  # pylint: disable=broad-except
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
