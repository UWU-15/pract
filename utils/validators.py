import re

def validate_email(email: str) -> bool:
    """
    Проверяет корректность формата email адреса.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """
    Проверяет минимальные требования к паролю.
    """
    return len(password) >= 6

def validate_username(username: str) -> bool:
    """
    Проверяет корректность имени пользователя.
    """
    return len(username) >= 3 and re.match(r'^[a-zA-Z0-9_]+$', username) is not None

def validate_user_registration(username: str, email: str, password: str, confirm_password: str) -> list:
    """
    Комплексная валидация данных при регистрации пользователя.
    """
    errors = []
    
    # Валидация имени пользователя
    if not validate_username(username):
        errors.append("Username must be at least 3 characters and contain only letters, numbers, and underscores")
    
    # Валидация email
    if not email:
        errors.append("Email is required")
    elif not validate_email(email):
        errors.append("Invalid email format")
    
    # Валидация пароля
    if not validate_password(password):
        errors.append("Password must be at least 6 characters")
    
    # Проверка совпадения паролей
    if password != confirm_password:
        errors.append("Passwords don't match")
    
    return errors