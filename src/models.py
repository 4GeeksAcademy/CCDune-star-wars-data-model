from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    String, Column, Table, ForeignKey, Boolean
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped,
    mapped_column, relationship,
)

class Base(DeclarativeBase):
    """
    This is magic that can be ignored
    for now!  It's a special tool
    that will help us later.
    """

db = SQLAlchemy(model_class=Base)

class User(Base):
    """
    This is the new SQA 2.0 style:
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False,
    )
    email: Mapped[str]
    password: Mapped[str] = mapped_column(
        String(256), nullable=False,
    )


class Characters(Base):
    __tablename__ = "Characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    birth_year: Mapped[int] = mapped_column(ForeignKey("author.id"))
    #eye_color: Mapped["Author"] = relationship(back_populates="books")
    eye_color: Mapped[str] 
    gender: Mapped[str]
    hair_color: Mapped[date]
    height: Mapped[str]
    mass: Mapped[str]
    skin_color: Mapped[str]
    #skin_color: Mapped[List["Genre"]] = relationship(
    #    back_populates="books",
    #    secondary=book_to_genre,
   # )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            # "author": self.author,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color

        }

    def __repr__(self):
        return f"<Character {self.name}>"