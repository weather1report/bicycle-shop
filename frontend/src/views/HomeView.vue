<script setup>
import { onMounted, ref } from 'vue';
import { api } from '../api';
import ProductArt from '../components/ProductArt.vue';
import Icon from '../components/Icon.vue';
const categories = ref([]), error = ref('');
async function load() {
    error.value = '';
    try { categories.value = await api('/categories'); }
    catch (e) { error.value = e.message; }
}
onMounted(load);
const kinds = ['bike', 'pedal', 'bottle', 'helmet', 'light'];
</script>
<template>
    <div class="container">
        <section class="hero">
            <div class="hero-copy">
                <span class="eyebrow">ВЕЛОСИПЕДЫ И НЕ ТОЛЬКО</span>
                <h1>Навстречу<br>новым<br><em>маршрутам.</em></h1>
                <p>Велосипеды, экипировка и полезные детали.<br>Всё для движения в вашем ритме.</p>
                <RouterLink to="/catalog" class="button">Выбрать свой маршрут <Icon name="arrow" /></RouterLink>
                <div class="hero-bottom">
                    <span class="small-line"></span>
                    ГОРОД · ПРИРОДА · СВОБОДА
                </div>
            </div>
            <div class="hero-visual">
                <div class="hero-circle"></div>
                <span class="hero-number">01 / 03</span>
                <span class="hero-watermark">ride.</span>
                <ProductArt kind="bike" color="#7d8c70"/>
                <div class="hero-product">
                    <span>БОЛЬШЕ, ЧЕМ ПРОСТО ВЕЛОСИПЕД</span>
                    <strong>VELO Trail 29</strong>
                    <RouterLink to="/product/1" aria-label="Посмотреть VELO Trail 29">↗</RouterLink>
                </div>
                <span class="hero-caption">Найдите свою дорогу.</span>
            </div>
        </section>
        <section class="benefits">
            <div>
                <Icon name="truck"/>
                <span><strong>Доставка по России</strong><small>Бесплатно при заказе от 10 000 ₽</small></span>
            </div>
            <div>
                <Icon name="shield"/>
                <span><strong>Внимание к деталям</strong><small>Характеристики для осознанного выбора</small></span>
            </div>
            <div>
                <Icon name="bag"/>
                <span><strong>Всё для вашей поездки</strong><small>От первого велосипеда до новой фляги</small></span>
            </div>
        </section>
        <div v-if="error" class="notice error" role="alert">
            {{ error }}
            <button @click="load">Повторить</button>
        </div>
        <section class="section">
            <div class="section-heading">
                <div>
                    <span class="eyebrow">СОБЕРИТЕ СВОЙ МАРШРУТ</span>
                    <h2>Что нужно для поездки?</h2>
                </div>
                <RouterLink to="/catalog" class="text-link">Весь каталог <Icon name="arrow"/></RouterLink>
            </div>
            <div class="category-grid">
                <RouterLink v-for="(category, index) in categories" :key="category.id" :to="{ path: '/catalog', query: { category: category.id } }" class="category-card">
                    <ProductArt :kind="kinds[index]" :color="index % 2 ? '#b3a388' : '#7b8976'"/>
                    <span>{{ category.name }} <span>↗</span></span>
                </RouterLink>
            </div>
        </section>
        <section class="story-banner">
            <div>
                <span class="eyebrow">НЕ ВАЖНО, СКОЛЬКО КИЛОМЕТРОВ</span>
                <h2>Главное —<br>получать удовольствие.</h2>
                <p>Первая поездка по городу или выходные за его пределами.<br>Мы поможем собраться в путь.</p>
                <RouterLink to="/about" class="text-link">Знакомство с «Вело» <Icon name="arrow"/></RouterLink>
            </div>
            <div class="story-art">
                <span>ВЫБИРАЙТЕ</span>
                <strong>свой<br><em>ритм.</em></strong>
                <span>И ПРОСТО КРУТИТЕ ПЕДАЛИ ↗</span>
            </div>
        </section>
    </div>
</template>

<style scoped>
.hero {
    display: grid;
    grid-template-columns: 43% 57%;
    background: #e9eddf;
    margin-top: 30px;
    min-height: 560px;
    border-radius: 12px;
    overflow: hidden;
}

.hero-copy {
    padding: 49px 0 32px 44px;
    position: relative;
    z-index: 1;
}

.hero h1 {
    font-size: clamp(46px, 5vw, 68px);
    letter-spacing: -3px;
    margin: 23px 0;
    line-height: 1.04;
}

.hero h1 em {
    color: #6c805e;
    font-size: 1.09em;
}

.hero p {
    font-size: 13px;
    color: #687264;
    line-height: 1.85;
    margin-bottom: 26px;
}

.hero-bottom {
    font-size: 9px;
    letter-spacing: 1.7px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 35px;
    color: #75816c;
}

.small-line {
    width: 28px;
    height: 1px;
    background: #859378;
}

.hero-visual {
    position: relative;
    display: flex;
    align-items: center;
    overflow: hidden;
}

.hero-circle {
    width: 540px;
    height: 540px;
    border-radius: 50%;
    background: #dbe2cc;
    position: absolute;
    left: 4%;
    top: 7%;
}

.hero-watermark {
    position: absolute;
    top: 74px;
    left: 85px;
    font-size: 150px;
    letter-spacing: -10px;
    font-weight: 800;
    color: #c6d0b6;
}

.hero-visual > .product-art {
    position: relative;
    width: 110%;
    max-width: none;
    transform: translate(-6%, 18px) rotate(-7deg);
    filter: drop-shadow(0 14px 6px #85916f24);
}

.hero-number {
    position: absolute;
    right: 28px;
    top: 25px;
    font-size: 10px;
    letter-spacing: 2px;
}

.hero-product {
    position: absolute;
    bottom: 41px;
    left: 26px;
    right: 52px;
    border-top: 1px solid #bac5aa;
    padding-top: 17px;
    display: grid;
    grid-template-columns: 1fr 34px;
    gap: 8px;
}

.hero-product > span {
    font-size: 8px;
    letter-spacing: 1.4px;
    color: #74816a;
}

.hero-product strong {
    font-size: 15px;
    grid-row: 2;
}

.hero-product a {
    grid-column: 2;
    grid-row: 1 / 3;
    font-size: 27px;
    align-self: center;
}

.hero-caption {
    position: absolute;
    right: -32px;
    top: 50%;
    transform: rotate(-90deg);
    font-size: 9px;
    letter-spacing: 1.5px;
}

.benefits {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    border-bottom: 1px solid var(--border);
    padding: 28px 0;
}

.benefits > div {
    display: flex;
    gap: 17px;
    align-items: center;
    justify-content: center;
    border-right: 1px solid var(--border);
}

.benefits > div:last-child {
    border: 0;
}

.benefits svg {
    width: 27px;
    height: 27px;
}

.benefits strong {
    display: block;
    font-size: 12px;
    font-weight: 600;
}

.benefits small {
    display: block;
    font-size: 10px;
    color: var(--muted);
    margin-top: 6px;
}

.section {
    margin-top: 60px;
}

.section-heading {
    display: flex;
    align-items: end;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 25px;
}

.section-heading h2 {
    margin: 10px 0 0;
}

.section-heading .eyebrow {
    color: var(--muted);
    font-size: 9px;
}

.category-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
}

.category-card {
    background: #f0f1e9;
    padding: 10px 16px 20px;
    border-radius: 8px;
}

.category-card:nth-child(even) {
    background: #f2eee5;
}

.category-card:hover {
    background: #e4e9d9;
    transform: translateY(-3px);
}

.category-card > span {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 600;
}

.category-card .product-art {
    height: 132px;
}

.story-banner {
    margin: 65px 0;
    padding: 40px 48px;
    border-radius: 10px;
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    background: #eeeade;
}

.story-banner h2 {
    font-size: 36px;
    margin: 20px 0;
}

.story-banner p {
    font-size: 12px;
    color: #7b7f70;
}

.story-art {
    border-left: 1px solid #d6d5c5;
    padding-left: 75px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.story-art span {
    font-size: 9px;
    letter-spacing: 2px;
}

.story-art strong {
    font-size: 69px;
    line-height: .95;
    letter-spacing: -3px;
    font-weight: 500;
    margin: 12px 0 20px;
}

.story-art strong em {
    color: #88916f;
}

.hero-copy, .hero-visual {
    min-width: 0;
}

@media (min-width: 1550px) {
    .hero {
        min-height: 590px;
    }

    .hero-copy {
        padding-top: 60px;
    }
}

@media (max-width: 1100px) {
    .hero {
        min-height: 520px;
    }

    .hero-copy {
        padding-left: 30px;
    }

    .hero h1 {
        font-size: 55px;
    }

    .hero-circle {
        left: -15%;
    }

    .category-card {
        padding: 8px 12px 17px;
    }

    .category-card > span {
        font-size: 10px;
    }
}

@media (max-width: 760px) {
    .hero {
        grid-template-columns: 1fr;
        margin-top: 20px;
        min-height: 0;
    }

    .hero-copy {
        padding: 32px 25px 0;
    }

    .hero h1 {
        font-size: 52px;
    }

    .hero p {
        font-size: 12px;
    }

    .hero-bottom {
        margin-top: 22px;
    }

    .hero-visual {
        height: 320px;
    }

    .hero-circle {
        width: 330px;
        height: 330px;
        left: 10%;
        top: 4%;
    }

    .hero-watermark {
        font-size: 110px;
        left: 55px;
        top: 12px;
    }

    .hero-visual > .product-art {
        width: 100%;
        transform: translateY(-13px) rotate(-7deg);
        height: 290px;
    }

    .hero-product {
        bottom: 19px;
        right: 25px;
        left: 25px;
    }

    .hero-caption {
        display: none;
    }

    .hero-number {
        top: 5px;
        font-size: 8px;
    }

    .benefits {
        grid-template-columns: 1fr;
        padding: 23px 0;
        gap: 23px;
    }

    .benefits > div {
        justify-content: start;
        border: 0;
        padding-left: 10px;
    }

    .benefits small {
        font-size: 11px;
    }

    .section {
        margin-top: 40px;
    }

    .section-heading {
        align-items: center;
    }

    .section-heading .eyebrow {
        font-size: 8px;
        letter-spacing: 1px;
    }

    .section-heading .text-link {
        font-size: 10px;
        gap: 5px;
        white-space: nowrap;
    }

    .section-heading .text-link svg {
        width: 16px;
    }

    .section-heading h2 {
        font-size: 24px;
    }

    .category-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
    }

    .category-card:last-child {
        grid-column: span 2;
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 0 18px 0 0;
    }

    .category-card:last-child .product-art {
        width: 45%;
        height: 110px;
    }

    .category-card:last-child > span {
        flex: 1;
    }

    .category-card > span {
        font-size: 12px;
    }

    .category-card .product-art {
        height: 120px;
    }

    .story-banner {
        margin: 45px 0;
        padding: 30px 25px;
        grid-template-columns: 1fr;
    }

    .story-banner h2 {
        font-size: 29px;
    }

    .story-art {
        margin-top: 25px;
        padding: 25px 0 0;
        border-left: 0;
        border-top: 1px solid #d6d5c5;
    }

    .story-art strong {
        font-size: 55px;
    }
}

@media (max-width: 760px) {
    .hero {
        grid-template-columns: minmax(0, 1fr);
    }

    .hero h1 {
        font-size: clamp(34px, 10.5vw, 52px);
        letter-spacing: -2px;
    }
}
</style>
