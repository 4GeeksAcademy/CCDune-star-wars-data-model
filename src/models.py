from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

favorite_character_table = Table(
    "favorite_character",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)

favorite_planet_table = Table(
    "favorite_planet",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planet_id", ForeignKey("planet.id"), primary_key=True),
)

favorite_vehicle_table = Table(
    "favorite_vehicle",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("vehicle_id", ForeignKey("vehicle.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Many-to-many favorites
    favorite_characters: Mapped[list["Character"]] = relationship(
        secondary=favorite_character_table,
        back_populates="fans",
        lazy="selectin",
    )
    favorite_planets: Mapped[list["Planet"]] = relationship(
        secondary=favorite_planet_table,
        back_populates="fans",
        lazy="selectin",
    )

    favorite_vehicles: Mapped[list["Vehicle"]] = relationship(
    secondary=favorite_vehicle_table,
    back_populates="fans",
    lazy="selectin",
)

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "favorite_characters": [c.id for c in self.favorite_characters],
            "favorite_planets": [p.id for p in self.favorite_planets],
            "favorite_vehicles": [v.id for v in self.favorite_vehicles]
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Character(Base):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str | None]
    eye_color: Mapped[str | None]
    gender: Mapped[str | None]
    hair_color: Mapped[str | None]
    height: Mapped[str | None]
    mass: Mapped[str | None]
    skin_color: Mapped[str | None]

    fans: Mapped[list[User]] = relationship(
        secondary=favorite_character_table,
        back_populates="favorite_characters",
        lazy="selectin",
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
        }

    def __repr__(self) -> str:
        return f"<Character {self.name}>"

class Planet(Base):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[int | None]  
    rotation_period: Mapped[str | None]
    orbital_period: Mapped[str | None]
    gravity: Mapped[str | None]
    population: Mapped[str | None]
    climate: Mapped[str | None]
    terrain: Mapped[str | None]
    surface_water: Mapped[str | None]

    
    fans: Mapped[list[User]] = relationship(
        secondary=favorite_planet_table,
        back_populates="favorite_planets",
        lazy="selectin",
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
        }

    def __repr__(self) -> str:
        return f"<Planet {self.name}>"

class Vehicle(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str | None]
    vehicle_class: Mapped[str | None]
    manufacturer: Mapped[str | None]
    length: Mapped[str | None]
    cost_in_credits: Mapped[str | None]
    crew: Mapped[str | None]
    passengers: Mapped[str | None]
    max_atmosphering_speed: Mapped[str | None]
    cargo_capacity: Mapped[str | None]
    consumables: Mapped[str | None]

    fans: Mapped[list[User]] = relationship(
    secondary=favorite_vehicle_table,
    back_populates="favorite_vehicles",
    lazy="selectin",
)


    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
        }

    def __repr__(self) -> str:
        return f"<Vehicle {self.name}>"
