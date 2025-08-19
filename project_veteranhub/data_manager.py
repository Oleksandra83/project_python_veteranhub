import json
import os
from resource_classes import JobPosting, PsychologistContact, LegalAid, EducationProgram, SocialGroup

# Словник для мапінгу строкових назв класів до самих класів
CLASS_MAP = {
    "JobPosting": JobPosting,
    "PsychologistContact": PsychologistContact,
    "LegalAid": LegalAid,
    "EducationProgram": EducationProgram,
    "SocialGroup": SocialGroup
}

def load_resources(filepath, category_name):
    """
    Завантажує ресурси з JSON файлу.
    Використовує менеджер контексту 'with open'.
    Обробляє виключення FileNotFoundError.
    """
    resources_list = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                # Використання інформації про тип для коректної десеріалізації
                item_type = item.get("type")
                if item_type and item_type in CLASS_MAP:
                    # Динамічне створення об'єкта класу з даних словника
                    if item_type == "JobPosting":
                        resources_list.append(JobPosting(
                            item['title'], item['company'], item['description'],
                            set(item['requirements']), item['contact']
                        ))
                    elif item_type == "PsychologistContact":
                        resources_list.append(PsychologistContact(
                            item['name'], item['specialization'], item['contact'],
                            item['schedule'] # Завантажуємо як рядок
                        ))
                    elif item_type == "LegalAid":
                        resources_list.append(LegalAid(
                            item['title'], # Тепер title - це назва організації
                            item['service_type'], item['contact'],
                            item['description']
                        ))
                    elif item_type == "EducationProgram":
                        resources_list.append(EducationProgram(
                            item['name'], item['institution'], item['duration'],
                            item['description'], item['contact']
                        ))
                    elif item_type == "SocialGroup":
                        resources_list.append(SocialGroup(
                            item['name'], item['focus_area'], item['location'],
                            item['contact'], item['description']
                        ))
                    else:
                        print(f"Попередження: Невідомий тип ресурсу '{item_type}' у файлі {filepath}")
                else:
                    print(f"Попередження: Відсутній або невідомий тип ресурсу у записі: {item}")
    except FileNotFoundError:
        # Це очікувана ситуація при першому запуску, тому просто повертаємо порожній список
        return []
    except json.JSONDecodeError as e:
        print(f"Помилка декодування JSON у файлі {filepath}: {e}")
        return []
    except Exception as e:
        print(f"Невідома помилка при завантаженні файлу {filepath}: {e}")
        return []
    return resources_list

def save_resources(resources_list, filepath):
    """
    Зберігає список ресурсів у JSON файл.
    Використовує менеджер контексту 'with open'.
    """
    # Перетворюємо список об'єктів на список словників
    data_to_save = [resource.to_dict() for resource in resources_list]
    try:
        # Створюємо директорію, якщо вона не існує
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            # ensure_ascii=False дозволяє зберігати українські символи
            # indent=4 робить файл читабельним
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Помилка при збереженні даних у файл {filepath}: {e}")