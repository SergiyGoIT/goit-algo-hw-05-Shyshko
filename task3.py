import timeit
from collections import defaultdict

# Алгоритм Боєра-Мура
def boyer_moore(text, pattern):
    # Створюємо таблицю поганих символів для пропуску порівнянь
    bad_char = defaultdict(lambda: -1)
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i
    
    m, n = len(pattern), len(text)
    s = 0  # Зсув шаблону
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s  # Знайдено збіг
        else:
            # Зсув на основі правила поганого символу
            s += max(1, j - bad_char[text[s + j]])
    return -1  # Підрядок не знайдено

# Алгоритм Кнута-Морріса-Пратта
def kmp_search(text, pattern):
    # Функція для створення префікс-функції
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    m, n = len(pattern), len(text)
    lps = compute_lps(pattern)
    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j  # Знайдено збіг
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1  # Підрядок не знайдено

# Алгоритм Рабіна-Карпа
def rabin_karp(text, pattern):
    d = 256  # Кількість символів в алфавіті
    q = 101  # Просте число для модуля
    m, n = len(pattern), len(text)
    h = pow(d, m-1) % q  # Для видалення першого символу
    p = 0  # Хеш шаблону
    t = 0  # Хеш тексту
    
    # Обчислюємо хеш для шаблону та першого вікна
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    
    for i in range(n - m + 1):
        if p == t:
            # Перевіряємо символи, якщо хеші збігаються
            if text[i:i+m] == pattern:
                return i  # Знайдено збіг
        if i < n - m:
            # Оновлюємо хеш для наступного вікна
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return -1  # Підрядок не знайдено

# Читання текстових файлів із спробою різних кодувань
def read_file(file_path):
    encodings = ['utf-8', 'cp1251', 'latin1', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            print(f"Не вдалося прочитати {file_path} з кодуванням {encoding}. Спроба іншого кодування...")
        except FileNotFoundError:
            print(f"Файл {file_path} не знайдено.")
            return None
    print(f"Не вдалося прочитати {file_path} з жодним кодуванням. Використовується синтетичний текст.")
    return None

# Спроба прочитати файли
text1 = read_file("article1.txt")
text2 = read_file("article2.txt")

# Запасний варіант: синтетичні тексти
if text1 is None:
    print("Використовується синтетичний текст для статті 1.")
    text1 = "Це приклад тексту для статті один. У цьому тексті ми розглядаємо алгоритми пошуку підрядка. Алгоритми важливі для обробки текстів." * 100
if text2 is None:
    print("Використовується синтетичний текст для статті 2.")
    text2 = "Стаття два присвячена аналізу ефективності алгоритмів. Ми тестуємо різні методи пошуку підрядків для порівняння їх швидкості." * 100

# Вибір підрядків
pattern_existing1 = "алгоритми пошуку"  # Наявний у тексті 1 (змінити, якщо потрібно)
pattern_non_existing1 = "вигаданий_підрядок"  # Вигаданий для тексту 1
pattern_existing2 = "ефективності алгоритмів"  # Наявний у тексті 2 (змінити, якщо потрібно)
pattern_non_existing2 = "несуществующий_подстрок"  # Вигаданий для тексту 2

# Функція для вимірювання часу
def measure_time(algorithm, text, pattern):
    setup_code = f'''
from __main__ import {algorithm.__name__}
text = """{text}"""
pattern = """{pattern}"""
'''
    stmt = f'{algorithm.__name__}(text, pattern)'
    return timeit.timeit(stmt=stmt, setup=setup_code, number=100)

# Вимірювання часу для всіх алгоритмів
results = {
    "article1": {"existing": {}, "non_existing": {}},
    "article2": {"existing": {}, "non_existing": {}}
}

algorithms = [boyer_moore, kmp_search, rabin_karp]

# Тестування для статті 1
for algo in algorithms:
    results["article1"]["existing"][algo.__name__] = measure_time(algo, text1, pattern_existing1)
    results["article1"]["non_existing"][algo.__name__] = measure_time(algo, text1, pattern_non_existing1)

# Тестування для статті 2
for algo in algorithms:
    results["article2"]["existing"][algo.__name__] = measure_time(algo, text2, pattern_existing2)
    results["article2"]["non_existing"][algo.__name__] = measure_time(algo, text2, pattern_non_existing2)

# Виведення результатів
print("Результати вимірювання часу (в секундах, для 100 запусків):")
print("\nСтаття 1 (наявний підрядок):")
for algo in algorithms:
    print(f"{algo.__name__}: {results['article1']['existing'][algo.__name__]:.6f} сек")
print("\nСтаття 1 (вигаданий підрядок):")
for algo in algorithms:
    print(f"{algo.__name__}: {results['article1']['non_existing'][algo.__name__]:.6f} сек")
print("\nСтаття 2 (наявний підрядок):")
for algo in algorithms:
    print(f"{algo.__name__}: {results['article2']['existing'][algo.__name__]:.6f} сек")
print("\nСтаття 2 (вигаданий підрядок):")
for algo in algorithms:
    print(f"{algo.__name__}: {results['article2']['non_existing'][algo.__name__]:.6f} сек")

# Визначення найшвидшого алгоритму
def find_fastest(results, text, pattern_type):
    min_time = float('inf')
    fastest_algo = None
    for algo, time in results[text][pattern_type].items():
        if time < min_time:
            min_time = time
            fastest_algo = algo
    return fastest_algo, min_time

# Аналіз для статті 1
fastest_article1_existing = find_fastest(results, "article1", "existing")
fastest_article1_non_existing = find_fastest(results, "article1", "non_existing")
print(f"\nНайшвидший для статті 1 (наявний): {fastest_article1_existing[0]} ({fastest_article1_existing[1]:.6f} сек)")
print(f"Найшвидший для статті 1 (вигаданий): {fastest_article1_non_existing[0]} ({fastest_article1_non_existing[1]:.6f} сек)")

# Аналіз для статті 2
fastest_article2_existing = find_fastest(results, "article2", "existing")
fastest_article2_non_existing = find_fastest(results, "article2", "non_existing")
print(f"Найшвидший для статті 2 (наявний): {fastest_article2_existing[0]} ({fastest_article2_existing[1]:.6f} сек)")
print(f"Найшвидший для статті 2 (вигаданий): {fastest_article2_non_existing[0]} ({fastest_article2_non_existing[1]:.6f} сек)")

# Загальний аналіз
total_times = defaultdict(float)
for algo in algorithms:
    total_times[algo.__name__] += results["article1"]["existing"][algo.__name__]
    total_times[algo.__name__] += results["article1"]["non_existing"][algo.__name__]
    total_times[algo.__name__] += results["article2"]["existing"][algo.__name__]
    total_times[algo.__name__] += results["article2"]["non_existing"][algo.__name__]

fastest_overall = min(total_times.items(), key=lambda x: x[1])
print(f"\nЗагалом найшвидший алгоритм: {fastest_overall[0]} (сумарний час: {fastest_overall[1]:.6f} сек)")