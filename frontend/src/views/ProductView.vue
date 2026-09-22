<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { api, money } from '../api';
import { addToCart } from '../store';
import ProductArt from '../components/ProductArt.vue';
import Icon from '../components/Icon.vue';
const route = useRoute(), product = ref(null), error = ref(''), quantity = ref(1);
async function load() {
    product.value = null; error.value = ''; quantity.value = 1;
    try { product.value = await api('/products/' + route.params.id); document.title = product.value.name + ' — Вело'; }
    catch (e) { error.value = e.message; }
}
watch(() => route.params.id, load, { immediate: true });
</script>

<template>
    <div class="container page">
        <div class="breadcrumb">
            <RouterLink to="/">Главная</RouterLink>
            <span>/</span>
            <RouterLink to="/catalog">Каталог</RouterLink>
            <span>/</span>
            {{ product?.name || 'Товар' }}
        </div>
        <div v-if="error" class="empty">
            <h1>{{ error }}</h1>
            <RouterLink class="button" to="/catalog">Вернуться в каталог</RouterLink>
        </div>
        <div v-else-if="!product" class="loading">Загружаем товар…</div>
        <template v-else>
            <div class="product-detail">
                <div class="detail-art">
                    <span class="badge">{{ product.badge || product.brand }}</span>
                    <ProductArt :kind="product.image" :color="product.color"/>
                    <span class="art-note">Иллюстрация модели · {{ product.brand }}</span>
                </div>
                <div class="detail-copy">
                    <span class="eyebrow">{{ product.brand }} / АРТИКУЛ V-{{ String(product.id).padStart(4, '0') }}</span>
                    <h1>{{ product.name }}</h1>
                    <span class="stock">{{ product.stock ? `В наличии: ${product.stock} шт.` : 'Нет в наличии' }}</span>
                    <p>{{ product.description }}</p>
                    <div class="detail-price">
                        <strong>{{ money(product.price) }}</strong>
                    </div>
                    <div class="buy-row">
                        <div class="quantity">
                            <button :disabled="quantity <= 1" @click="quantity--" aria-label="Уменьшить количество">−</button>
                            <span>{{ quantity }}</span>
                            <button :disabled="quantity >= product.stock" @click="quantity++" aria-label="Увеличить количество">+</button>
                        </div>
                        <button class="button" :disabled="!product.stock" @click="addToCart(product, quantity)">Добавить в корзину <Icon name="bag"/></button>
                    </div>
                    <div class="detail-delivery">
                        <Icon name="truck"/>
                        <div>
                            Курьером или самовывозом
                            <small>Доставка бесплатно от 10 000 ₽</small>
                        </div>
                    </div>
                    <RouterLink to="/delivery" class="text-link">Условия доставки и оплаты ↗</RouterLink>
                </div>
            </div>
            <section class="specifications">
                <h2>Всё в деталях</h2>
                <dl>
                    <div v-for="a in product.attributes" :key="a.id">
                        <dt>{{ a.name }}</dt>
                        <dd>{{ a.value }}</dd>
                    </div>
                    <div>
                        <dt>Бренд</dt>
                        <dd>{{ product.brand }}</dd>
                    </div>
                </dl>
            </section>
        </template>
    </div>
</template>

<style scoped>
.product-detail {
    display: grid;
    grid-template-columns: 1.15fr 1fr;
    gap: 65px;
}

.detail-art {
    background: #eef1e5;
    position: relative;
    border-radius: 10px;
    display: flex;
    align-items: center;
    min-height: 480px;
}

.detail-art .product-art {
    padding: 12px;
}

.detail-art .badge {
    top: 24px;
    left: 24px;
}

.art-note {
    position: absolute;
    bottom: 24px;
    left: 24px;
    font-size: 10px;
    color: var(--muted);
}

.detail-copy {
    padding: 20px 0;
}

.detail-copy h1 {
    margin: 18px 0;
    font-size: 40px;
}

.detail-copy > p {
    margin: 25px 0;
    font-size: 13px;
    color: var(--muted);
}

.detail-price {
    margin: 27px 0;
}

.detail-price strong {
    font-size: 32px;
}

.buy-row {
    display: flex;
    gap: 12px;
}

.detail-delivery {
    border-top: 1px solid var(--border);
    margin: 30px 0 15px;
    padding-top: 22px;
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 12px;
}

.detail-delivery small {
    display: block;
    color: var(--muted);
    margin-top: 6px;
}

.specifications {
    margin-top: 60px;
    max-width: 740px;
}

dl > div {
    display: flex;
    justify-content: space-between;
    gap: 25px;
    padding: 17px 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
}

dt {
    color: var(--muted);
}

dd {
    margin: 0;
    text-align: right;
}

@media (max-width: 1100px) {
    .product-detail {
        gap: 35px;
    }

    .buy-row {
        flex-wrap: wrap;
    }

    .detail-art {
        min-height: 420px;
    }
}

@media (max-width: 760px) {
    .product-detail {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .detail-art {
        min-height: 300px;
    }

    .detail-copy h1 {
        font-size: 33px;
    }

    .detail-copy {
        padding-top: 10px;
    }

    .buy-row {
        flex-wrap: nowrap;
    }

    .buy-row .button {
        padding: 13px 16px;
        font-size: 12px;
        gap: 10px;
        flex: 1;
    }

    .specifications {
        margin-top: 30px;
    }
}
</style>
