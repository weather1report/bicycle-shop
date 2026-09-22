<script setup>
import { onMounted, reactive, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { api, money } from '../api';
import { store, logout, notify } from '../store';
import ProductArt from '../components/ProductArt.vue';
const router = useRouter(), route = useRoute();
const orders = ref([]), error = ref(''), loading = ref(true), busy = ref(false), tab = ref('orders');
const profile = reactive({ name: '', phone: '', address: '' });
async function load() {
    loading.value = true; error.value = '';
    try { store.user = await api('/users/me'); Object.assign(profile, store.user); orders.value = await api('/orders'); }
    catch (e) { if (e.status === 401) router.replace('/login'); else error.value = e.message; }
    finally { loading.value = false; }
}
async function save() { busy.value = true; error.value = ''; try { store.user = await api('/users/me', { method: 'PUT', body: JSON.stringify(profile) }); notify('Данные сохранены'); } catch (e) { error.value = e.message; } finally { busy.value = false; } }
async function exit() { try { await logout(); router.push('/'); } catch (e) { error.value = e.message; } }
onMounted(load);
</script>

<template>
    <div class="container page">
        <div class="breadcrumb">
            <RouterLink to="/">Главная</RouterLink>
            <span>/</span>Личный кабинет
        </div>
        <h1>Здравствуйте{{ store.user ? ', ' + store.user.name : '' }}.</h1>
        <p class="muted">Ваши покупки, планы и новые маршруты.</p>
        <div v-if="route.query.ordered" class="notice success" role="status">Заказ №{{ route.query.ordered }} оформлен! Все подробности — в истории покупок.</div>
        <div v-if="error" class="notice error" role="alert">{{ error }} <button @click="load">Повторить</button></div>
        <div v-if="loading" class="loading">Загружаем личный кабинет…</div>
        <div v-else-if="store.user" class="account-layout">
            <aside class="account-nav">
                <div class="avatar">{{ store.user.name[0].toUpperCase() }}</div>
                <strong>{{ store.user.name }}</strong>
                <span class="muted">{{ store.user.email }}</span>
                <button :class="{ selected: tab === 'orders' }" @click="tab = 'orders'">История покупок <span>{{ orders.length }}</span></button>
                <button :class="{ selected: tab === 'profile' }" @click="tab = 'profile'">Личные данные</button>
                <button @click="exit">Выйти из аккаунта ↗</button>
            </aside>
            <section v-if="tab === 'orders'">
                <h2>История покупок</h2>
                <div v-if="!orders.length" class="empty">
                    <h3>Всё ещё впереди</h3>
                    <p>Здесь будут ваши заказы. Начните с каталога.</p>
                    <RouterLink to="/catalog" class="button">Выбрать товары</RouterLink>
                </div>
                <article v-for="order in orders" :key="order.id" class="order-card">
                    <div class="order-heading">
                        <div>
                            <h3>Заказ №{{ String(order.id).padStart(4, '0') }}</h3>
                            <span class="muted">{{ new Date(order.created_at + 'Z').toLocaleDateString('ru-RU') }}</span>
                        </div>
                        <span class="status-badge">{{ order.status }}</span>
                        <strong>{{ money(order.total) }}</strong>
                    </div>
                    <div v-for="item in order.items" :key="item.id" class="order-product">
                        <div class="order-art"><ProductArt :kind="item.image" :color="item.color"/></div>
                        <RouterLink :to="`/product/${item.product_id}`">{{ item.name }}</RouterLink>
                        <span>{{ item.quantity }} шт.</span>
                        <strong>{{ money(item.price * item.quantity) }}</strong>
                    </div>
                    <div class="order-details">
                        <span>{{ order.delivery === 'pickup' ? 'Самовывоз' : 'Курьерская доставка' }} · {{ money(order.delivery_price) }}</span>
                        <span>{{ order.address }}</span>
                        <span>Получатель: {{ order.name }} · {{ order.phone }}</span>
                        <span>Оплата при получении</span>
                    </div>
                </article>
            </section>
            <section v-else class="profile-section">
                <h2>Личные данные</h2>
                <p class="muted">Сохраним их для быстрого оформления заказа.</p>
                <form @submit.prevent="save">
                    <label>Ваше имя<input v-model.trim="profile.name" required minlength="2" maxlength="80" autocomplete="name"></label>
                    <label>Телефон<input v-model="profile.phone" type="tel" maxlength="25" autocomplete="tel" placeholder="+7 (900) 000-00-00"></label>
                    <label>Адрес доставки<textarea v-model.trim="profile.address" maxlength="250" autocomplete="street-address" placeholder="Город, улица, дом, квартира"></textarea></label>
                    <button class="button" :disabled="busy">{{ busy ? 'Сохраняем…' : 'Сохранить изменения' }}</button>
                </form>
            </section>
        </div>
    </div>
</template>

<style scoped>
.success {
    background: #e7efdb;
}

.account-layout {
    display: grid;
    grid-template-columns: 230px minmax(0, 1fr);
    gap: 60px;
    margin-top: 42px;
}

.account-nav {
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 12px;
}

.avatar {
    border-radius: 50%;
    width: 58px;
    height: 58px;
    display: grid;
    place-items: center;
    background: #e4ebd8;
    font-size: 24px;
}

.account-nav > .muted {
    font-size: 11px;
    overflow-wrap: anywhere;
    margin-bottom: 22px;
}

.account-nav button {
    width: 100%;
    text-align: left;
    padding: 14px;
    border-radius: 5px;
    font-size: 12px;
    display: flex;
    justify-content: space-between;
}

.order-card {
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-bottom: 25px;
}

.order-heading {
    background: #f1f3eb;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    padding: 20px 23px;
}

.order-heading h3 {
    margin-bottom: 6px;
}

.order-heading .muted {
    font-size: 11px;
}

.status-badge {
    background: #dfe9d1;
    font-size: 10px;
    padding: 7px 12px;
    border-radius: 30px;
}

.order-product {
    display: flex;
    align-items: center;
    gap: 18px;
    margin: 0 23px;
    padding: 15px 0;
    font-size: 12px;
    border-bottom: 1px solid var(--border);
}

.order-art {
    width: 75px;
    background: #f2f3ee;
    border-radius: 5px;
}

.order-product a {
    flex: 1;
}

.order-product strong {
    white-space: nowrap;
}

.order-details {
    padding: 20px 23px;
    display: grid;
    gap: 9px;
    font-size: 11px;
    color: var(--muted);
}

.profile-section {
    max-width: 530px;
}

.profile-section .button {
    margin-top: 24px;
}

.profile-section > p {
    font-size: 13px;
}

@media (max-width: 1100px) {
    .account-layout {
        gap: 30px;
    }
}

@media (max-width: 760px) {
    .account-layout {
        grid-template-columns: 1fr;
        gap: 30px;
    }

    .account-nav {
        flex-direction: row;
        flex-wrap: wrap;
        align-items: center;
        gap: 8px;
    }

    .account-nav .avatar, .account-nav > strong, .account-nav > .muted {
        
        display: none;
    }

    .account-nav button {
        width: auto;
        font-size: 10px;
        border: 1px solid var(--border);
        padding: 12px;
        gap: 10px;
    }

    .order-heading {
        gap: 8px;
        padding: 15px;
        flex-wrap: wrap;
    }

    .order-heading h3 {
        font-size: 13px;
    }

    .order-heading > strong {
        font-size: 13px;
    }

    .order-product {
        margin: 0 15px;
        gap: 9px;
        font-size: 10px;
    }

    .order-art {
        width: 45px;
    }

    .order-product > span {
        white-space: nowrap;
    }

    .order-details {
        padding: 15px;
    }
}
</style>
