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

<details><summary>Получить данные по колесу баланса авторизованного пользателя</summary>
      <br>
  
    /api/balanceCircle/circle_data
    
  > Метод запроса  - GET
</details>
<details><summary>Добавить элемент колеса баланса авторизованного пользателя</summary>
    <br>
  
    /api/balanceCircle/insert_value
        
  > Метод запроса  - POST
</details>
<details><summary>Обновить элемент колеса баланса (по коду) авторизованного пользателя</summary>
      <br>
  
    /api/balanceCircle/{id}
        
  > Метод запроса  - PUT
</details>
<details><summary>Удалить элемент колеса баланса (по коду) авторизованного пользателя</summary>
      <br>
  
    /api/balanceCircle/{id}
        
  > Метод запроса  - DELETE
</details>

### СПИСОК ЗАДАЧ

<details><summary>Получить данные по списку дел авторизованного пользателя</summary>
      <br>
  
    /api/tasksList/tasks_in_list
    
  > Метод запроса  - GET
</details>
<details><summary>Добавить элемент списка дел авторизованного пользателя</summary>
    <br>
  
    /api/tasksList/insert_task_in_list
        
  > Метод запроса  - POST
</details>
<details><summary>Обновить элемент списка дел (по коду) авторизованного пользателя</summary>
      <br>
  
    /api/tasksList/{id}
        
  > Метод запроса  - PUT
</details>
<details><summary>Удалить элемент списка дел (по коду) авторизованного пользателя</summary>
      <br>
  
    /api/tasksList/{id}
        
  > Метод запроса  - DELETE
</details>

### КАНБАН КАРТОЧКИ

<details><summary>Получить данные по карточкам канбан авторизованного пользателя</summary>
      <br>
  
    /api/kanbanCards/kanban_cards

  > Метод запроса  - GET
</details>
<details><summary>Добавить карточку канбан авторизованного пользателя</summary>
    <br>
  
    /api/kanbanCards/insert_kanban_card
    
  > Метод запроса  - POST
</details>
<details><summary>Обновить карточку канбан (по коду) авторизованного пользателя</summary>
      <br>
  
    /api/kanbanCards/{id}
    
  > Метод запроса  - PUT
</details>
<details><summary>Удалить карточку канбан (по коду) авторизованного пользателя</summary>
      <br>
  
    /api/kanbanCards/{id}
    
  > Метод запроса  - DELETE
</details>
