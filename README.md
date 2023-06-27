# Серверная часть диплома <br> "Разработка сайта для тайм-менеджмента и оптимизации работы"
> Эндпоинты, обращение к базе данных PostgreSQL, доступ к которой реализован через Docker <br>
> **/docs** - автособираемая документация

##### Запуск в консоли:

    python -m uvicorn app.main:app --host localhost --port 8000 --reload

### АВТОРИЗАЦИЯ

<details><summary>Создать пользователя - регистрация </summary>
<br>

     /api/auth/register
         
  > Метод запроса  - POST

Добавляет пользователя в базу, если логин уникальный, пароль больше 8 символов и остальные поля непустые
</details>
<details><summary>Авторизация пользователя - логин </summary>
<br>
    
    /api/auth/login
        
  > Метод запроса  - POST

Авторизирует аккаунт, возвращает аксес токен, если верные логин с паролем; пишет токены(access и refresh) и logged_in в куки, если на фронте **withCredentials:true**
</details>
<details><summary>Обновить токены</summary>
<br>
  
    /api/auth/refresh
    
  > Метод запроса  - GET

Обновляет токены, если рефреш еще действителен, пишет в куки
</details>
<details><summary>Выйти из аккаунта</summary>
<br>
  
    /api/auth/logout
    
  > Метод запроса  - GET

Выходит из аккаунта, удаляет куки, если пользователь был авторизован 
</details>

### РАБОТА С ДАННЫМИ ПОЛЬЗОВАТЕЛЯ

<details><summary>Получить данные профиля</summary>
  <br>
  
    /api/users/me
    
  > Метод запроса  - GET
</details>
<details><summary>Обновить данные профиля</summary>
    <br>
  
    /api/users/update_profile
        
  > Метод запроса  - PUT
</details>
<details><summary>Проверить старый пароль</summary>
    <br>
  
    /api/users/check_password/{oldPassword}
    
  > Метод запроса  - GET
</details>
<details><summary>Обновить пароль пользователя</summary>
    <br>
  
    /api/users/update_user_password
        
  > Метод запроса  - PUT
</details>

### КОЛЕСО ЖИЗНЕННОГО БАЛАНСА

<details><summary>Получить данные по колесу баланса авторизованного пользователя</summary>
      <br>
  
    /api/balanceCircle/circle_data
    
  > Метод запроса  - GET
</details>
<details><summary>Добавить элемент колеса баланса авторизованного пользователя</summary>
    <br>
  
    /api/balanceCircle/insert_value
        
  > Метод запроса  - POST
</details>
<details><summary>Обновить элемент колеса баланса (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/balanceCircle/{id}
        
  > Метод запроса  - PUT
</details>
<details><summary>Удалить элемент колеса баланса (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/balanceCircle/{id}
        
  > Метод запроса  - DELETE
</details>

### СПИСОК ЗАДАЧ

<details><summary>Получить данные по списку дел авторизованного пользователя</summary>
      <br>
  
    /api/tasksList/tasks_in_list
    
  > Метод запроса  - GET
</details>
<details><summary>Добавить элемент списка дел авторизованного пользователя</summary>
    <br>
  
    /api/tasksList/insert_task_in_list
        
  > Метод запроса  - POST
</details>
<details><summary>Обновить элемент списка дел (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/tasksList/{id}
        
  > Метод запроса  - PUT
</details>
<details><summary>Удалить элемент списка дел (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/tasksList/{id}
        
  > Метод запроса  - DELETE
</details>

### КАНБАН КАРТОЧКИ

<details><summary>Получить данные по карточкам канбан авторизованного пользователя</summary>
      <br>
  
    /api/kanbanCards/kanban_cards

  > Метод запроса  - GET
</details>
<details><summary>Добавить карточку канбан авторизованного пользователя</summary>
    <br>
  
    /api/kanbanCards/insert_kanban_card
    
  > Метод запроса  - POST
</details>
<details><summary>Обновить карточку канбан (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/kanbanCards/{id}
    
  > Метод запроса  - PUT
</details>
<details><summary>Удалить карточку канбан (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/kanbanCards/{id}
    
  > Метод запроса  - DELETE
</details>

### ЗАДАЧИ В КАНБАН КАРТОЧКАХ

<details><summary>Получить данные по задачам в карточке канбан авторизованного пользователя</summary>
      <br>
  
    /api/taskInCards/tasks_in_card/{id}

  > Метод запроса  - GET
</details>
<details><summary>Добавить задачу в карточку канбан авторизованного пользователя</summary>
    <br>
  
    /api/taskInCards/insert_task/{id}
    
  > Метод запроса  - POST
</details>
<details><summary>Обновить задачу в карточке канбан (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/taskInCards/{id}
    
  > Метод запроса  - PUT
</details>
<details><summary>Удалить задачу в карточке канбан (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/taskInCards/{id}
    
  > Метод запроса  - DELETE
</details>

### ЗАДАЧИ ДЛЯ ДИАГРАММЫ ГАНТА

<details><summary>Получить данные по задачам в диаграмме Ганта авторизованного пользователя</summary>
      <br>
  
    /api/ganttChartTasks/gantt_tasks_data

  > Метод запроса  - GET
</details>
<details><summary>Добавить задачу в диаграмму Ганта авторизованного пользователя</summary>
    <br>
  
    /api/ganttChartTasks/insert_gantt_task
    
  > Метод запроса  - POST
</details>
<details><summary>Обновить задачу в диаграмме Ганта (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/ganttChartTasks/{id}
    
  > Метод запроса  - PUT
</details>
<details><summary>Удалить задачу в диаграмме Ганта (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/ganttChartTasks/{id}
    
  > Метод запроса  - DELETE
</details>

### ДЛИТЕЛЬНОСТЬ ЗАДАЧ ДЛЯ ДИАГРАММЫ ГАНТА

<details><summary>Получить данные по длительностям задачи в диаграмме Ганта авторизованного пользователя</summary>
      <br>
  
    /api/ganttChartTaskDuration/gantt_durations_data/{id}

  > Метод запроса  - GET
</details>
<details><summary>Добавить длительность задачи в диаграмму Ганта авторизованного пользователя</summary>
    <br>
  
    /api/ganttChartTaskDuration/insert_duration/{id}
    
  > Метод запроса  - POST
</details>
<details><summary>Обновить длительность задачи в диаграмме Ганта (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/ganttChartTaskDuration/{id}
    
  > Метод запроса  - PUT
</details>
<details><summary>Удалить длительность задачи в диаграмме Ганта (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/ganttChartTaskDuration/{id}
    
  > Метод запроса  - DELETE
</details>

### ЗАПИСИ В ЕЖЕДНЕВНИКЕ

<details><summary>Получить данные по записям в ежедневнике авторизованного пользователя</summary>
      <br>
  
    /api/entryDailyPlanner/DailyPlanner/entry_data

  > Метод запроса  - GET
</details>
<details><summary>Добавить запись в ежедневник авторизованного пользователя</summary>
    <br>
  
    /api/entryDailyPlanner/insert_entry
    
  > Метод запроса  - POST
</details>
<details><summary>Обновить запись в ежедневнике (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/entryDailyPlanner/{id}
    
  > Метод запроса  - PUT
</details>
<details><summary>Удалить запись в ежедневнике (по коду) авторизованного пользователя</summary>
      <br>
  
    /api/entryDailyPlanner/{id}
    
  > Метод запроса  - DELETE
</details>

### ВЗАИМОДЕЙСТВИЕ С ПОЧТОЙ

<details><summary>Отправка сообщения на почту зарегистрированного пользователя</summary>
      <br>
  
    /email/verify_profile

  > Метод запроса  - GET
</details>
<details><summary>Сравнить коды подтверждения: отправленный и введенный</summary>
    <br>
  
    /email/verify_auth_code/{user_specified_code}

  > Метод запроса  - GET
</details>
<details><summary>Сравнение кодов подтверждения при регистрации</summary>
      <br>
  
    /email/verify_mail_not_auth
    
  > Метод запроса  - POST
</details>

### СХЕМА ДАННЫХ

> Русифицированная схема данных
> 
> ![image](https://github.com/vergeeva/backendManagement/assets/61785118/38378c20-80e5-4f95-857f-0379500c72e6)

<details><summary>Взаимодействие с Docker</summary>
<br> Запуск Docker
  
    docker-compose up -d
<br> Остановка Docker
  
    docker-compose down
<br> Создание расширения
  
    docker exec -it <Имя_контейнера> bash

<br> Вход в запущенную базу
  
    psql -U <Имя_пользователя> <Имя_базы_данных>
<br> Установка модуля uuid-ossp
  
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
</details>

<details><summary>Миграции базы данных</summary>
<br> Создание миграции
  
    alembic revision --autogenerate -m "имя_миграции"
<br> Отправка изменений в базу
  
    alembic upgrade head
</details>

<details><summary>Переменные, указанные в .env файле</summary>
    
    DATABASE_PORT
    POSTGRES_PASSWORD
    POSTGRES_USER
    POSTGRES_DB
    POSTGRES_HOST
    POSTGRES_HOSTNAME
    
    MAIL_USERNAME
    MAIL_PASSWORD
    MAIL_FROM
    MAIL_PORT
    MAIL_SERVER
    MAIL_STARTTLS=False
    MAIL_SSL_TLS=True
    USE_CREDENTIALS=True
    VALIDATE_CERTS=True
    
    ACCESS_TOKEN_EXPIRES_IN
    REFRESH_TOKEN_EXPIRES_IN
    JWT_ALGORITHM
    
    CLIENT_ORIGIN
    
    JWT_PRIVATE_KEY
    JWT_PUBLIC_KEY
</details>
