from sqlmodel import Session, select
from database import engine
from models import Category, Product, ProductAttribute


catalog = [
    ("Велосипеды", "bikes", "Для города, лесных троп и новых маршрутов", [
        ("Велосипед Trail 29", "VELO", 42900, "bike", "#728276", "Выбор команды", {"Рама": "Алюминий, M / 17″", "Колёса": "29 дюймов", "Скорости": "21", "Тормоза": "Дисковые механические", "Вес": "14,2 кг"}),
        ("Велосипед City 28", "VELO", 31900, "bike", "#b99577", "Для города", {"Рама": "Алюминий, M / 18″", "Колёса": "28 дюймов", "Скорости": "7", "Тормоза": "Ободные", "Вес": "13,5 кг"}),
        ("Велосипед Gravel 700", "NORD", 68900, "bike", "#525d70", "Новинка", {"Рама": "Алюминий, M / 54 см", "Колёса": "700C", "Скорости": "18", "Тормоза": "Дисковые", "Вес": "11,3 кг"}),
    ]),
    ("Запчасти", "parts", "Всё, чтобы велосипед работал как часы", [
        ("Педали Platform", "NORD", 2490, "pedal", "#626b63", "", {"Материал": "Алюминий", "Резьба": "9/16″", "Комплект": "2 педали"}),
        ("Покрышка Trail Grip 29", "VELO", 2190, "tire", "#454846", "", {"Размер": "29 × 2,1″", "Назначение": "Горный велосипед", "Корд": "Стальной"}),
        ("Седло Comfort", "NORD", 3290, "saddle", "#5f6660", "", {"Покрытие": "Экокожа", "Ширина": "155 мм", "Наполнитель": "Пена"}),
    ]),
    ("Аксессуары", "accessories", "Полезные детали для каждой поездки", [
        ("Фляга Flow 750", "VELO", 890, "bottle", "#80927f", "Бестселлер", {"Объём": "750 мл", "Материал": "Пластик без BPA", "Вес": "85 г"}),
        ("Велозамок Secure", "NORD", 1890, "lock", "#515c55", "", {"Тип": "U-lock", "Материал": "Закалённая сталь", "Ключи": "2 шт."}),
        ("Насос Mini Air", "VELO", 1490, "pump", "#9f856f", "", {"Ниппель": "Presta / Schrader", "Давление": "До 8 бар", "Длина": "22 см"}),
    ]),
    ("Экипировка", "gear", "Комфорт и защита на любом расстоянии", [
        ("Шлем Urban Air", "NORD", 4490, "helmet", "#bda98a", "Выбор команды", {"Размер": "M, 55–59 см", "Вентиляция": "18 отверстий", "Вес": "260 г"}),
        ("Перчатки Ride", "VELO", 1590, "gloves", "#727d6a", "", {"Размер": "M", "Материал": "Полиэстер", "Ладонь": "Гелевые вставки"}),
        ("Очки Horizon", "NORD", 2990, "glasses", "#4d595b", "Новинка", {"Защита": "UV400", "Линза": "Поликарбонат", "Комплект": "Чехол"}),
    ]),
    ("Свет и электроника", "electronics", "Видеть дорогу и быть заметным", [
        ("Фара Beam 600", "VELO", 2790, "light", "#596b61", "", {"Яркость": "600 лм", "Зарядка": "USB-C", "Время работы": "До 6 часов"}),
        ("Задний фонарь Dot", "VELO", 1190, "light", "#ba7266", "", {"Яркость": "50 лм", "Режимы": "4", "Защита": "IPX4"}),
        ("Велокомпьютер Track", "NORD", 3490, "computer", "#525d56", "", {"Подключение": "Беспроводное", "Функции": "Скорость, дистанция, время", "Питание": "CR2032"}),
    ]),
]


def seed_data():
    with Session(engine) as session:
        if session.exec(select(Category)).first():
            return
        for name, slug, description, products in catalog:
            category = Category(name=name, slug=slug, description=description)
            session.add(category)
            session.flush()
            for title, brand, price, image, color, badge, attributes in products:
                product = Product(category_id=category.id, name=title, brand=brand,
                    description=f"{title} — практичный выбор для ежедневных поездок. " + description + ". Модель из учебной коллекции магазина «Вело».",
                    price=price * 100,
                    image=image, color=color, badge=badge, stock=12)
                session.add(product)
                session.flush()
                for key, value in attributes.items():
                    session.add(ProductAttribute(product_id=product.id, name=key, value=value))
        session.commit()
