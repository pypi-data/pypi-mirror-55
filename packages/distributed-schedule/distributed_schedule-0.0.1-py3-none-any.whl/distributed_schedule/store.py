from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import sessionmaker


Base = declarative_base()


engine = create_engine('sqlite:///test.db')


class ClientsInfo(Base):
    __tablename__ = 'clientsinfo'
    id = Column(Integer, primary_key=True)
    client_id = Column(String(32), index=True, nullable=False)

    def __str__(self):
        return "id : {0}  client_id : {1}".format(self.id, self.client_id)


class TasksInfo(Base):
    __tablename__ = 'tasksinfo'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(32), nullable=True)
    # 1: 实时任务  2：延时任务 比如延时30秒执行一次 3: 定时任务(cron表达式）
    task_type = Integer()
    cron_expr = Column(String(32), nullable=True)
    call_later_time = Integer()
    # 客户端的id
    client_id = Column(String(32), index=True, nullable=False)

    def __str__(self):
        return "id : {0}  task_id : {1}".format(self.id, self.task_id)


class TaskTrigger(Base):
    __tablename__ = 'tasktrigger'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(32), nullable=True)
    client_id = Column(String(32), index=True, nullable=False)
    # 一个任务组的uuid
    task_group_id = Column(String(63), nullable=False)
    # 1: 正在执行  2：执行成功 3：执行失败
    status = Integer()
    # 1: 执行一次如果失败了则保证直到有结果无论是失败或者成功 2：不需要确保执行
    task_status = Integer()

    def __str__(self):
        return "id : {0}  task_id : {1}".format(self.id, self.task_id)


Base.metadata.create_all(engine)


class Store(object):

    def __init__(self):
        self.session = sessionmaker(bind=engine)()

    def register_task(self, **kwargs):
        data = {}
        if "task_id" in kwargs:
            data["task_id"] = kwargs.get("task_id")

        if "task_type" in kwargs:
            data["task_type"] = kwargs.get("task_type")

        if "cron_expr" in kwargs:
            data["cron_expr"] = kwargs.get("cron_expr")

        if "call_later_time" in kwargs:
            data["call_later_time"] = kwargs.get("call_later_time")

        if "client_id" in kwargs:
            data["client_id"] = kwargs.get("client_id")

