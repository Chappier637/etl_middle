# etl_middle

## Запуск

### Инициализация airflow

Выполните следующую команду для инициализации Airflow:
   ```bash
   docker compose -f docker-compose.init.yaml -d up
   ```

### Инициализация всего сервиса
Выполните:
```bash
docker compose up
```
---

## Airflow Dags

### Вход в Airflow
Используйте следующие учетные данные для входа:
- **Логин:** `admin`
- **Пароль:** `admin`

### Описание доступных DAGs

#### 1. **`initial_migration`**
- Запускается **один раз** для инициализации.
- Функциональность:
  - Создание таблиц в Postgres.

#### 2. **`mongo_to_postgress`**
- Периодичность: **ежедневно**.
- Функциональность:
- Импорт таблиц из Mongo в PG

#### 3. **`data_marts`**
- Функциональность:
    Собирает витрины в PG на данных, импортированных из Mongo
- **Создание витрин**:
  - SQL-скрипты для сборки лежат в `code/dags/sql/marts`
---





