class VeteranResource:
    """
    Базовий клас для всіх ресурсів, що надаються ветеранам.
    Визначає загальні атрибути та методи.
    """
    def __init__(self, title, description, contact):
        # Атрибути екземпляра
        self.title = title
        self.description = description
        self.contact = contact

    def __str__(self):
        """
        Метод для зручного строкового представлення об'єкта.
        """
        return (f"Назва: {self.title}\n"
                f"Опис: {self.description}\n"
                f"Контакт: {self.contact}")

    def to_dict(self):
        """
        Перетворює об'єкт на словник для збереження у JSON.
        """
        return {
            "type": self.__class__.__name__, # Додаємо тип для десеріалізації
            "title": self.title,
            "description": self.description,
            "contact": self.contact
        }

class JobPosting(VeteranResource):
    """
    Клас для представлення вакансій.
    Наслідує від VeteranResource.
    Демонструє використання змінних (рядки, множини) та методів класу.
    """
    def __init__(self, title, company, description, requirements, contact):
        super().__init__(title, description, contact)
        self.company = company
        self.requirements = requirements # Множина для унікальних вимог

    def __str__(self):
        return (f"{super().__str__()}\n"
                f"Компанія: {self.company}\n"
                f"Вимоги: {', '.join(self.requirements)}")

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "company": self.company,
            "requirements": list(self.requirements) # Перетворюємо множину на список для JSON
        })
        return base_dict

class PsychologistContact(VeteranResource):
    """
    Клас для представлення контактів психологів.
    Наслідує від VeteranResource.
    Демонструє використання змінних (рядки).
    """
    def __init__(self, name, specialization, contact, schedule):
        # Використовуємо name як title і specialization як description для базового класу
        super().__init__(name, specialization, contact)
        self.schedule = schedule # Тепер це звичайний рядок

    def __str__(self):
        # Використовуємо self.title (що є name) та self.description (що є specialization)
        return (f"Ім'я: {self.title}\n"
                f"Спеціалізація: {self.description}\n"
                f"Контакт: {self.contact}\n"
                f"Графік: {self.schedule}") # Прямий доступ до рядка

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.title, # Відображаємо name з self.title для JSON
            "specialization": self.description, # Відображаємо specialization з self.description для JSON
            "schedule": self.schedule # Зберігаємо як рядок
        })
        return base_dict

class LegalAid(VeteranResource):
    """
    Клас для представлення інформації про юридичну допомогу.
    Наслідує від VeteranResource.
    """
    def __init__(self, organization_name, service_type, contact, description):
        # organization_name стає title для базового класу
        super().__init__(organization_name, description, contact)
        self.service_type = service_type

    def __str__(self):
        # self.title вже містить назву організації, тому не дублюємо її
        return (f"{super().__str__()}\n"
                f"Тип послуги: {self.service_type}")

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "service_type": self.service_type
        })
        return base_dict

class EducationProgram(VeteranResource):
    """
    Клас для представлення освітніх програм.
    Наслідує від VeteranResource.
    """
    def __init__(self, name, institution, duration, description, contact):
        super().__init__(name, description, contact)
        self.name = name
        self.institution = institution
        self.duration = duration

    def __str__(self):
        return (f"{super().__str__()}\n"
                f"Назва програми: {self.name}\n"
                f"Навчальний заклад: {self.institution}\n"
                f"Тривалість: {self.duration}")

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "institution": self.institution,
            "duration": self.duration
        })
        return base_dict

class SocialGroup(VeteranResource):
    """
    Клас для представлення соціальних груп та спільнот.
    Наслідує від VeteranResource.
    """
    def __init__(self, name, focus_area, location, contact, description):
        super().__init__(name, description, contact)
        self.name = name
        self.focus_area = focus_area
        self.location = location

    def __str__(self):
        return (f"{super().__str__()}\n"
                f"Назва групи: {self.name}\n"
                f"Напрямок: {self.focus_area}\n"
                f"Місце/Онлайн: {self.location}")

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "focus_area": self.focus_area,
            "location": self.location
        })
        return base_dict