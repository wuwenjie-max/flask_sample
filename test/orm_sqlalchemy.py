from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/test",
                       echo=True,
                       pool_size=8,
                       pool_recycle=60*30)

Base = declarative_base(engine)
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    phone = Column(String(120))
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __repr__(self):
        return "User name: {} phone: {}".format(self.name, self.phone)
Base.metadata.create_all(engine)


DbSession = sessionmaker(bind=engine)
session = DbSession()

# user = Users('wu', '1320921312300')
# session.add(user)
# session.commit()

users = session.query(Users).all()
for item in users:
    print(item)
