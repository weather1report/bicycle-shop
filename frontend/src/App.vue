<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import Icon from './components/Icon.vue';
import { store, cartCount, loadUser } from './store';
const menu = ref(false);
const route = useRoute();
watch(() => route.fullPath, () => menu.value = false);
onMounted(loadUser);
</script>
<template>
    <header class="header"><div class="container header-inner">
        <RouterLink to="/" class="logo" aria-label="Вело — главная"><span class="logo-mark">в.</span>вело<span class="logo-dot">®</span></RouterLink>
        <nav :class="{ open: menu }" aria-label="Основная навигация">
            <RouterLink to="/catalog">Каталог</RouterLink>
            <RouterLink to="/about">О магазине</RouterLink>
            <RouterLink to="/delivery">Доставка и оплата</RouterLink>
        </nav>
        <div class="header-actions">
            <RouterLink to="/catalog" aria-label="Поиск товаров"><Icon name="search" /></RouterLink>
            <RouterLink :to="store.user ? '/account' : '/login'" aria-label="Личный кабинет">
                <Icon name="user" /><span>{{ store.user ? store.user.name.split(' ')[0] : 'Войти' }}</span>
            </RouterLink>
            <RouterLink to="/cart" aria-label="Корзина"><Icon name="bag" /><span class="cart-count">{{ cartCount }}</span></RouterLink>
            <button class="menu-toggle" @click="menu = !menu" aria-label="Открыть меню" :aria-expanded="menu"><Icon name="menu" /></button>
        </div>
    </div></header>
    <main><RouterView /></main>
    <footer>
        <div class="container footer-top">
            <div>
                <RouterLink to="/" class="logo">вело<span class="logo-dot">®</span></RouterLink>
                <p>Для тех, кто выбирает движение.<br>Каждый день. В своём ритме.</p>
            </div>
            <div><h3>Магазин</h3><RouterLink to="/catalog">Каталог товаров</RouterLink><RouterLink to="/about">О проекте</RouterLink></div>
            <div><h3>Покупателям</h3><RouterLink to="/delivery">Доставка и оплата</RouterLink><RouterLink to="/account">Личный кабинет</RouterLink></div>
            <div class="footer-note"><span class="eyebrow">ЕЩЁ ОДИН ПОВОД ВЫЙТИ НА УЛИЦУ</span><p>Ваш следующий<br>маршрут начинается здесь. ↗</p></div>
        </div>
    </footer>
    <Transition name="toast"><div v-if="store.toast" class="toast" role="status"><Icon name="check" />{{ store.toast }}</div></Transition>
</template>

<style scoped>
.header {
    border-bottom: 1px solid var(--border);
    background: #ffffff;
}

.header-inner {
    height: 91px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 25px;
}

.logo {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -2px;
    display: inline-flex;
    align-items: center;
    gap: 11px;
}

.logo-mark {
    color: white;
    background: var(--green);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    font-size: 27px;
    display: grid;
    place-items: center;
    line-height: 1;
}

.logo-dot {
    font-size: 12px;
    align-self: start;
    margin-top: 9px;
    letter-spacing: 0;
}

nav {
    display: flex;
    gap: 34px;
    font-size: 13px;
}

nav .router-link-active {
    color: #6b7e57;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 24px;
    font-size: 12px;
}

.header-actions a {
    display: flex;
    gap: 9px;
    align-items: center;
}

.cart-count {
    border-radius: 50%;
    background: var(--soft);
    width: 23px;
    height: 23px;
    display: grid;
    place-items: center;
}

.menu-toggle {
    display: none;
}

footer {
    background: #edf0e6;
    padding-top: 43px;
}

.footer-top {
    display: grid;
    grid-template-columns: 1.15fr .7fr 1fr 1fr;
    gap: 35px;
    padding-bottom: 40px;
}

.footer-top p {
    font-size: 11px;
    color: #7b8473;
    margin-top: 15px;
}

.footer-top h3 {
    font-size: 11px;
    margin: 13px 0 20px;
}

.footer-top > div > a:not(.logo) {
    display: block;
    font-size: 11px;
    margin-top: 12px;
}

.footer-note .eyebrow {
    font-size: 8px;
    letter-spacing: 1px;
    margin-top: 15px;
}

.footer-note p {
    font-size: 16px;
    color: var(--green);
    line-height: 1.5;
}

.toast {
    position: fixed;
    bottom: 28px;
    left: 50%;
    transform: translateX(-50%);
    background: #2d4939;
    color: white;
    padding: 17px 25px;
    border-radius: 9px;
    box-shadow: 0 8px 40px #223c3025;
    display: flex;
    align-items: center;
    gap: 13px;
    font-size: 13px;
    z-index: 10;
    max-width: 90vw;
    width: max-content;
}

.toast-enter-active, .toast-leave-active {
    transition: opacity .2s;
}

.toast-enter-from, .toast-leave-to {
    opacity: 0;
}

@media (max-width: 1100px) {
    nav {
        gap: 20px;
    }

    .header-actions {
        gap: 16px;
    }
}

@media (max-width: 760px) {
    .header-inner {
        height: 74px;
        gap: 10px;
    }

    .logo {
        font-size: 29px;
    }

    .logo-mark {
        width: 30px;
        height: 30px;
        font-size: 22px;
    }

    .header-actions {
        gap: 16px;
    }

    .header-actions a > span:not(.cart-count) {
        display: none;
    }

    .header-actions > a:first-child {
        display: none;
    }

    .menu-toggle {
        display: flex;
        padding: 0;
    }

    nav {
        display: none;
        position: absolute;
        top: 102px;
        left: 0;
        right: 0;
        background: #ffffff;
        padding: 25px;
        border-bottom: 1px solid var(--border);
        z-index: 5;
    }

    nav.open {
        display: flex;
        flex-direction: column;
    }

    .footer-top {
        grid-template-columns: 1fr 1fr;
        gap: 25px;
    }

    .footer-top > div:first-child {
        grid-column: span 2;
    }

    .footer-note {
        display: none;
    }
}
</style>
