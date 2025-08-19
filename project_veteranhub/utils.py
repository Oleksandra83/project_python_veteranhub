import os

def clear_screen():
    """
    Очищає екран консолі.
    Використовує модуль os.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def log_function_call(func):
    """
    Декоратор, який логує виклик функції та її назву.
    Демонструє створення та використання декораторів.
    """
    def wrapper(*args, **kwargs):
        print(f"\n[ЛОГ] Викликається функція: '{func.__name__}'")
        result = func(*args, **kwargs)
        print(f"[ЛОГ] Функція '{func.__name__}' завершила роботу.")
        return result
    return wrapper

def get_user_input(prompt, type_converter=str):
    """
    Отримує введення від користувача, забезпечуючи обробку виключень.
    Демонструє використання try-except для валідації введення.
    Функція type_converter є об'єктом першого класу.
    """
    while True:
        try:
            user_input = input(prompt)
            # Спроба конвертувати введення у потрібний тип
            return type_converter(user_input)
        except ValueError:
            print(f"Невірний формат введення. Будь ласка, введіть значення типу {type_converter.__name__}.")
        except Exception as e:
            print(f"Виникла невідома помилка: {e}")