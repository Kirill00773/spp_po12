"""
Модуль для лабораторной работы №5.
Вариант 17: Разработка API и базы данных "Ресурсы Internet".
"""

# pylint: disable=too-few-public-methods, invalid-name

from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel

# --- НАСТРОЙКА БД ---
DATABASE_URL = "sqlite:///./internet_resources.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- МОДЕЛИ SQLALCHEMY ---
resource_tags = Table(
    "resource_tags",
    Base.metadata,
    Column("resource_id", ForeignKey("resources.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Category(Base):
    """Модель таблицы категорий."""

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    resources = relationship("Resource", back_populates="category")


class Resource(Base):
    """Модель таблицы ресурсов (сайтов)."""

    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="resources")
    reviews = relationship("Review", back_populates="resource")
    tags = relationship("Tag", secondary=resource_tags, back_populates="resources")


class User(Base):
    """Модель таблицы пользователей."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String)
    reviews = relationship("Review", back_populates="user")


class Review(Base):
    """Модель таблицы отзывов."""

    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float)
    comment = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))

    user = relationship("User", back_populates="reviews")
    resource = relationship("Resource", back_populates="reviews")


class Tag(Base):
    """Модель таблицы тегов."""

    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    resources = relationship("Resource", secondary=resource_tags, back_populates="tags")


Base.metadata.create_all(bind=engine)


# --- СХЕМЫ PYDANTIC ---
class CategoryCreate(BaseModel):
    """Схема для создания категории."""

    name: str


class CategoryOut(BaseModel):
    """Схема для вывода данных категории."""

    id: int
    name: str

    class Config:
        """Конфигурация Pydantic."""

        from_attributes = True


class ResourceBase(BaseModel):
    """Базовая схема ресурса."""

    title: str
    url: str
    description: Optional[str] = None
    category_id: int


class ResourceCreate(ResourceBase):
    """Схема для создания ресурса."""


class ResourceOut(ResourceBase):
    """Схема для вывода данных ресурса."""

    id: int

    class Config:
        """Конфигурация Pydantic."""

        from_attributes = True


# --- FASTAPI APP ---
app = FastAPI(title="Internet Resources API")


def get_db():
    """Зависимость для получения сессии базы данных."""
    database = SESSION_LOCAL()
    try:
        yield database
    finally:
        database.close()


@app.post("/categories/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Добавление новой категории."""
    db_cat = Category(name=category.name)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


@app.get("/categories/", response_model=List[CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    """Получение всех категорий."""
    return db.query(Category).all()


@app.post("/resources/", response_model=ResourceOut)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    """Добавление нового ресурса."""
    cat = db.query(Category).filter(Category.id == resource.category_id).first()
    if not cat:
        raise HTTPException(status_code=400, detail="Category not found.")

    db_resource = Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


@app.get("/resources/", response_model=List[ResourceOut])
def read_resources(db: Session = Depends(get_db)):
    """Получение всех ресурсов."""
    return db.query(Resource).all()


@app.delete("/resources/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """Удаление ресурса по ID."""
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(db_resource)
    db.commit()
    return {"message": "Deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
