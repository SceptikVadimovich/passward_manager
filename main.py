#!/usr/bin/env python3
"""
Password Manager - Консольное приложение для управления паролями
"""

from controller import PasswordController


def main():
    """Точка входа в приложение."""
    app = PasswordController()
    app.run()


if __name__ == "__main__":
    main()
