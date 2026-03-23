
import requests # позволяет скачивать программе веб-страницы
import time     # нужен для пауз между запросами
import json     # для сохранения данных в файл
from bs4 import BeautifulSoup  # для разбора HTML-кода страниц
from urllib.parse import urljoin  # для правильной склейки адресов
from typing import List, Dict

# Настройки
BASE_URL = "https://ru.wikipedia.org"  #глав.адрес википедии

# 2) Получение случайной статьи через API

# специальный адрес (API), который
# сразу возвращает случайную статью в
# удобном формате
RANDOM_API = "https://ru.wikipedia.org/api/rest_v1/page/random/summary"

# "маскировка" под браузер, чтобы сайт не заблокировал программу
HEADERS = {
    "User-Agent": "Mozilla/5.0 (SeminarScraper/1.0; +https://example.org/)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ru,en;q=0.8",
}

# Создаем сессию для переиспользования соединений
session = requests.Session()
session.headers.update(HEADERS)

# 3)  Функция получения случайной статьи
#Обращается к специальному адресу Википедии, который даёт случайную статью
#Получает ответ в формате JSON (как словарь)
#Извлекает оттуда название статьи и составляет её полный адрес
#Возвращает эту информацию


def get_random_article_info() -> Dict:
    """
    Получает информацию о случайной статье через REST API
    """
    try:
        response = session.get(RANDOM_API, timeout=20)
        response.raise_for_status()
        data = response.json()

        return {
            'title': data.get('title', 'Unknown'),
            'url': f"{BASE_URL}/wiki/{data.get('title', '').replace(' ', '_')}",
            'description': data.get('description', ''),
            'extract': data.get('extract', '')
        }
    except Exception as e:
        print(f"Ошибка при получении случайной статьи: {e}")
        return None

# 4) Функция извлечения ссылок
#Находит на странице все ссылки (<a href="...">)
#Оставляет только ссылки на статьи Википедии (начинаются с /wiki/)
#Исключает служебные страницы (там есть двоеточие :)
#Превращает короткие адреса в полные
#Возвращает список из найденных ссылок

def get_article_links(soup: BeautifulSoup, base_url: str, max_links: int = 10) -> List[str]:
    """
    Извлекает ссылки на другие статьи Википедии из HTML
    """
    links = []

    # Ищем все ссылки на статьи Википедии
    for link in soup.find_all('a', href=True):
        href = link['href']

        # Фильтруем: только ссылки на статьи (не служебные, не файлы и т.д.)
        if href.startswith('/wiki/') and ':' not in href:
            full_url = urljoin(base_url, href)
            links.append(full_url)

            if len(links) >= max_links:
                break

    return links

# 5) Функция посещения страницы (самая важная!)

def visit_page(url: str, visited_pages: List[Dict], depth: int = 0):
    """
    Посещает страницу, извлекает информацию и ссылки
    """
    try:
        print(f"{'  ' * depth}Посещаем: {url}")

        response = session.get(url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # Извлекаем заголовок
        title_elem = soup.find('h1')
        title = title_elem.get_text(strip=True) if title_elem else 'Unknown'

        # Сохраняем информацию о посещенной странице
        page_info = {
            'url': url,
            'title': title,
            'depth': depth,
            'timestamp': time.time()
        }
        visited_pages.append(page_info)

        print(f"{'  ' * depth}Заголовок: {title}")

        # Если это не последний уровень, ищем ссылки
        if depth < 2:  # Переходим максимум на 2 уровня вглубь
            links = get_article_links(soup, BASE_URL, max_links=5)

            if links:
                # Выбираем первую ссылку (можно изменить логику выбора)
                next_url = links[0]
                print(f"{'  ' * depth}Найдена ссылка: {next_url}")

                # Добавляем задержку между запросами
                time.sleep(1)

                # Рекурсивно переходим по ссылке
                visit_page(next_url, visited_pages, depth + 1)
            else:
                print(f"{'  ' * depth}Ссылок не найдено")

        return True

    except Exception as e:
        print(f"{'  ' * depth}Ошибка при посещении {url}: {e}")
        return False

# 6) Сохранение результатов в двух форматах
#
# JSON (visited_pages.json) — для программной обработки
#
# TXT (visited_pages.txt) — для чтения человеком


def save_results(visited_pages: List[Dict], filename: str = 'visited_pages.json'):
    """
    Сохраняет результаты в JSON файл
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(visited_pages, f, ensure_ascii=False, indent=2)
        print(f"\nРезультаты сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

# 7) главная функция
def main():
    print("=" * 60)
    print("Сбор данных со случайной статьи Википедии")
    print("=" * 60)

    visited_pages = []

    # 1. Получаем случайную статью через API
    print("\n1. Получение случайной статьи...")
    random_article = get_random_article_info()

    if not random_article:
        print("Не удалось получить случайную статью. Завершаем работу.")
        return

    print(f"Случайная статья: {random_article['title']}")
    print(f"URL: {random_article['url']}")
    print(f"Описание: {random_article['description']}")

    # 2. Посещаем случайную статью
    print("\n2. Начинаем обход страниц...")
    visit_page(random_article['url'], visited_pages, depth=0)

    # 3. Выводим статистику
    print("\n" + "=" * 60)
    print("ИТОГИ ОБХОДА:")
    print("=" * 60)
    print(f"Посещено страниц: {len(visited_pages)}")

    for i, page in enumerate(visited_pages, 1):
        print(f"{i}. {page['title']} (глубина {page['depth']})")
        print(f"   URL: {page['url']}")

    # 4. Сохраняем результаты
    save_results(visited_pages)

    # 5. Дополнительно сохраняем в читаемом формате
    with open('visited_pages.txt', 'w', encoding='utf-8') as f:
        f.write("Посещенные страницы:\n")
        f.write("=" * 60 + "\n")
        for page in visited_pages:
            f.write(f"\nГлубина {page['depth']}: {page['title']}\n")
            f.write(f"URL: {page['url']}\n")
            f.write(f"Время: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(page['timestamp']))}\n")
            f.write("-" * 40 + "\n")

    print(f"\nТакже сохранен читаемый файл: visited_pages.txt")


# Исправленная версия для работы с предоставленным кодом
def alternative_approach():
    """
    Альтернативный подход, интегрирующийся с существующим кодом
    """
    print("=" * 60)
    print("Альтернативный подход (с использованием существующего кода)")
    print("=" * 60)

    # Исправляем проблему с headers
    headers = {
        "User-Agent": "Mozilla/5.0 (SeminarScraper/1.0; +https://example.org/)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "ru,en;q=0.8",
    }

    session = requests.Session()
    session.headers.update(headers)

    visited = []

    # Получаем случайную статью через API
    try:
        print("\n1. Запрос случайной статьи через API...")
        api_response = session.get(RANDOM_API, timeout=20)
        api_data = api_response.json()

        start_url = f"{BASE_URL}/wiki/{api_data['title'].replace(' ', '_')}"
        start_title = api_data['title']

        print(f"Стартовая статья: {start_title}")
        print(f"URL: {start_url}")

        # Сохраняем стартовую страницу
        visited.append({
            'url': start_url,
            'title': start_title,
            'depth': 0
        })

        current_url = start_url
        current_depth = 0

        # Проходим по ссылкам
        while current_depth < 3:  # Идем на 3 уровня вглубь
            print(f"\n{'  ' * current_depth}Посещаем глубину {current_depth}: {current_url}")

            response = session.get(current_url, timeout=20)
            soup = BeautifulSoup(response.text, 'lxml')

            # Ищем ссылки на другие статьи
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/wiki/') and ':' not in href:
                    full_url = urljoin(BASE_URL, href)
                    links.append(full_url)
                    if len(links) >= 3:
                        break

            if not links:
                print(f"{'  ' * current_depth}Ссылок не найдено, останов")
                break

            # Выбираем первую ссылку
            next_url = links[0]

            # Получаем заголовок следующей статьи
            next_response = session.get(next_url, timeout=20)
            next_soup = BeautifulSoup(next_response.text, 'lxml')
            next_title = next_soup.find('h1').get_text(strip=True)

            # Сохраняем информацию
            visited.append({
                'url': next_url,
                'title': next_title,
                'depth': current_depth + 1
            })

            print(f"{'  ' * current_depth}-> {next_title}")

            current_url = next_url
            current_depth += 1

            # Задержка между запросами
            time.sleep(1)

        # Сохраняем результаты
        print("\n" + "=" * 60)
        print("СОХРАНЕННЫЕ СТРАНИЦЫ:")
        print("=" * 60)

        for i, page in enumerate(visited, 1):
            print(f"{i}. {page['title']}")
            print(f"   URL: {page['url']}")

        # Сохраняем в файл
        with open('visited_pages.json', 'w', encoding='utf-8') as f:
            json.dump(visited, f, ensure_ascii=False, indent=2)

        with open('visited_pages.txt', 'w', encoding='utf-8') as f:
            for page in visited:
                f.write(f"{page['title']}\n{page['url']}\n\n")

        print("\nРезультаты сохранены в visited_pages.json и visited_pages.txt")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    # Запускаем основной вариант
    main()

    print("\n" + "=" * 60)
    print("Хотите запустить альтернативный вариант? (да/нет)")
    # Для автоматического запуска раскомментируйте следующую строку:
    # alternative_approach()