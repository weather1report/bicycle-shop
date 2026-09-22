<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();
</script>

<template>
    <div class="container page info-page">
        <div class="breadcrumb">
            <RouterLink to="/">Главная</RouterLink>
            <span>/</span>
            {{ route.meta.title }}
        </div>
        <template v-if="route.path === '/about'">
            <span class="eyebrow">В ДВИЖЕНИИ — СМЫСЛ</span>
            <h1>Меньше суеты.<br>Больше <em>велосипеда.</em></h1>
            <p class="lead">«Вело» — магазин для тех, кто любит дорогу, свежий воздух и маленькие открытия по пути.</p>
            <div class="info-columns">
                <section>
                    <h2>Всё начинается с поездки</h2>
                    <p>Мы собрали велосипеды, запчасти, аксессуары, экипировку и свет в одном каталоге. Здесь легко сравнить характеристики и подобрать нужную вещь для своего маршрута.</p>
                </section>
            </div>
            <RouterLink to="/catalog" class="button">Найти что-то для себя →</RouterLink>
        </template>
        <template v-else-if="route.path === '/delivery'">
            <span class="eyebrow">ПРОСТО И ПОНЯТНО</span>
            <h1>Доставка и оплата</h1>
            <p class="lead">Выберите удобный способ получения при оформлении заказа.</p>
            <div class="info-columns">
                <section>
                    <h2>Самовывоз</h2>
                    <p>Бесплатно при любой сумме заказа.</p>
                </section>
                <section>
                    <h2>Курьерская доставка</h2>
                    <p>390 ₽ для заказов до 10 000 ₽. При сумме товаров от 10 000 ₽ — бесплатно. Для оформления укажите город, улицу, дом и квартиру.</p>
                </section>
                <section>
                    <h2>Оплата при получении</h2>
                    <p>Сайт не запрашивает данные карты. Подтверждение создаёт демонстрационный заказ в личном кабинете.</p>
                </section>
                <section>
                    <h2>История заказов</h2>
                    <p>Состав покупки, цены, способ доставки и общая сумма сохраняются. Посмотреть их можно в разделе «История покупок» после входа в аккаунт.</p>
                </section>
            </div>
        </template>
        <template v-else>
            <h1>Кажется, мы свернули не туда.</h1>
            <p class="lead">Такой страницы нет. Вернёмся на знакомый маршрут?</p>
            <RouterLink to="/" class="button">На главную →</RouterLink>
        </template>
    </div>
</template>

<style scoped>
.info-page {
    max-width: 1100px;
}

.info-page > .eyebrow {
    margin-bottom: 22px;
}

.lead {
    font-size: 19px;
    color: #78816f;
    max-width: 760px;
}

.info-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 35px 60px;
    margin: 50px 0;
}

.info-columns h2 {
    font-size: 24px;
}

.info-columns p {
    font-size: 14px;
}

@media (max-width: 760px) {
    .info-columns {
        grid-template-columns: 1fr;
        gap: 25px;
        margin: 30px 0;
    }

    .lead {
        font-size: 16px;
    }
}
</style>
