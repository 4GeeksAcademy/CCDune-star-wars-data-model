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
    birth_year: Mapped[str]
    #eye_color: Mapped["Author"] = relationship(back_populates="books")
    eye_color: Mapped[str] 
    gender: Mapped[str]
    hair_color: Mapped[str]
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
        return f"<Characters {self.name}>"
    
class Planets(Base):
    __tablename__ = "Planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    diameter: Mapped[int] = mapped_column(ForeignKey("user.id"))
    #eye_color: Mapped["Author"] = relationship(back_populates="books")
    rotation_period: Mapped[str] 
    orbital_period: Mapped[str]
    gravity: Mapped[str]
    population: Mapped[str]
    climate: Mapped[str]
    terrain: Mapped[str]
    surface_water: Mapped[str]
    residents: Mapped[str]
    #skin_color: Mapped[List["Genre"]] = relationship(
    #    back_populates="books",
    #    secondary=book_to_genre,
   # )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            # "author": self.author,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "residents": self.residents
        }

    def __repr__(self):
        return f"<Planets {self.name}>"
    

class Vehicles(Base):
    __tablename__ = "Vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    #diameter: Mapped[int] = mapped_column(ForeignKey("user.id"))
    #eye_color: Mapped["Author"] = relationship(back_populates="books")
    model: Mapped[str] 
    vehicle_class: Mapped[str]
    manufacturer: Mapped[str]
    length: Mapped[str]
    cost_in_credits: Mapped[str]
    crew: Mapped[str]
    passengers: Mapped[str]
    max_atmosphering_speed: Mapped[str]
    cargo_capacity: Mapped[str]
    consumables: Mapped[str]
    #skin_color: Mapped[List["Genre"]] = relationship(
    #    back_populates="books",
    #    secondary=book_to_genre,
   # )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            # "author": self.author,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "length": self.length,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.sucargo_capacityface_water,
            "consumables": self.consumables
        }

    def __repr__(self):
        return f"<Vehicles {self.name}>"