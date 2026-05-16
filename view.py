from typing import List, Optional
from model import PasswordRecord


class ConsoleView:
    """Представление для консольного интерфейса."""
    
    @staticmethod
    def show_menu() -> None:
        """Отображает главное меню."""
        print("\n" + "=" * 50)
        print("         PASSWORD MANAGER")
        print("=" * 50)
        print("1. Добавить пароль")
        print("2. Просмотреть все пароли")
        print("3. Найти пароль по сервису")
        print("4. Удалить пароль")
        print("5. Сгенерировать пароль")
        print("6. Выйти")
        print("-" * 50)
    
    @staticmethod
    def get_input(prompt: str) -> str:
        """Получает ввод от пользователя."""
        return input(prompt).strip()
    
    @staticmethod
    def show_message(message: str, is_error: bool = False) -> None:
        """Показывает сообщение пользователю."""
        prefix = "❌ " if is_error else "✅ "
        print(prefix + message)
    
    @staticmethod
    def show_password_record(record: PasswordRecord, index: Optional[int] = None) -> None:
        """Показывает одну запись пароля."""
        prefix = f"{index + 1}. " if index is not None else ""
        print(f"\n{prefix}Сервис: {record.service}")
        print(f"   Логин: {record.username}")
        print(f"   Пароль: {record.password}")
        print(f"   Создан: {record.created_at}")
    
    @staticmethod
    def show_all_records(records: List[PasswordRecord]) -> None:
        """Показывает все записи паролей."""
        if not records:
            ConsoleView.show_message("Нет сохранённых паролей")
            return
        
        print("\n" + "=" * 50)
        print("СПИСОК ПАРОЛЕЙ")
        print("=" * 50)
        for i, record in enumerate(records):
            print(f"{i + 1}. {record.service} - {record.username}")
        print("-" * 50)
    
    @staticmethod
    def get_password_generation_settings() -> tuple:
        """Запрашивает настройки для генерации пароля."""
        print("\n--- Настройки генерации пароля ---")
        
        while True:
            try:
                length = int(ConsoleView.get_input("Длина пароля (8-50): "))
                if 8 <= length <= 50:
                    break
                ConsoleView.show_message("Длина должна быть от 8 до 50", is_error=True)
            except ValueError:
                ConsoleView.show_message("Введите число", is_error=True)
        
        use_upper = ConsoleView.get_input("Использовать заглавные буквы? (y/n): ").lower() == 'y'
        use_lower = ConsoleView.get_input("Использовать строчные буквы? (y/n): ").lower() == 'y'
        use_digits = ConsoleView.get_input("Использовать цифры? (y/n): ").lower() == 'y'
        use_symbols = ConsoleView.get_input("Использовать символы? (y/n): ").lower() == 'y'
        
        return length, use_upper, use_lower, use_digits, use_symbols
    
    @staticmethod
    def show_generated_password(password: str) -> None:
        """Показывает сгенерированный пароль."""
        print(f"\n🔑 Сгенерированный пароль: {password}")
    
    @staticmethod
    def get_search_term() -> str:
        """Запрашивает термин для поиска."""
        return ConsoleView.get_input("Введите название сервиса для поиска: ")
    
    @staticmethod
    def get_service_to_delete() -> str:
        """Запрашивает сервис для удаления."""
        return ConsoleView.get_input("Введите название сервиса для удаления: ")
