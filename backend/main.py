from contextlib import asynccontextmanager
from typing import Literal
from fastapi import Depends, FastAPI, HTTPException, Query, Response
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from database import create_tables, get_session
from models import Category, Order, OrderItem, Product, ProductAttribute, User
from schemas import LoginData, OrderData, ProfileData, RegisterData
from security import create_login, get_current_user, public_user
from seed import seed_data


@asynccontextmanager
async def lifespan(app):
    create_tables()
    seed_data()
    yield


app = FastAPI(title="Вело — API магазина", version="1.0.0", lifespan=lifespan)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/auth/register", status_code=201)
def register(data: RegisterData, response: Response, session: Session = Depends(get_session)):
    user = User(name=data.name, email=str(data.email).lower(), password=data.password)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Пользователь с такой почтой уже существует")
    session.refresh(user)
    return create_login(user, response)


@app.post("/api/auth/login")
def login(data: LoginData, response: Response, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == str(data.email).lower())).first()
    if not user or data.password != user.password:
        raise HTTPException(401, "Неверная почта или пароль")
    return create_login(user, response)


@app.post("/api/auth/logout")
def logout(response: Response):
    response.delete_cookie("user_id")
    return {"detail": "Вы вышли из аккаунта"}



@app.get("/api/users/me")
def me(user: User = Depends(get_current_user)):
    return public_user(user)


@app.put("/api/users/me")
def update_profile(data: ProfileData, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    for key, value in data.model_dump().items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return public_user(user)


@app.get("/api/categories")
def categories(session: Session = Depends(get_session)):
    return session.exec(select(Category).order_by(Category.id)).all()


@app.get("/api/products")
def products(category: int | None = None, search: str = Query(default="", max_length=100),
             sort: Literal["popular", "price_asc", "price_desc", "new"] = "popular",
             min_price: int = Query(default=0, ge=0), max_price: int | None = Query(default=None, ge=0),
             session: Session = Depends(get_session)):
    statement = select(Product).where(Product.price >= min_price)
    if category:
        statement = statement.where(Product.category_id == category)
    if max_price is not None:
        statement = statement.where(Product.price <= max_price)

    order = {"popular": Product.id, "price_asc": Product.price.asc(), "price_desc": Product.price.desc(), "new": Product.id.desc()}
    items = session.exec(statement.order_by(order[sort])).all()
    return [p for p in items if search.strip().casefold() in (p.name + " " + p.brand).casefold()]


@app.get("/api/products/{product_id}")
def product(product_id: int, session: Session = Depends(get_session)):
    item = session.get(Product, product_id)
    if not item:
        raise HTTPException(404, "Товар не найден")
    attributes = session.exec(select(ProductAttribute).where(ProductAttribute.product_id == product_id)).all()
    return {**item.model_dump(), "attributes": attributes}


def order_response(session, order):
    items = session.exec(select(OrderItem).where(OrderItem.order_id == order.id)).all()
    return {**order.model_dump(exclude={"request_id"}), "items": items}


@app.post("/api/orders", status_code=201)
def create_order(data: OrderData, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if data.delivery == "courier" and len(data.address.strip()) < 8:
        raise HTTPException(400, "Укажите полный адрес доставки")
    user_id = user.id
    session.rollback()

    session.execute(text("BEGIN IMMEDIATE"))
    existing = session.exec(select(Order).where(Order.request_id == data.request_id)).first()
    if existing:
        if existing.user_id != user_id:
            raise HTTPException(409, "Повторите оформление заказа")
        return order_response(session, existing)
    quantities = {}
    for item in data.items:
        quantities[item.product_id] = quantities.get(item.product_id, 0) + item.quantity
    products = []
    subtotal = 0
    for product_id, quantity in quantities.items():
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(404, "Один из товаров больше не доступен")
        if quantity > product.stock:
            raise HTTPException(409, f"{product.name}: в наличии {product.stock} шт.")
        subtotal += product.price * quantity
        products.append((product, quantity))
    delivery_price = 0 if data.delivery == "pickup" or subtotal >= 1000000 else 39000
    order = Order(user_id=user_id, request_id=data.request_id, name=data.name, phone=data.phone,
                  delivery=data.delivery, address=data.address if data.delivery == "courier" else "Пункт самовывоза «Вело»",
                  subtotal=subtotal, delivery_price=delivery_price, total=subtotal + delivery_price)
    session.add(order)
    session.flush()
    for product, quantity in products:
        session.add(OrderItem(order_id=order.id, product_id=product.id, name=product.name,
                              price=product.price, quantity=quantity, image=product.image, color=product.color))
        product.stock -= quantity
        session.add(product)
    session.commit()
    session.refresh(order)
    return order_response(session, order)


@app.get("/api/orders")
def orders(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    items = session.exec(select(Order).where(Order.user_id == user.id).order_by(Order.id.desc())).all()
    return [order_response(session, item) for item in items]


@app.get("/api/orders/{order_id}")
def read_order(order_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(404, "Заказ не найден")
    return order_response(session, order)
