import os
import sys
from data_manager import load_resources, save_resources
from resource_classes import JobPosting, PsychologistContact, LegalAid, EducationProgram, SocialGroup
from utils import clear_screen, log_function_call, get_user_input

# Глобальні словники для зберігання ресурсів
# Використання словників для швидкого доступу за ID або іншими ключами
# Кожен ключ - це назва категорії, а значення - список об'єктів відповідного класу
resources = {
    "jobs": [],
    "psychologists": [],
    "legal_aids": [],
    "education": [],
    "social_groups": []
}

# Назви файлів для збереження даних
DATA_FILES = {
    "jobs": "data/jobs.json",
    "psychologists": "data/psychologists.json",
    "legal_aids": "data/legal_aids.json",
    "education": "data/education.json",
    "social_groups": "data/social_groups.json"
}

def initialize_data():
    """
    Ініціалізує дані програми, завантажуючи їх з JSON файлів.
    Демонструє роботу з файлами та обробку виключень (FileNotFoundError).
    """
    print("Завантаження даних...")
    for category, filename in DATA_FILES.items():
        try:
            # Завантажуємо дані для кожної категорії
            loaded_data = load_resources(filename, category)
            resources[category].extend(loaded_data)
            print(f"Дані для '{category}' завантажено успішно.")
        except FileNotFoundError:
            print(f"Файл '{filename}' не знайдено. Буде створено новий.")
            # Створюємо директорію, якщо її немає
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        except Exception as e:
            print(f"Помилка при завантаженні даних з '{filename}': {e}")
    print("Ініціалізація даних завершена.")

def save_all_data():
    """
    Зберігає всі поточні дані у відповідні JSON файли.
    """
    print("Збереження всіх даних...")
    for category, filename in DATA_FILES.items():
        try:
            save_resources(resources[category], filename)
            print(f"Дані для '{category}' збережено успішно.")
        except Exception as e:
            print(f"Помилка при збереженні даних у '{filename}': {e}")

@log_function_call # Застосування декоратора для логування виклику функції
def display_main_menu():
    """
    Відображає головне меню програми.
    """
    clear_screen()
    print("=" * 40)
    print("         НАВІГАТОР ПЕРЕХОДУ         ")
    print("  Допомога ветеранам та демобілізованим")
    print("=" * 40)
    print("\nОберіть категорію ресурсів:")
    print("1. Працевлаштування та Кар'єра")
    print("2. Психологічна Підтримка")
    print("3. Юридична Допомога")
    print("4. Освіта та Навчання")
    print("5. Соціальна Адаптація")
    print("6. Додати новий ресурс")
    print("0. Вийти з програми")
    print("-" * 40)

def display_resource_menu(category_name):
    """
    Відображає меню для конкретної категорії ресурсів.
    """
    clear_screen()
    print(f"--- {category_name} ---")
    print("1. Переглянути всі ресурси")
    print("2. Знайти ресурс (за ключовим словом)")
    print("3. Повернутися до головного меню")
    print("-" * 40)

def view_resources(category_key, title):
    """
    Переглядає та виводить список ресурсів для заданої категорії.
    Демонструє використання циклу for та умовних операторів.
    """
    clear_screen()
    print(f"--- Всі {title} ---")
    if not resources[category_key]:
        print(f"Наразі немає доступних {title.lower()}.")
        input("\nНатисніть Enter, щоб продовжити...")
        return

    for i, resource in enumerate(resources[category_key]):
        print(f"\n--- Ресурс #{i+1} ---")
        print(resource) # Виклик методу __str__ об'єкта
        print("-" * 20)
    input("\nНатисніть Enter, щоб продовжити...")

def search_resources(category_key, title):
    """
    Шукає ресурси за ключовим словом у заданій категорії.
    Демонструє використання генераторів списків та булевих операторів.
    """
    clear_screen()
    print(f"--- Пошук {title} ---")
    search_term = get_user_input("Введіть ключове слово для пошуку: ").lower()

    # Використання генератора списків для фільтрації
    found_resources = [
        resource for resource in resources[category_key]
        if search_term in str(resource).lower() # Пошук у строковому представленні об'єкта
    ]

    if not found_resources:
        print(f"Не знайдено {title.lower()} за запитом '{search_term}'.")
    else:
        print(f"\nЗнайдено {len(found_resources)} {title.lower()} за запитом '{search_term}':")
        for i, resource in enumerate(found_resources):
            print(f"\n--- Знайдений ресурс #{i+1} ---")
            print(resource)
            print("-" * 20)
    input("\nНатисніть Enter, щоб продовжити...")

def add_new_resource_menu():
    """
    Меню для додавання нового ресурсу.
    Демонструє використання словників для мапінгу вибору до функцій (функції як об'єкти першого класу).
    """
    clear_screen()
    print("--- Додати Новий Ресурс ---")
    print("1. Вакансію")
    print("2. Контакт психолога")
    print("3. Юридичну допомогу")
    print("4. Освітню програму")
    print("5. Соціальну групу")
    print("0. Повернутися до головного меню")
    print("-" * 40)

    add_choice = get_user_input("Ваш вибір: ", int)

    # Функції як об'єкти першого класу: мапінг вибору до відповідних функцій додавання
    add_functions = {
        1: add_job_posting,
        2: add_psychologist_contact,
        3: add_legal_aid,
        4: add_education_program,
        5: add_social_group,
    }

    if add_choice == 0:
        return
    elif add_choice in add_functions:
        add_functions[add_choice]()
    else:
        print("Невірний вибір. Спробуйте ще раз.")
        input("Натисніть Enter, щоб продовжити...")

def add_job_posting():
    """Додає нову вакансію."""
    clear_screen()
    print("--- Додати Нову Вакансію ---")
    title = get_user_input("Назва вакансії: ")
    company = get_user_input("Компанія: ")

    # Перевірка на дублікати
    for job in resources["jobs"]:
        if job.title.lower() == title.lower() and job.company.lower() == company.lower():
            print("\nПомилка: Вакансія з такою назвою та компанією вже існує.")
            input("Натисніть Enter, щоб продовжити...")
            return

    description = get_user_input("Опис вакансії: ")
    requirements_str = get_user_input("Вимоги (через кому, наприклад: досвід, освіта): ")
    # Використання множини для унікальних вимог
    requirements = set(req.strip() for req in requirements_str.split(',') if req.strip())
    contact = get_user_input("Контактна інформація: ")

    new_job = JobPosting(title, company, description, requirements, contact)
    resources["jobs"].append(new_job)
    print("Вакансію успішно додано!")
    input("Натисніть Enter, щоб продовжити...")
    save_all_data()

def add_psychologist_contact():
    """Додає новий контакт психолога."""
    clear_screen()
    print("--- Додати Контакт Психолога ---")
    name = get_user_input("Ім'я психолога: ")
    specialization = get_user_input("Спеціалізація: ")
    contact = get_user_input("Контактна інформація (телефон, email): ")
    # Змінено на звичайний рядок
    schedule = get_user_input("Графік роботи (наприклад, Пн-Пт 9:00-18:00): ")

    new_psychologist = PsychologistContact(name, specialization, contact, schedule)
    resources["psychologists"].append(new_psychologist)
    print("Контакт психолога успішно додано!")
    input("Натисніть Enter, щоб продовжити...")
    save_all_data()

def add_legal_aid():
    """Додає нову інформацію про юридичну допомогу."""
    clear_screen()
    print("--- Додати Юридичну Допомогу ---")
    organization = get_user_input("Назва організації: ")
    service_type = get_user_input("Тип послуги (наприклад, консультація, представництво): ")
    contact = get_user_input("Контактна інформація: ")
    description = get_user_input("Опис послуги: ")

    new_legal_aid = LegalAid(organization, service_type, contact, description)
    resources["legal_aids"].append(new_legal_aid)
    print("Юридичну допомогу успішно додано!")
    input("Натисніть Enter, щоб продовжити...")
    save_all_data()

def add_education_program():
    """Додає нову освітню програму."""
    clear_screen()
    print("--- Додати Освітню Програму ---")
    name = get_user_input("Назва програми: ")
    institution = get_user_input("Навчальний заклад: ")
    duration = get_user_input("Тривалість (наприклад, 6 місяців): ")
    description = get_user_input("Опис програми: ")
    contact = get_user_input("Контактна інформація: ")

    new_education = EducationProgram(name, institution, duration, description, contact)
    resources["education"].append(new_education)
    print("Освітню програму успішно додано!")
    input("Натисніть Enter, щоб продовжити...")
    save_all_data()

def add_social_group():
    """Додає нову соціальну групу."""
    clear_screen()
    print("--- Додати Соціальну Групу ---")
    name = get_user_input("Назва групи: ")
    focus_area = get_user_input("Напрямок діяльності (наприклад, підтримка, хобі): ")
    location = get_user_input("Місце проведення/онлайн: ")
    contact = get_user_input("Контактна інформація: ")
    description = get_user_input("Опис групи: ")

    new_social_group = SocialGroup(name, focus_area, location, contact, description)
    resources["social_groups"].append(new_social_group)
    print("Соціальну групу успішно додано!")
    input("Натисніть Enter, щоб продовжити...")
    save_all_data()

def handle_category_choice(category_key, title):
    """
    Обробляє вибір користувача в меню категорії.
    Використовує цикл while та булеві змінні для керування потоком.
    """
    category_active = True
    while category_active:
        display_resource_menu(title)
        choice = get_user_input("Ваш вибір: ", int)

        if choice == 1:
            view_resources(category_key, title)
        elif choice == 2:
            search_resources(category_key, title)
        elif choice == 3:
            category_active = False # Вихід з поточного циклу категорії
        else:
            print("Невірний вибір. Спробуйте ще раз.")
            input("Натисніть Enter, щоб продовжити...")

def main():
    """
    Головна функція програми.
    Містить основний цикл виконання та обробку вибору користувача.
    """
    initialize_data() # Ініціалізація даних при старті програми

    program_running = True # Булева змінна для керування головним циклом
    while program_running:
        display_main_menu()
        choice = get_user_input("Ваш вибір: ", int) # Обробка виключень для введення

        if choice == 1:
            handle_category_choice("jobs", "Вакансії")
        elif choice == 2:
            handle_category_choice("psychologists", "Психологи")
        elif choice == 3:
            handle_category_choice("legal_aids", "Юридична Допомога")
        elif choice == 4:
            handle_category_choice("education", "Освітні Програми")
        elif choice == 5:
            handle_category_choice("social_groups", "Соціальні Групи")
        elif choice == 6:
            add_new_resource_menu()
        elif choice == 0:
            clear_screen() # Очищення екрану перед виходом
            print("=" * 40)
            print("  Дякуємо за використання 'Навігатора Переходу'!")
            print("         До побачення!         ")
            print("=" * 40)
            program_running = False # Зміна булевої змінної для виходу з циклу
        else:
            print("Невірний вибір. Будь ласка, введіть число від 0 до 6.")
            input("Натисніть Enter, щоб продовжити...")

    save_all_data() # Збереження всіх даних при виході з програми
    sys.exit() # Вихід з програми

if __name__ == "__main__":
    main()