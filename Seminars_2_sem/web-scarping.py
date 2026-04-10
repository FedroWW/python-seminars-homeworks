#реализация случайных блужданий по википеди, создание графа ссылок с расстояниями между ними
#реализация захода на случайную статью через этот сервис, из случайной статьи заходите на какую-то другую статью,
№и оттуда еще на одну (все автоматизированно сделать и по итогу сохранить адреса и title страниц посещенных)


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









#задание:                                                   
#1) выбрать некоторую важную статью в википедии на ваш выбор
#2) используя код выше, начать со случайной статьи и посчитать, сколько раз вам надо перейти по ссылке чтобы дойти до вашей заранее выбранной статьи
#3) провести этот эксперимент несколько раз для разных случайных статей, построить статистику (в виде гистограммы, например)

import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urljoin
import time
import random
import matplotlib.pyplot as plt
from collections import deque

# ---------- Конфигурация ----------
BASE = "https://ru.wikipedia.org"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; WikiWalker/1.0)"}
TARGET_ARTICLE = "Россия"                # 👈 выбранная важная статья
MAX_STEPS = 500                          # лимит шагов во избежание вечного цикла
SLEEP_BETWEEN_REQUESTS = 0.2             # пауза между запросами (вежливость)
NUM_EXPERIMENTS = 40                     # количество запусков

# ---------- Кэш страниц ----------
page_cache = {}  # title -> list соседних статей

# ---------- Вспомогательные функции (из оригинала с небольшими доработками) ----------
def article_to_url(title: str) -> str:
    return f"{BASE}/wiki/{title.replace(' ', '_')}"

def is_valid_article_href(href: str) -> bool:
    if not href.startswith("/wiki/"):
        return False
    title = href[len("/wiki/"):]
    if not title or "#" in title or ":" in title:
        return False
    if title.startswith("Заглавная_страница"):
        return False
    return True

def href_to_title(href: str) -> str:
    return unquote(href[len("/wiki/"):]).replace("_", " ")

def extract_all_links(article_title: str):
    """
    Возвращает список ВСЕХ валидных названий статей, на которые ссылается данная статья.
    Использует кэш для ускорения повторных обращений.
    """
    if article_title in page_cache:
        return page_cache[article_title]

    url = article_to_url(article_title)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Ошибка загрузки '{article_title}': {e}")
        page_cache[article_title] = []
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    content = soup.find("div", id="mw-content-text")
    if not content:
        page_cache[article_title] = []
        return []

    links = []
    seen = set()
    for a in content.find_all("a", href=True):
        href = a["href"]
        if not is_valid_article_href(href):
            continue
        target = href_to_title(href)
        norm_target = target.strip()
        if norm_target.casefold() == article_title.casefold():
            continue
        if norm_target.casefold() in seen:
            continue
        seen.add(norm_target.casefold())
        links.append(target)

    page_cache[article_title] = links
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    return links

def get_random_article():
    """
    Получить название случайной статьи через редирект со спецстраницы.
    """
    random_url = f"{BASE}/wiki/Служебная:Случайная_страница"
    resp = requests.get(random_url, headers=HEADERS, allow_redirects=False, timeout=10)
    if resp.status_code == 302:
        location = resp.headers.get("Location", "")
        if location.startswith("/wiki/"):
            return href_to_title(location)
    # fallback (очень редко)
    resp2 = requests.get(random_url, headers=HEADERS, timeout=10)
    return href_to_title(resp2.url.split("/wiki/")[1])

# ---------- Функция случайного блуждания ----------
def random_walk_to_target(target: str, max_steps: int = MAX_STEPS):
    """
    Начинает со случайной статьи и идёт по случайным ссылкам, пока не встретит целевую.
    Возвращает количество переходов или None, если достигнут лимит шагов.
    """
    current = get_random_article()
    print(f"🚀 Старт: {current}")
    steps = 0
    visited_in_walk = set()

    while steps < max_steps:
        if current.casefold() == target.casefold():
            print(f"✅ Достигнута цель '{target}' за {steps} шагов.")
            return steps

        # Защита от зацикливания внутри одного блуждания (редко, но возможно)
        if current.casefold() in visited_in_walk:
            # Если мы уже были здесь в этом же проходе, выбираем другую ссылку, если есть
            pass
        visited_in_walk.add(current.casefold())

        links = extract_all_links(current)
        if not links:
            print(f"⚠️ У статьи '{current}' нет исходящих ссылок. Остановка.")
            break

        # Случайный выбор следующей статьи
        next_article = random.choice(links)
        print(f"   Шаг {steps+1}: {current} → {next_article}")
        current = next_article
        steps += 1

    print(f"❌ Лимит шагов ({max_steps}) исчерпан, цель не достигнута.")
    return None

# ---------- Запуск экспериментов ----------
results = []
for i in range(NUM_EXPERIMENTS):
    print(f"\n===== Эксперимент {i+1}/{NUM_EXPERIMENTS} =====")
    steps = random_walk_to_target(TARGET_ARTICLE, MAX_STEPS)
    if steps is not None:
        results.append(steps)
    else:
        results.append(MAX_STEPS)  # учитываем как "неудачу" с лимитом

# ---------- Статистика и визуализация ----------
if results:
    plt.figure(figsize=(10, 6))
    plt.hist(results, bins=15, edgecolor='black', alpha=0.7)
    plt.axvline(sum(results)/len(results), color='red', linestyle='dashed', linewidth=2,
                label=f'Среднее: {sum(results)/len(results):.1f}')
    plt.xlabel('Количество переходов до цели')
    plt.ylabel('Частота')
    plt.title(f'Распределение длины случайного блуждания до статьи "{TARGET_ARTICLE}"\n'
              f'({NUM_EXPERIMENTS} запусков, макс. шагов = {MAX_STEPS})')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('histogram_wiki_walk.png', dpi=150)
    plt.show()

    print("\n📊 Итоговая статистика:")
    print(f"   Успешных достижений цели: {len([r for r in results if r < MAX_STEPS])} из {NUM_EXPERIMENTS}")
    print(f"   Минимальное число шагов: {min(results)}")
    print(f"   Максимальное число шагов: {max(results)}")
    print(f"   Среднее число шагов: {sum(results)/len(results):.2f}")
    print(f"   Медиана: {sorted(results)[len(results)//2]}")
else:
    print("Нет данных для отображения.")
