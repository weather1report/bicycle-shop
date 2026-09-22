<script setup>
import { computed, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from '../api';
import { store } from '../store';
import Icon from '../components/Icon.vue';
const route = useRoute(), router = useRouter();
const register = computed(() => route.path === '/register');
const name = ref(''), email = ref(''), password = ref(''), error = ref(''), busy = ref(false);
watch(() => route.path, () => { error.value = ''; password.value = ''; });
async function submit() {
    busy.value = true; error.value = '';
    try {
        store.user = await api(register.value ? '/auth/register' : '/auth/login', { method: 'POST', body: JSON.stringify({ name: name.value, email: email.value, password: password.value }) });
        router.push(route.query.redirect === '/checkout' ? '/checkout' : '/account');
    } catch (e) { error.value = e.message; } finally { busy.value = false; }
}
</script>
<template>
    <div class="container page auth-layout">
        <div class="auth-story">
            <span class="eyebrow">ВАШ ЛИЧНЫЙ МАРШРУТ</span>
            <h1>Рады видеть<br>вас <em>в седле.</em></h1>
            <p>Все покупки в одном месте.<br>Сохранённые данные для следующей поездки.</p>
            <span class="auth-graphic">в.</span>
        </div>
        <section class="auth-card">
            <span class="eyebrow">ЛИЧНЫЙ КАБИНЕТ</span>
            <h2>{{ register ? 'Давайте знакомиться' : 'С возвращением' }}</h2>
            <p class="muted">{{ register ? 'Создайте аккаунт, чтобы оформить первый заказ.' : 'Войдите, чтобы продолжить свой маршрут.' }}</p>
            <form @submit.prevent="submit">
                <label v-if="register">Ваше имя<input v-model.trim="name" required minlength="2" maxlength="80" autocomplete="name" placeholder="Как к вам обращаться"></label>
                <label>Электронная почта<input v-model.trim="email" type="email" required autocomplete="email" placeholder="you@example.ru"></label>
                <label>Пароль<input v-model="password" type="password" required :minlength="register ? 8 : 1" maxlength="128" :autocomplete="register ? 'new-password' : 'current-password'" :placeholder="register ? 'Не менее 8 символов' : 'Введите пароль'"></label>
                <div v-if="error" class="notice error" role="alert">{{ error }}</div>
                <button class="button" :disabled="busy">{{ busy ? 'Подождите…' : register ? 'Создать аккаунт' : 'Войти' }}<Icon name="arrow"/></button>
            </form>
            <p class="auth-switch">{{ register ? 'Уже есть аккаунт?' : 'Впервые у нас?' }} <RouterLink :to="{ path: register ? '/login' : '/register', query: route.query }">{{ register ? 'Войти' : 'Зарегистрироваться' }}</RouterLink></p>
            <p class="muted small">Учебный магазин. Используйте тестовые данные для знакомства с проектом.</p>
        </section>
    </div>
</template>

<style scoped>
.auth-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 100px;
    padding-top: 65px;
    padding-bottom: 80px;
}

.auth-story {
    background: #e9eedf;
    border-radius: 10px;
    padding: 50px 40px;
    overflow: hidden;
    position: relative;
    min-height: 550px;
}

.auth-story h1 {
    margin: 25px 0;
    font-size: 50px;
}

.auth-story p {
    font-size: 13px;
    color: var(--muted);
}

.auth-graphic {
    font-size: 290px;
    font-weight: 800;
    color: #cad6bb;
    position: absolute;
    bottom: -82px;
    right: 12px;
    letter-spacing: -25px;
    transform: rotate(-12deg);
}

.auth-card {
    padding: 30px 25px 10px 0;
}

.auth-card h2 {
    margin: 18px 0 12px;
}

.auth-card > p {
    font-size: 12px;
}

.auth-card form {
    margin-top: 30px;
}

.auth-card .button {
    width: 100%;
    margin-top: 27px;
}

.auth-switch {
    text-align: center;
    margin-top: 22px;
}

.auth-switch a {
    text-decoration: underline;
    font-weight: 700;
}

@media (max-width: 1100px) {
    .auth-layout {
        gap: 45px;
    }
}

@media (max-width: 760px) {
    .auth-layout {
        grid-template-columns: 1fr;
        gap: 26px;
    }

    .auth-story {
        min-height: 210px;
        padding: 25px;
    }

    .auth-story h1 {
        font-size: 34px;
        position: relative;
        z-index: 1;
        margin: 18px 0 0;
    }

    .auth-story p {
        display: none;
    }

    .auth-graphic {
        font-size: 200px;
        bottom: -68px;
        right: 10px;
    }

    .auth-card {
        padding: 0;
    }

    .auth-card > .eyebrow {
        display: none;
    }
}

@media (max-width: 760px) {
    .auth-layout {
        padding-top: 22px;
        padding-bottom: 45px;
    }
}
</style>
