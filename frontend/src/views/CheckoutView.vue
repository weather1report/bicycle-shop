<script setup>
import { computed, onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { api, money } from '../api';
import { store } from '../store';
const router = useRouter(), products = ref([]), loading = ref(true), error = ref(''), busy = ref(false);
const form = reactive({ name: '', phone: '', address: '', delivery: 'pickup' });
const requestId = crypto.randomUUID();
const items = computed(() => store.cart.map(item => ({ ...products.value.find(p => p.id === item.id), ...item })));
const subtotal = computed(() => items.value.reduce((sum, p) => sum + (p.price || 0) * p.quantity, 0));
const delivery = computed(() => form.delivery === 'pickup' || subtotal.value >= 1000000 ? 0 : 39000);
const invalid = computed(() => !items.value.length || items.value.some(p => !p.name || p.quantity > p.stock));
async function load() {
    loading.value = true; error.value = '';
    try {
        store.user = await api('/users/me');
        Object.assign(form, { name: store.user.name, phone: store.user.phone, address: store.user.address });
        products.value = await api('/products');
    } catch (e) { if (e.status === 401) router.replace('/login?redirect=/checkout'); else error.value = e.message; }
    finally { loading.value = false; }
}
async function submit() {
    busy.value = true; error.value = '';
    try {
        const order = await api('/orders', { method: 'POST', body: JSON.stringify({ ...form, request_id: requestId, items: store.cart.map(p => ({ product_id: p.id, quantity: p.quantity })) }) });
        store.cart = [];
        router.replace('/account?ordered=' + order.id);
    } catch (e) { error.value = e.message; if (e.status === 401) router.push('/login?redirect=/checkout'); }
    finally { busy.value = false; }
}
onMounted(load);
</script>

<template>
    <div class="container page">
        <div class="breadcrumb">
            <RouterLink to="/cart">Корзина</RouterLink>
            <span>/</span>
            Оформление
        </div>
        <h1>Почти в пути.</h1>
        <p class="muted">Осталось выбрать, как получить ваш заказ.</p>
        <div v-if="loading" class="loading">Подготавливаем заказ…</div>
        <div v-else-if="invalid" class="empty">
            <h2>Проверьте корзину</h2>
            <p>{{ error || 'Корзина пуста или количество товара превышает остаток.' }}</p>
            <RouterLink to="/cart" class="button">В корзину</RouterLink>
        </div>
        <form v-else class="checkout-layout" @submit.prevent="submit">
            <div class="checkout-fields">
                <h2><span class="step">01</span>Получатель</h2>
                <div class="two-fields">
                    <label>Имя<input v-model.trim="form.name" required minlength="2" maxlength="80" autocomplete="name"></label>
                    <label>Телефон<input v-model="form.phone" required type="tel" minlength="10" maxlength="25" autocomplete="tel" placeholder="+7 (900) 000-00-00"></label>
                </div>
                <h2><span class="step">02</span>Способ получения</h2>
                <div class="delivery-options">
                    <label :class="{ chosen: form.delivery === 'pickup' }">
                        <input v-model="form.delivery" type="radio" value="pickup">
                        <span><strong>Самовывоз</strong><small>Из пункта «Вело» · бесплатно</small></span>
                    </label>
                    <label :class="{ chosen: form.delivery === 'courier' }">
                        <input v-model="form.delivery" type="radio" value="courier">
                        <span><strong>Курьером</strong><small>390 ₽ · бесплатно от 10 000 ₽</small></span>
                    </label>
                </div>
                <label v-if="form.delivery === 'courier'">Адрес доставки<textarea v-model.trim="form.address" required minlength="8" maxlength="250" autocomplete="street-address" placeholder="Город, улица, дом, квартира"></textarea></label>
                <h2><span class="step">03</span>Оплата</h2>
            </div>
            <aside class="summary">
                <h2>Ваш заказ</h2>
                <div v-for="p in items" :key="p.id">
                    <span>{{ p.name }} × {{ p.quantity }}</span>
                    <strong>{{ money(p.price * p.quantity) }}</strong>
                </div>
                <div>
                    <span>Доставка</span>
                    <strong>{{ delivery ? money(delivery) : 'Бесплатно' }}</strong>
                </div>
                <div class="summary-total">
                    <span>Итого</span>
                    <strong>{{ money(subtotal + delivery) }}</strong>
                </div>
                <div v-if="error" class="notice error" role="alert">{{ error }}</div>
                <button class="button" :disabled="busy">{{ busy ? 'Оформляем…' : 'Подтвердить заказ' }}</button>
            </aside>
        </form>
    </div>
</template>

<style scoped>
.checkout-layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 330px;
    gap: 40px;
    margin-top: 40px;
}

.checkout-fields h2 {
    margin: 30px 0 24px;
    font-size: 23px;
    display: flex;
    align-items: center;
    gap: 15px;
}

.checkout-fields h2:first-child {
    margin-top: 0;
}

.step {
    font-size: 11px;
    background: #ebefdf;
    border-radius: 50%;
    width: 34px;
    height: 34px;
    display: grid;
    place-items: center;
    letter-spacing: 0;
}

.two-fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.two-fields label + label {
    margin-top: 0;
}

.delivery-options {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-bottom: 25px;
}

.delivery-options label {
    flex-direction: row;
    gap: 14px;
    border: 1px solid var(--border);
    padding: 20px 15px;
    border-radius: 6px;
    align-items: center;
    margin: 0;
    cursor: pointer;
}

.delivery-options .chosen {
    background: #eff3e7;
    border-color: #8b9b78;
}

.delivery-options small {
    display: block;
    font-size: 10px;
    font-weight: 400;
    color: var(--muted);
    margin-top: 6px;
}

@media (max-width: 1100px) {
    .checkout-layout {
        grid-template-columns: minmax(0, 1fr) 290px;
        gap: 25px;
    }
}

@media (max-width: 760px) {
    .checkout-layout {
        grid-template-columns: 1fr;
        margin-top: 30px;
    }

    .two-fields, .delivery-options {
        grid-template-columns: 1fr;
    }

    .delivery-options label {
        padding: 18px;
    }
}
</style>
