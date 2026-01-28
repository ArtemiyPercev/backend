# 📝 Шпаргалка: Полный цикл преобразования данных в FastAPI + SQLAlchemy

## 🎯 Главное правило: ПОЛНЫЙ ЦИКЛ ДАННЫХ

```
JSON → Pydantic → Словарь → SQL запрос → БД → ORM → Pydantic → JSON → HTTP ответ
```

---

## 🔄 Детальный разбор каждого шага

### 1️⃣ **JSON → Pydantic schema** (валидация входящих данных)

**Что происходит:**
- Пользователь отправляет HTTP запрос с JSON в теле
- FastAPI автоматически валидирует JSON и создает Pydantic объект

**Пример:**
```python
# Пользователь отправляет:
{"room_id": 5, "date_from": "2024-01-01", "date_to": "2024-01-05"}

# FastAPI создает:
data_booking = BookingAddRequest(room_id=5, date_from=..., date_to=...)
```

**Где в коде:**
```python
# src/api/bookings.py, строка 25
async def add_booking(
    data_booking: BookingAddRequest,  # ← FastAPI автоматически делает JSON → Pydantic
    ...
):
```

**Зачем:** Валидация данных (проверка типов, обязательных полей)

---

### 2️⃣ **Pydantic schema → Словарь** (для работы с SQLAlchemy)

**Что происходит:**
- Pydantic объект превращается в словарь через `model_dump()`

**Пример:**
```python
# Pydantic:
BookingAdd(user_id=42, room_id=5, price=5000, ...)

# Словарь:
{"user_id": 42, "room_id": 5, "price": 5000, ...}
```

**Где в коде:**
```python
# src/api/bookings.py, строка 39
**data_booking.model_dump()  # ← Pydantic → словарь

# Или в репозитории:
# src/repositories/base.py, строка 30
data.model_dump()  # ← Pydantic → словарь
```

**Зачем:** SQLAlchemy работает со словарями, а не с Pydantic объектами напрямую

---

### 3️⃣ **Словарь → SQL запрос SQLAlchemy** (построение запроса)

**Что происходит:**
- SQLAlchemy берет словарь и строит SQL запрос INSERT

**Пример:**
```python
# Словарь:
{"user_id": 42, "room_id": 5, "price": 5000, ...}

# SQL запрос:
INSERT INTO bookings (user_id, room_id, price, date_from, date_to) 
VALUES (42, 5, 5000, '2024-01-01', '2024-01-05')
RETURNING *
```

**Где в коде:**
```python
# src/repositories/base.py, строка 30
add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
# ↑ SQLAlchemy строит SQL запрос из словаря
```

**Зачем:** SQLAlchemy - это ORM, он переводит Python код в SQL запросы

---

### 4️⃣ **SQL запрос → База данных** (выполнение)

**Что происходит:**
- SQL запрос отправляется в PostgreSQL
- База данных выполняет INSERT и создает запись

**Пример:**
```python
# SQL запрос уходит в БД:
INSERT INTO bookings (...) VALUES (...)

# БД создает запись:
id=123, user_id=42, room_id=5, price=5000, created_at='2024-01-01 10:30:00'
```

**Где в коде:**
```python
# src/repositories/base.py, строка 31
result = await self.session.execute(add_stmt)  # ← SQL запрос уходит в БД
```

**Зачем:** Это реальное сохранение данных в базе данных

---

### 5️⃣ **База данных → ORM model** (создание модели из результата)

**Что происходит:**
- БД возвращает созданную запись (благодаря RETURNING *)
- SQLAlchemy преобразует данные из БД в ORM модель

**Пример:**
```python
# БД возвращает данные:
id=123, user_id=42, room_id=5, price=5000, created_at=datetime(...)

# SQLAlchemy создает ORM модель:
BookingsOrm(id=123, user_id=42, room_id=5, price=5000, created_at=...)
```

**Где в коде:**
```python
# src/repositories/base.py, строка 32
return result.scalars().one()  # ← БД вернула данные, SQLAlchemy создал ORM
```

**Зачем:** ORM модель - это Python объект, с которым удобно работать в коде

---

### 6️⃣ **ORM model → Pydantic schema** (для ответа)

**Что происходит:**
- ORM модель преобразуется в Pydantic схему через `model_validate()`

**Пример:**
```python
# ORM модель:
BookingsOrm(id=123, user_id=42, room_id=5, ...)

# Pydantic схема:
Booking(id=123, user_id=42, room_id=5, created_at=...)
```

**Где в коде:**
```python
# src/api/bookings.py, строка 45
booking = Booking.model_validate(result, from_attributes=True)  # ← ORM → Pydantic
```

**Зачем:** 
- Контроль полей (возвращаем только нужные)
- Безопасность (не возвращаем внутренние ORM атрибуты)
- Легкая сериализация в JSON

---

### 7️⃣ **Pydantic schema → JSON** (сериализация)

**Что происходит:**
- FastAPI автоматически сериализует Pydantic объект в JSON

**Пример:**
```python
# Pydantic:
Booking(id=123, user_id=42, room_id=5, created_at=datetime(...))

# JSON:
{"id": 123, "user_id": 42, "room_id": 5, "created_at": "2024-01-01T10:30:00"}
```

**Где в коде:**
```python
# src/api/bookings.py, строка 47
return {"Status": "OK", "data": booking}  # ← FastAPI автоматически делает Pydantic → JSON
```

**Зачем:** JSON - это стандартный формат для HTTP ответов

---

### 8️⃣ **JSON → HTTP ответ** (отправка пользователю)

**Что происходит:**
- FastAPI отправляет HTTP ответ с JSON в теле

**Пример:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "Status": "OK",
    "data": {
        "id": 123,
        "user_id": 42,
        "room_id": 5,
        "price": 5000,
        "date_from": "2024-01-01",
        "date_to": "2024-01-05",
        "created_at": "2024-01-01T10:30:00"
    }
}
```

**Где в коде:**
```python
# src/api/bookings.py, строка 47
return {"Status": "OK", "data": booking}  # ← FastAPI автоматически отправляет HTTP ответ
```

**Зачем:** Это финальный ответ пользователю

---

## 🎓 Как это запомнить?

### Метод 1: Запомни последовательность

```
JSON → Pydantic → Словарь → SQL → БД → ORM → Pydantic → JSON → HTTP
```

**Мнемоника:** "JSON превращается в Pydantic, потом в словарь, отправляется SQL запросом в БД, возвращается как ORM, превращается обратно в Pydantic, потом в JSON и отправляется HTTP ответом"

### Метод 2: Раздели на две части

**Входящий поток (от пользователя к БД):**
```
JSON → Pydantic → Словарь → SQL → БД
```
*"Пользователь отправляет JSON, мы валидируем (Pydantic), превращаем в словарь, строим SQL запрос и сохраняем в БД"*

**Исходящий поток (от БД к пользователю):**
```
БД → ORM → Pydantic → JSON → HTTP
```
*"БД возвращает данные, SQLAlchemy создает ORM, мы превращаем в Pydantic для контроля, сериализуем в JSON и отправляем HTTP ответом"*

### Метод 3: Запомни ключевые методы

- **Входящие:** `model_dump()` - Pydantic → словарь
- **Исходящие:** `model_validate()` - ORM → Pydantic

---

## 📋 Быстрая шпаргалка по методам

| Преобразование | Метод | Где используется |
|----------------|-------|------------------|
| Pydantic → Словарь | `model_dump()` | Перед отправкой в БД |
| ORM → Pydantic | `model_validate(orm, from_attributes=True)` | После получения из БД |
| Словарь → SQL | `insert(Model).values(**словарь)` | В репозитории |
| SQL → ORM | `result.scalars().one()` | После execute() |

---

## 🔍 Пример из реального кода

```python
# src/api/bookings.py

@router.post("/bookings")
async def add_booking(
    data_booking: BookingAddRequest,  # 1. JSON → Pydantic (автоматически)
    db: DBdep,
    user_id: UserIdDep,
):
    # Создаем полную схему
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_data.price,
        **data_booking.model_dump()  # 2. Pydantic → Словарь
    )
    
    # Отправляем в репозиторий
    result = await db.bookings.add(_booking_data)
    # ↓ Внутри репозитория:
    #   3. Словарь → SQL запрос (insert().values(**словарь))
    #   4. SQL запрос → БД (session.execute())
    #   5. БД → ORM (result.scalars().one())
    
    await db.commit()
    
    # 6. ORM → Pydantic
    booking = Booking.model_validate(result, from_attributes=True)
    
    # 7-8. Pydantic → JSON → HTTP ответ (автоматически)
    return {"Status": "OK", "data": booking}
```

---

## 💡 Почему так много преобразований?

1. **JSON → Pydantic:** Валидация входящих данных (безопасность)
2. **Pydantic → Словарь:** SQLAlchemy работает со словарями
3. **Словарь → SQL:** SQLAlchemy - это ORM, переводит Python в SQL
4. **SQL → БД:** Реальное сохранение данных
5. **БД → ORM:** Удобная работа с данными в Python
6. **ORM → Pydantic:** Контроль полей и безопасность ответа
7. **Pydantic → JSON:** Стандартный формат для HTTP
8. **JSON → HTTP:** Отправка ответа пользователю

**Каждое преобразование решает свою задачу!**

---

## 🎯 Главное запомнить

1. **Входящий поток:** JSON → Pydantic → Словарь → SQL → БД
2. **Исходящий поток:** БД → ORM → Pydantic → JSON → HTTP
3. **Ключевые методы:** `model_dump()` (входящие) и `model_validate()` (исходящие)
4. **FastAPI делает автоматически:** JSON ↔ Pydantic, Pydantic → JSON → HTTP


   Входящие: JSON → Pydantic → Словарь → SQL → БД
   Исходящие: БД → ORM → Pydantic → JSON → HTTP
---

## 📚 Дополнительные материалы

- **BaseRepository.add()** - где происходит словарь → SQL → БД → ORM
- **Booking.model_validate()** - где происходит ORM → Pydantic
- **FastAPI автоматически** - JSON ↔ Pydantic и Pydantic → JSON → HTTP

---

**Создано:** 2024  
**Для проекта:** BackendCourse  
**Цель:** Шпаргалка по циклу преобразования данных
