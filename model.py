import json
from datetime import datetime
from typing import List, Optional


class PasswordRecord:
    """Модель данных для записи пароля."""
    
    def __init__(self, service: str, username: str, password: str, created_at: Optional[str] = None):
        self._service = service
        self._username = username
        self._password = password
        self._created_at = created_at or datetime.now().isoformat()
    
    # Геттеры
    @property
    def service(self) -> str:
        return self._service
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def created_at(self) -> str:
        return self._created_at
    
    # Сеттеры с валидацией
    @service.setter
    def service(self, value: str):
        if not value or not value.strip():
            raise ValueError("Service name cannot be empty")
        self._service = value.strip()
    
    @username.setter
    def username(self, value: str):
        if not value or not value.strip():
            raise ValueError("Username cannot be empty")
        self._username = value.strip()
    
    @password.setter
    def password(self, value: str):
        if not value or not value.strip():
            raise ValueError("Password cannot be empty")
        self._password = value
    
    def to_dict(self) -> dict:
        """Преобразует запись в словарь для JSON."""
        return {
            "service": self._service,
            "username": self._username,
            "password": self._password,
            "created_at": self._created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PasswordRecord':
        """Создаёт запись из словаря."""
        return cls(
            service=data["service"],
            username=data["username"],
            password=data["password"],
            created_at=data.get("created_at")
        )
    
    def __str__(self) -> str:
        return f"{self._service} | {self._username} | {self._created_at[:10]}"


class PasswordStorage:
    """Класс для работы с JSON-хранилищем."""
    
    def __init__(self, filename: str = "data.json"):
        self._filename = filename
    
    def save(self, records: List[PasswordRecord]) -> None:
        """Сохраняет список записей в JSON файл."""
        data = [record.to_dict() for record in records]
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self) -> List[PasswordRecord]:
        """Загружает список записей из JSON файла."""
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [PasswordRecord.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
