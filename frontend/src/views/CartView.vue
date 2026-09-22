<script setup>
import { computed, onMounted, ref } from 'vue';
import { api, money } from '../api';
import { store, removeFromCart } from '../store';
import ProductArt from '../components/ProductArt.vue';
import Icon from '../components/Icon.vue';
const products = ref([]), error = ref(''), loading = ref(true);
const items = computed(() => store.cart.map(item => ({ ...products.value.find(p => p.id === item.id), ...item })));
const total = computed(() => items.value.reduce((sum, p) => sum + (p.price || 0) * p.quantity, 0));
const invalid = computed(() => items.value.some(p => !p.name || p.stock < p.quantity));
async function load() { loading.value = true; error.value = ''; try { products.value = await api('/products'); } catch (e) { error.value = e.message; } finally { loading.value = false; } }
function change(id, value) { const item = store.cart.find(p => p.id === id); item.quantity += value; }
onMounted(load);
</script>

<template>
    <div class="container page">
        <div class="breadcrumb">
            <RouterLink to="/">Главная</RouterLink>
            <span>/</span>
            Корзина
        </div>
        <h1>Ваша корзина<span class="title-count">{{ store.cart.length }}</span></h1>
        <div v-if="error" class="notice error" role="alert">
            {{ error }}
            <button @click="load">Повторить</button>
        </div>
        <div v-else-if="loading" class="loading">Проверяем цены и наличие…</div>
        <div v-else-if="!items.length" class="empty">
            <Icon name="bag"/>
            <h2>Здесь начинается ваша поездка</h2>
            <p>Добавьте в корзину то, что пригодится в пути.</p>
            <RouterLink to="/catalog" class="button">Перейти в каталог <Icon name="arrow"/></RouterLink>
        </div>
        <div v-else class="cart-layout">
            <div>
                <article v-for="p in items" :key="p.id" class="cart-row">
                    <RouterLink :to="`/product/${p.id}`" class="cart-art">
                        <ProductArt :kind="p.image" :color="p.color"/>
                    </RouterLink>
                    <div class="cart-info">
                        <span class="eyebrow">{{ p.brand }}</span>
                        <RouterLink :to="`/product/${p.id}`">
                            <h3>{{ p.name || 'Товар недоступен' }}</h3>
                        </RouterLink>
                        <span>{{ money(p.price || 0) }} / шт.</span>
                        <p v-if="!p.name || p.quantity > p.stock" class="error-text">{{ p.name ? `В наличии только ${p.stock} шт. Уменьшите количество.` : 'Удалите товар из корзины' }}</p>
                    </div>
                    <div class="quantity">
                        <button @click="change(p.id, -1)" :disabled="p.quantity <= 1" :aria-label="`Уменьшить: ${p.name}`">−</button>
                        <span>{{ p.quantity }}</span>
                        <button @click="change(p.id, 1)" :disabled="p.quantity >= p.stock" :aria-label="`Увеличить: ${p.name}`">+</button>
                    </div>
                    <strong>{{ money((p.price || 0) * p.quantity) }}</strong>
                    <button class="icon-button" @click="removeFromCart(p.id)" :aria-label="`Удалить: ${p.name}`"><Icon name="close"/></button>
                </article>
                <RouterLink class="text-link continue" to="/catalog">← Продолжить покупки</RouterLink>
            </div>
            <aside class="summary">
                <span class="eyebrow">ВАШ СЛЕДУЮЩИЙ МАРШРУТ</span>
                <h2>Итого</h2>
                <div>
                    <span>Товары</span>
                    <strong>{{ money(total) }}</strong>
                </div>
                <div>
                    <span>Доставка</span>
                    <span>При оформлении</span>
                </div>
                <div class="summary-total">
                    <span>Сумма</span>
                    <strong>{{ money(total) }}</strong>
                </div>
                <RouterLink v-if="!invalid" to="/checkout" class="button">Оформить заказ <Icon name="arrow"/></RouterLink>
                <p v-else class="error-text">Проверьте наличие товаров в корзине.</p>
                <p class="muted">Самовывоз — бесплатно.<br>Курьер — 390 ₽, бесплатно от 10 000 ₽.</p>
            </aside>
        </div>
    </div>
</template>

<style scoped>
.title-count {
    font-size: 19px;
    background: var(--soft);
    padding: 7px 14px;
    border-radius: 50%;
    vertical-align: middle;
    margin-left: 20px;
    letter-spacing: 0;
}

.cart-layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 330px;
    gap: 40px;
    margin-top: 40px;
}

.cart-row {
    display: flex;
    gap: 18px;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding: 22px 0;
}

.cart-row:first-child {
    padding-top: 0;
}

.cart-art {
    width: 108px;
    flex-shrink: 0;
    background: #eff1e7;
    border-radius: 6px;
}

.cart-info {
    flex: 1;
}

.cart-info h3 {
    font-size: 13px;
    margin: 6px 0;
}

.cart-info > span {
    font-size: 10px;
    color: var(--muted);
}

.cart-row > strong {
    font-size: 13px;
    white-space: nowrap;
}

.icon-button {
    padding: 5px;
    display: inline-flex;
}

.continue {
    margin-top: 25px;
}

@media (max-width: 1100px) {
    .cart-layout {
        grid-template-columns: minmax(0, 1fr) 290px;
        gap: 25px;
    }

    .cart-row {
        gap: 12px;
        flex-wrap: wrap;
    }

    .cart-info {
        min-width: 140px;
    }
}

@media (max-width: 760px) {
    .cart-layout {
        grid-template-columns: 1fr;
        margin-top: 30px;
    }

    .cart-row {
        gap: 13px;
        padding: 20px 0;
    }

    .cart-art {
        width: 88px;
    }

    .cart-info {
        min-width: 130px;
    }

    .cart-row > strong {
        flex: 1;
        text-align: right;
    }

    .cart-row .quantity {
        min-width: 100px;
    }
}
</style>
