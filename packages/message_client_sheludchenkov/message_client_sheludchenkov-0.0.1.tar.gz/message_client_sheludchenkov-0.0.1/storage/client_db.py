from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import or_, and_
from datetime import datetime


class ClientStorage:
    """Класс для работы с БД"""
    Base = declarative_base()

    def __init__(self, path='client_data.sqlite3'):
        """

        :param path: путь до базы данных
        """
        self.engine = create_engine(f'sqlite:///{path}')
        self.Base.metadata.create_all(self.engine)
        session = sessionmaker(self.engine, autocommit=True)
        self.session = session()

    def add_to_history(self, sender, receiver, message, time):
        """
        Добавить в историю

        :param sender: отправитель
        :param receiver: получатель
        :param message: сообщение
        :param time: время
        :return: None
        """
        sender_id = self.get_contact_id_by_name(sender)
        receiver_id = self.get_contact_id_by_name(receiver)
        time = datetime.fromtimestamp(time)
        line = self.History(sender_id=sender_id, receiver_id=receiver_id,
                            message=message, time=time)
        self.session.add(line)
        self.session.flush()

    def get_contact_by_name(self, name):
        """
        Поиск пользователя по имени

        :param name: имя
        :return: ContactList
        """
        return self.session.query(self.ContactList).filter(
            self.ContactList.user == name).first()

    def get_contact_id_by_name(self, name):
        """
        Поиск Id по имени

        :param name: имя пользователя
        :return: int: id
        """
        user = self.get_contact_by_name(name)
        if user:
            return user.id
        return None

    def get_contacts(self):
        """
        Получить всех пользователей

        :return: ContactList query
        """
        return self.session.query(self.ContactList).all()

    def get_contacts_list(self):
        """
        Получить всех пользователей в виде списка

        :return: list
        """
        result = list()
        for row in self.get_contacts():
            result.append([row.user, row.status, row.is_friend])
        return result

    def get_history(self, user, contact):
        """
        Получить всю историю сообщений между пользователями user и contact

        :param user: имя пользователя
        :param contact: имя собеседника
        :return: list(sender.user, receiver.user, message, time)
        """
        result = list()
        for i in self.session.query(self.History).filter(
                or_(and_(self.History.sender.has(user=user),
                         self.History.receiver.has(user=contact)),
                    and_(self.History.receiver.has(user=user),
                         self.History.sender.has(user=contact)))).all():
            result.append((i.sender.user, i.receiver.user, i.message, i.time))
        return result

    def update_contacts(self, contacts: dict):
        """
        Обновить текущие контакты

        :param contacts: список всех контактов
        :return:
        """
        all_contacts = self.get_contacts()
        # Update current
        for user in all_contacts:
            if user.user in contacts.keys():
                user.status = contacts[user.user]['status']
                user.is_friend = contacts[user.user]['is_friend']
                contacts.pop(user.user, None)
            else:
                self.session.delete(user)
        # Add new
        for user in contacts.keys():
            new_client = self.ContactList(user, contacts[user]['status'],
                                          contacts[user]['is_friend'])
            self.session.add(new_client)

    class ContactList(Base):
        """Список всех контактов"""
        __tablename__ = "Contacts"
        id = Column(Integer, primary_key=True)
        user = Column(String, unique=True)
        status = Column(String, default="Offline")
        is_friend = Column(Boolean, default=False)

        def __init__(self, user, status, is_friend):
            self.user = user
            self.status = status
            self.is_friend = is_friend

        def __repr__(self):
            return f"<{self.user}: {self.status}, {self.is_friend}>"

    class History(Base):
        """История сообщений"""
        __tablename__ = "History"
        id = Column(Integer, primary_key=True)
        sender_id = Column(Integer, ForeignKey("Contacts.id"))
        receiver_id = Column(Integer, ForeignKey("Contacts.id"))
        message = Column(String)
        time = Column(DateTime)
        sender = relationship('ContactList',
                              foreign_keys='[History.sender_id]')
        receiver = relationship('ContactList',
                                foreign_keys='[History.receiver_id]')

        def __init__(self, sender_id, receiver_id, message, time):
            self.sender_id = sender_id
            self.receiver_id = receiver_id
            self.message = message
            self.time = time

        def __repr__(self):
            return f'<{self.sender_id}, {self.receiver_id}, {self.message}, ' \
                   f'{self.time}>'


if __name__ == '__main__':
    contacts = {'test': {'status': 'offline', 'is_friend': False},
                'test2': {'status': 'online', 'is_friend': False},
                'test1': {'status': 'offline', 'is_friend': False},
                'test0': {'status': 'online', 'is_friend': False},
                'test3': {'status': 'online', 'is_friend': False},
                'Guest': {'status': 'online', 'is_friend': False}}
    storage = ClientStorage('sqlite:///../client_data.sqlite3')
    date = datetime.now()
    message = ('Guest', 'test3', 'test', date)

    history = storage.get_history('test1', 'Guest')
    for i in history:
        print(i)
