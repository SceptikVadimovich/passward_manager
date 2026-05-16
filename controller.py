import random
import string
from typing import List, Optional
from model import PasswordRecord, PasswordStorage
from view import ConsoleView


class PasswordGenerator:
    """Класс для генерации паролей."""
    
    @staticmethod
    def generate(length: int = 12, use_upper: bool = True, use_lower: bool = True,
                 use_digits: bool = True, use_symbols: bool = True) -> str:
        """
        Генерирует случайный пароль с заданными параметрами.
        """
        chars = ""
        if use_upper:
            chars += string.ascii_uppercase
        if use_lower:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            # Если не выбрано ни одного набора, используем по умолчанию
            chars = string.ascii_letters + string.digits
        
        # Гарантируем, что пароль содержит хотя бы один символ из каждого выбранного набора
        password_chars = []
        if use_upper:
            password_chars.append(random.choice(string.ascii_uppercase))
        if use_lower:
            password_chars.append(random.choice(string.ascii_lowercase))
        if use_digits:
            password_chars.append(random.choice(string.digits))
        if use_symbols:
            password_chars.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Заполняем остальную длину случайными символами
        remaining_length = length - len(password_chars)
        if remaining_length > 0:
            password_chars.extend(random.choices(chars, k=remaining_length))
        
        # Перемешиваем
        random.shuffle(password_chars)
        
        return ''.join(password_chars)


class PasswordController:
    """Контроллер для управления паролями."""
    
    def __init__(self):
        self._storage = PasswordStorage()
        self._view = ConsoleView()
        self._generator = PasswordGenerator()
        self._records: List[PasswordRecord] = []
        self._load_data()
    
    def _load_data(self) -> None:
        """Загружает данные из хранилища."""
        self._records = self._storage.load()
    
    def _save_data(self) -> None:
        """Сохраняет данные в хранилище."""
        self._storage.save(self._records)
    
    def _find_by_service(self, service: str) -> Optional[PasswordRecord]:
        """Находит запись по названию сервиса."""
        for record in self._records:
            if record.service.lower() == service.lower():
                return record
        return None
    
    def _validate_input(self, service: str, username: str, password: str) -> bool:
        """Проверяет корректность ввода."""
        if not service or not service.strip():
            self._view.show_message("Название сервиса не может быть пустым", is_error=True)
            return False
        if not username or not username.strip():
            self._view.show_message("Имя пользователя не может быть пустым", is_error=True)
            return False
        if not password or not password.strip():
            self._view.show_message("Пароль не может быть пустым", is_error=True)
            return False
        return True
    
    def add_record(self) -> None:
        """Добавляет новую запись пароля."""
        print("\n--- Добавление нового пароля ---")
        
        service = self._view.get_input("Название сервиса: ")
        username = self._view.get_input("Имя пользователя/логин: ")
        password = self._view.get_input("Пароль: ")
        
        if not self._validate_input(service, username, password):
            return
        
        # Проверка на дубликат
        if self._find_by_service(service):
            self._view.show_message(f"Запись для сервиса '{service}' уже существует", is_error=True)
            return
        
        try:
            record = PasswordRecord(service, username, password)
            self._records.append(record)
            self._save_data()
            self._view.show_message(f"Пароль для '{service}' успешно сохранён!")
        except ValueError as e:
            self._view.show_message(str(e), is_error=True)
    
    def view_all_records(self) -> None:
        """Показывает все записи."""
        self._view.show_all_records(self._records)
        
        if self._records:
            print("\nДля просмотра деталей введите номер записи или Enter для выхода:")
            try:
                choice = self._view.get_input("> ")
                if choice and choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(self._records):
                        self._view.show_password_record(self._records[idx], idx)
                    else:
                        self._view.show_message("Неверный номер", is_error=True)
            except Exception:
                pass
    
    def find_record(self) -> None:
        """Ищет запись по названию сервиса."""
        service = self._view.get_search_term()
        if not service:
            return
        
        record = self._find_by_service(service)
        if record:
            self._view.show_password_record(record)
        else:
            self._view.show_message(f"Сервис '{service}' не найден", is_error=True)
    
    def delete_record(self) -> None:
        """Удаляет запись пароля."""
        service = self._view.get_service_to_delete()
        if not service:
            return
        
        record = self._find_by_service(service)
        if record:
            self._view.show_password_record(record)
            confirm = self._view.get_input("Удалить эту запись? (y/n): ")
            if confirm.lower() == 'y':
                self._records.remove(record)
                self._save_data()
                self._view.show_message(f"Запись для '{service}' удалена")
            else:
                self._view.show_message("Удаление отменено")
        else:
            self._view.show_message(f"Сервис '{service}' не найден", is_error=True)
    
    def generate_and_save_password(self) -> None:
        """Генерирует пароль и предлагает сохранить."""
        length, use_upper, use_lower, use_digits, use_symbols = self._view.get_password_generation_settings()
        
        password = self._generator.generate(length, use_upper, use_lower, use_digits, use_symbols)
        self._view.show_generated_password(password)
        
        save = self._view.get_input("\nСохранить этот пароль для сервиса? (y/n): ")
        if save.lower() == 'y':
            service = self._view.get_input("Название сервиса: ")
            username = self._view.get_input("Имя пользователя/логин: ")
            
            if self._validate_input(service, username, password):
                if self._find_by_service(service):
                    self._view.show_message(f"Запись для сервиса '{service}' уже существует", is_error=True)
                    return
                
                try:
                    record = PasswordRecord(service, username, password)
                    self._records.append(record)
                    self._save_data()
                    self._view.show_message(f"Пароль для '{service}' успешно сохранён!")
                except ValueError as e:
                    self._view.show_message(str(e), is_error=True)
    
    def run(self) -> None:
        """Запускает главный цикл приложения."""
        self._view.show_message("Добро пожаловать в Password Manager!")
        
        while True:
            self._view.show_menu()
            choice = self._view.get_input("Выберите действие (1-6): ")
            
            if choice == '1':
                self.add_record()
            elif choice == '2':
                self.view_all_records()
            elif choice == '3':
                self.find_record()
            elif choice == '4':
                self.delete_record()
            elif choice == '5':
                self.generate_and_save_password()
            elif choice == '6':
                self._view.show_message("До свидания!")
                break
            else:
                self._view.show_message("Неверный выбор. Попробуйте снова.", is_error=True)
