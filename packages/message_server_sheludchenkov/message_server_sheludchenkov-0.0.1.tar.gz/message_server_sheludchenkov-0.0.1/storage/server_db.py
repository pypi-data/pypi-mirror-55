from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,\
    DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import exc
from datetime import datetime
from jim.config import USER_STATUS


class Storage:
    """Класс для работы с БД"""
    Base = declarative_base()

    def __init__(self):
        self.engine = create_engine('sqlite:///server_data.sqlite3')
        # self.mem_engine = create_engine('sqlite:///:memory:')
        self.Base.metadata.create_all(self.engine)
        session_factory = sessionmaker(self.engine)
        self.session = scoped_session(session_factory)
        # self.session = session()

    def add_friend(self, client, friend):
        """
        Сделать связь между клиентами

        :param client: Клиент
        :param friend: Друг
        :return:
        """
        connection = self.ClientRelation(client_id=client.id,
                                         friend_id=friend.id)
        try:
            self.session.add(connection)
            self.session.commit()
            return True
        except exc.IntegrityError:
            return False

    def del_friend(self, client, friend):
        """
        Удалить связь между клиентами

        :param client: Клиент
        :param friend: Друг
        :return:
        """
        try:
            self.session.query(self.ClientRelation).filter(
                self.ClientRelation.client_id == client.id,
                self.ClientRelation.friend_id == friend.id).delete()
            self.session.commit()
            return True
        except exc.IntegrityError:
            return False

    def get_all_clients(self):
        """
        Получить список всех клиентов

        :return: Clients.query
        """
        return self.session.query(self.Client).all()

    def get_client_by_name(self, username):
        """
        Получить клиента по имени

        :param username: Имя клиента
        :return: str
        """
        return self.session.query(self.Client).filter(
            self.Client.login == username).first()

    def get_friends(self, user):
        """
        Получить друзей клиента

        :param user: Клиент
        :return: list(Client)
        """
        result = list()
        for i in self.session.query(self.ClientRelation).filter(
                self.ClientRelation.client_id == user.id).all():
            friend = self.session.query(self.Client).get(i.friend_id)
            if friend:
                result.append(friend)
        return result

    def register_action(self, client, ip_address, action=None,
                        recepients=None, message=None):
        """
        Занести действие в БД

        :param client: Клиент
        :param ip_address: Адресс
        :param action: Действие
        :param recepients: Получатель
        :param message: Сообщение
        :return: None
        """
        login = self.ClientHistory(client_id=client.id, ip_address=ip_address,
                                   action=action, recepients=recepients,
                                   message=message)
        try:
            self.session.add(login)
            self.session.commit()
            return login
        except exc.IntegrityError:
            self.session.rollback()
            return None

    def register_client(self, username):
        """
        Добавить клиента в БД

        :param username: Имя пользователя
        :return: Client
        """
        client = self.Client(username)
        # print(f"Registered client: {client}")
        try:
            self.session.add(client)
            self.session.commit()
            return client
        except exc.IntegrityError:
            self.session.rollback()
            # print(f"Client {client} already exists")
            return self.session.query(self.Client).filter(
                self.Client.login == username).first()

    class Client(Base):
        """Список всех клиентов"""
        __tablename__ = 'Clients'
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        register_date = Column(DateTime, default=datetime.now())
        status = Column(String, default=USER_STATUS.OFFLINE)
        last_presence_time = Column(DateTime, nullable=True)
        last_ip_address = Column(String, nullable=True)

        def __init__(self, login):
            self.login = login
            # self.information = information

        def __repr__(self):
            return f'<Client("{self.id} -- {self.login}", ' \
                   f'"{self.register_date}")>'

    class ClientHistory(Base):
        """История действий клиента"""
        __tablename__ = 'ClientHistory'
        id = Column(Integer, primary_key=True)
        client_id = Column(Integer, ForeignKey("Clients.id"))
        action = Column(String, nullable=True)
        action_time = Column(DateTime, default=datetime.now())
        ip_address = Column(String)
        recepients = Column(String, nullable=True)
        message = Column(String, nullable=True)
        client = relationship('Client')

        def __init__(self, client_id, ip_address, action, recepients, message):
            self.client_id = client_id
            self.ip_address = ip_address
            self.action = action
            self.recepients = recepients
            self.message = message

    class ClientRelation(Base):
        """Список отношений между клиентами"""
        __tablename__ = "ClientRelations"
        id = Column(Integer, primary_key=True)
        client_id = Column(Integer, ForeignKey("Clients.id"))
        friend_id = Column(Integer, ForeignKey("Clients.id"))
        client = relationship('Client',
                              foreign_keys="[ClientRelation.client_id]")
        friend = relationship('Client',
                              foreign_keys="[ClientRelation.friend_id]")

        def __init__(self, client_id, friend_id):
            self.client_id = client_id
            self.friend_id = friend_id

        def __repr__(self):
            return f'<client: {self.client_id}, friend: {self.friend_id}>'


if __name__ == '__main__':
    storage = Storage()
    test = storage.get_all_clients()
    print(test)
    user = storage.get_client_by_name("test1")
    clients = storage.get_friends(user)
    for i in clients:
        print(i)
