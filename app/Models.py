import uuid
from .database import BaseModel
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(BaseModel):  # Пользователи
    __tablename__ = 'users'  # имя таблицы
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)  # Код пользователя
    email = Column(String, unique=True, nullable=True)  # почта
    firstName = Column(String, nullable=False)  # имя
    lastName = Column(String, nullable=False)  # фамилия
    patronymic = Column(String, nullable=True)  # отчество
    login = Column(String, unique=True, nullable=False)  # логин
    password = Column(String, nullable=False)  # пароль
    verified = Column(Boolean, nullable=False, server_default='False')  # подтверждена ли почта
    verification_code = Column(String, nullable=True, unique=True)  # код подтверждения


class KanbanCards(BaseModel):  # Карточки канбан
    __tablename__ = 'kanban_cards'  # имя таблицы
    idCard = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                    default=uuid.uuid4)  # код карточки канбан
    typeOfCard = Column(UUID(as_uuid=True), ForeignKey(
        'cards_type.idType', ondelete='CASCADE'), nullable=False)  # тип карточки
    userId = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)  # код пользователя


class TypeOfCards(BaseModel):  # Типы карточек
    __tablename__ = 'cards_type'  # имя таблицы
    idType = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                    default=uuid.uuid4)  # код типа карточки
    typeName = Column(String, unique=True, nullable=False)  # имя типа карточки


class TaskInCards(BaseModel):  # задачи в карточках
    __tablename__ = 'task_in_cards'  # имя таблицы
    idTaskInCard = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                          default=uuid.uuid4)  # код задачи в карточке
    cardId = Column(UUID(as_uuid=True), ForeignKey(
        'kanban_cards.idCard', ondelete='CASCADE'), nullable=False)  # код карточки
    taskText = Column(String, nullable=False)  # текст задачи
    isDone = Column(Boolean, nullable=False)  # зачеркнута или нет


class EntryDailyPlanner(BaseModel):  # Запись в ежедневнике
    __tablename__ = 'daily_planner'  # имя таблицы
    idTaskInCard = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                          default=uuid.uuid4)  # код записи в ежедневнике
    dailyTaskName = Column(String, nullable=False)  # текст задачи
    taskStart = Column(Date, nullable=False)  # дата и время начала
    taskEnd = Column(Date, nullable=False)  # дата и время окончания
    taskColor = Column(String, nullable=False)  # цвет оформления задачи
    taskStatus = Column(Boolean, nullable=False)  # статус выполнения задачи
    userId = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)  # код пользователя


class TechnicsSettings(BaseModel):  # Настройки техники Помодорро
    __tablename__ = 'technics_settings'  # имя таблицы
    idTechnic = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                       default=uuid.uuid4)  # код техники
    workTimer = Column(Integer, nullable=False)  # рабочий таймер
    shortBreak = Column(Integer, nullable=False)  # короткий перерыв
    longBreak = Column(Integer, nullable=False)  # длинный перерыв
    countOfCycles = Column(Integer, nullable=False)  # количество циклов
    userId = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)  # код пользователя


class telegramUsers(BaseModel):  # Пользователи telegram
    __tablename__ = 'telegram_users'  # имя таблицы
    chatId = Column(Integer, unique=True, nullable=False, primary_key=True)  # код чата
    statusId = Column(Integer, nullable=False)  # статус чата


class ItemsList(BaseModel):
    __tablename__ = 'tasks_list'  # имя таблицы
    idTaskInList = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                          default=uuid.uuid4)  # код элемента в списке
    textOfItem = Column(String, nullable=False)  # текст элемента
    isChecked = Column(Boolean, nullable=False)  # сделано или нет
    userListsId = Column(UUID(as_uuid=True), ForeignKey(
        'user_lists.idUserList', ondelete='CASCADE'), nullable=False)  # код пользователя


class UserLists(BaseModel):
    __tablename__ = 'user_lists'  # имя таблицы
    idUserList = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                        default=uuid.uuid4)  # код списка
    nameOfList = Column(String, nullable=False)  # название списка
    userId = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)  # код пользователя


class GanttChartTasks(BaseModel):  # Задачи в диаграмме Гантта
    __tablename__ = 'gantt_tasks'  # имя таблицы
    idGanttTask = Column(Integer, unique=True, nullable=False,
                         primary_key=True, autoincrement=True)
    nameOfTask = Column(String, nullable=False)  # наименование задачи
    userId = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)  # код пользователя


class GanttChartTaskDuration(BaseModel):  # Длительность задач в д. Гантта
    __tablename__ = 'gantt_task_duration'  # имя таблицы
    idGanttTask = Column(Integer, unique=True, nullable=False,
                         primary_key=True, autoincrement=True)
    ganttTaskStart = Column(Date, nullable=False)  # дата и время начала
    ganttTaskEnd = Column(Date, nullable=False)  # дата и время окончания
    projectId = Column(Integer, ForeignKey('gantt_tasks.idGanttTask', ondelete='CASCADE'), nullable=False)  # код задачи в д. Гантта


class BalanceCircle(BaseModel):  # Колесо жизненного баланса
    __tablename__ = 'balance_circle'  # имя таблицы
    idBalance = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                       default=uuid.uuid4)  # код техники
    labelItem = Column(String, nullable=False) #
    value = Column(Integer, nullable=False)
    userId = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)  # код пользователя
