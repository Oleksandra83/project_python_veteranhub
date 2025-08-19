# =========================
# ПРОЄКТ: Система підтримки ветеранів
# Автор: Andrushchenko Oleksandra
# Опис: Керування даними про ветеранів війни та демобілізованих осіб
# Використано: змінні, типи, input, цикли, списки, словники, функції, модулі, винятки, файли, класи, декоратори
# =========================

import json
import os
from typing import Callable

# === Глобальні змінні ===
DATA_FILE = "veterans.json"

# === Декоратор для логування ===
def log_action(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print(f"[INFO] Виконується: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# === Клас Veteran ===
class Veteran:
    def __init__(self, veteran_id: int, name: str, age: int, status: str, region: str):
        self.veteran_id = veteran_id
        self.name = name
        self.age = age
        self.status = status  # "демобілізований" / "учасник війни" / "УБД" / "інвалід внаслідок війни" / "член сім'ї загиблого Захисника України"
        self.region = region

    def to_dict(self) -> dict:
        return self.__dict__

    @staticmethod
    def from_dict(data: dict):
        return Veteran(**data)

# === Робота з JSON ===
@log_action
def load_veterans() -> list:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return [Veteran.from_dict(d) for d in json.load(f)]

@log_action
def save_veterans(veterans: list):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([v.to_dict() for v in veterans], f, indent=2, ensure_ascii=False)

# === CRUD операції ===
@log_action
def add_veteran(veterans: list):
    try:
        veteran_id = max([v.veteran_id for v in veterans], default=0) + 1
        name = input("Ім'я та прізвище: ")
        age = int(input("Вік: "))
        status = input("Статус (демобілізований/учасник війни/УБД/інвалід внаслідок війни/член сім'ї загиблого Захисника України): ")
        region = input("Регіон проживання: ")
        veteran = Veteran(veteran_id, name, age, status, region)
        veterans.append(veteran)
        print("✔ Додано успішно!")
    except ValueError:
        print("❌ Помилка введення. Спробуйте ще раз.")

@log_action
def list_veterans(veterans: list):
    for v in veterans:
        print(f"ID: {v.veteran_id} | {v.name}, {v.age} р. | {v.status} | {v.region}")

@log_action
def find_by_region(veterans: list):
    region = input("Введіть регіон: ").strip().lower()
    found = [v for v in veterans if v.region.lower() == region]
    _display_found(found)

@log_action
def find_by_name(veterans: list):
    name = input("Введіть ім'я або прізвище: ").strip().lower()
    found = [v for v in veterans if name in v.name.lower()]
    _display_found(found)

@log_action
def find_by_status(veterans: list):
    status = input("Введіть статус (демобілізований/учасник війни/УБД/інвалід внаслідок війни/член сім'ї загиблого Захисника України): ").strip().lower()
    found = [v for v in veterans if v.status.lower() == status]
    _display_found(found)

@log_action
def filter_by_age(veterans: list):
    try:
        min_age = int(input("Мінімальний вік: "))
        max_age = int(input("Максимальний вік: "))
        found = [v for v in veterans if min_age <= v.age <= max_age]
        _display_found(found)
    except ValueError:
        print("❌ Вік має бути числом.")

def _display_found(found: list):
    if not found:
        print("❌ Не знайдено.")
    else:
        for v in found:
            print(f"{v.veteran_id}: {v.name}, {v.age} р. | {v.status} | {v.region}")

@log_action
def delete_veteran(veterans: list):
    try:
        id_to_delete = int(input("Введіть ID для видалення: "))
        updated = [v for v in veterans if v.veteran_id != id_to_delete]
        if len(updated) < len(veterans):
            veterans.clear()
            veterans.extend(updated)
            print("✔ Видалено.")
        else:
            print("❌ Не знайдено ID.")
    except ValueError:
        print("❌ Некоректне значення.")

@log_action
def edit_veteran(veterans: list):
    try:
        id_to_edit = int(input("Введіть ID для редагування: "))
        for v in veterans:
            if v.veteran_id == id_to_edit:
                print("Залиште поле порожнім, щоб не змінювати значення")
                name = input(f"Ім'я та прізвище ({v.name}): ").strip() or v.name
                age_input = input(f"Вік ({v.age}): ").strip()
                age = int(age_input) if age_input else v.age
                status = input(f"Статус ({v.status}): ").strip() or v.status
                region = input(f"Регіон ({v.region}): ").strip() or v.region
                v.name, v.age, v.status, v.region = name, age, status, region
                print("✔ Запис оновлено.")
                return
        print("❌ Не знайдено ID.")
    except ValueError:
        print("❌ Некоректне значення.")

# === Меню ===
def menu():
    print("""
--- МЕНЮ ---
1. Додати ветерана
2. Показати всіх
3. Пошук за регіоном
4. Видалити за ID
5. Пошук за ім'ям
6. Пошук за статусом
7. Фільтр за віком
8. Редагувати запис
0. Вихід
""")

# === Головна функція ===
def main():
    veterans = load_veterans()
    while True:
        menu()
        choice = input("Оберіть дію: ").strip()
        if choice == "1":
            add_veteran(veterans)
        elif choice == "2":
            list_veterans(veterans)
        elif choice == "3":
            find_by_region(veterans)
        elif choice == "4":
            delete_veteran(veterans)
        elif choice == "5":
            find_by_name(veterans)
        elif choice == "6":
            find_by_status(veterans)
        elif choice == "7":
            filter_by_age(veterans)
        elif choice == "8":
            edit_veteran(veterans)
        elif choice == "0":
            save_veterans(veterans)
            print("Збережено. До зустрічі!")
            break
        else:
            print("❌ Невірна команда")

if __name__ == "__main__":
    main()
