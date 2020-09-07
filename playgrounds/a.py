from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Wagie(Base):
    __tablename__ = "wagie"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    wage = Column(Integer)
    email = None

    def create_email(self):
        pass

    def __str__(self):
        return f"Wagie name:{self.name} lastname:{self.last_name}"


engine = create_engine("sqlite:///test.db", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

with Session.Session() as session:

    wagie = Wagie(name="Wojak", last_name="Doomer", wage=1000)
    session.add(wagie)
    session.commit()
    wagies = session.query(Wagie).all()
    print(wagies)

#session.close()