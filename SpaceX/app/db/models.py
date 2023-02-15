from __future__ import annotations
from typing import Optional, Type, Union
from typing_extensions import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey

LaunchForeignKey = Annotated[
    str, mapped_column(ForeignKey("launch.id", ondelete="CASCADE"))
]

TableType = Union[
    Type["Launch"],
    Type["Mission"],
    Type["Rocket"],
]


class Base(DeclarativeBase):
    """Base"""


class Launch(Base):
    """
    Model that contains name and images sources of data like Oricon,Shoseki etc.
    Related to :model: SourceType
    """

    __tablename__ = "launch"
    id: Mapped[str] = mapped_column(primary_key=True)
    details: Mapped[Optional[str]]
    mission: Mapped[Mission] = relationship(back_populates="launch")
    rocket: Mapped[Rocket] = relationship(back_populates="launch")


class Mission(Base):
    """
    Model that contains name and images sources of data like Oricon,Shoseki etc.
    Related to :model: SourceType
    """

    __tablename__ = "mission"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    launch_id: Mapped[LaunchForeignKey]
    launch: Mapped[Launch] = relationship(back_populates="mission")


class Rocket(Base):
    """
    Model that contains name and images sources of data like Oricon,Shoseki etc.
    Related to :model: SourceType
    """

    __tablename__ = "rocket"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    launch_id: Mapped[LaunchForeignKey]
    launch: Mapped[Launch] = relationship(back_populates="rocket")
