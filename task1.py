class HashTable:
    def __init__(self, size):
        # Ініціалізація хеш-таблиці з заданим розміром
        self.size = size
        # Створення списку порожніх списків для зберігання пар ключ-значення
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        # Обчислення хеш-індексу для ключа
        return hash(key) % self.size

    def insert(self, key, value):
        # Вставка пари ключ-значення у хеш-таблицю
        key_hash = self.hash_function(key)
        key_value = [key, value]

        # Якщо комірка порожня, створюємо новий список із парою
        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            # Якщо ключ уже існує, оновлюємо значення
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            # Якщо ключа немає, додаємо нову пару
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        # Отримання значення за ключем
        key_hash = self.hash_function(key)
        # Перевіряємо, чи комірка не порожня
        if self.table[key_hash] is not None:
            # Шукаємо ключ у списку пар
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        # Якщо ключ не знайдено, повертаємо None
        return None

    def delete(self, key):
        # Видалення пари ключ-значення за ключем
        key_hash = self.hash_function(key)
        # Перевіряємо, чи комірка не порожня
        if self.table[key_hash] is not None:
            # Шукаємо ключ у списку пар
            for i, pair in enumerate(self.table[key_hash]):
                if pair[0] == key:
                    # Видаляємо пару за індексом
                    self.table[key_hash].pop(i)
                    return True
        # Якщо ключ не знайдено, повертаємо False
        return False

# Тестування хеш-таблиці
if __name__ == "__main__":
    H = HashTable(5)
    # Вставляємо тестові дані
    H.insert("apple", 10)
    H.insert("orange", 20)
    H.insert("banana", 30)

    # Виводимо значення за ключами
    print(H.get("apple"))   # Виведе: 10
    print(H.get("orange"))  # Виведе: 20
    print(H.get("banana"))  # Виведе: 30

    # Тестуємо видалення
    print(H.delete("apple"))  # Виведе: True
    print(H.get("apple"))     # Виведе: None
    print(H.delete("grape"))  # Виведе: False