<script setup>
import ProductArt from './ProductArt.vue';
import Icon from './Icon.vue';
import { money } from '../api';
import { addToCart } from '../store';
defineProps({ product: Object });
</script>
<template>
    <article class="product-card">
        <RouterLink :to="`/product/${product.id}`" class="product-picture" :aria-label="product.name">
            <span v-if="product.badge" class="badge">{{ product.badge }}</span>
            <ProductArt :kind="product.image" :color="product.color" />
            <span class="picture-arrow">↗</span>
        </RouterLink>
        <div class="product-caption"><span class="eyebrow">{{ product.brand }}</span><span class="stock">{{ product.stock ? 'В наличии' : 'Нет в наличии' }}</span></div>
        <RouterLink :to="`/product/${product.id}`" class="product-name">{{ product.name }}</RouterLink>
        <div class="product-bottom"><div><strong>{{ money(product.price) }}</strong></div><button class="add-button" :disabled="!product.stock" @click="addToCart(product)" :aria-label="`В корзину: ${product.name}`"><Icon name="bag" /></button></div>
    </article>
</template>

<style scoped>
.product-picture {
    display: block;
    border-radius: 8px;
    background: #f2f3ed;
    position: relative;
    overflow: hidden;
    padding: 26px 8px 15px;
}

.product-picture .product-art {
    height: 189px;
    transition: transform .3s;
}

.product-picture:hover .product-art {
    transform: scale(1.06);
}

.picture-arrow {
    position: absolute;
    right: 14px;
    bottom: 9px;
    color: #6a7860;
}

.product-caption {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    margin-top: 17px;
}

.product-caption .eyebrow {
    font-size: 9px;
    color: var(--muted);
}

.product-name {
    font-size: 14px;
    display: block;
    font-weight: 600;
    margin: 9px 0 15px;
}

.product-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.product-bottom strong {
    font-size: 16px;
}

.add-button {
    border: 1px solid #dce2d3;
    border-radius: 6px;
    padding: 9px;
    display: flex;
}

.add-button:hover {
    background: #dfe7d4;
}

@media (max-width: 1100px) {
    .product-picture .product-art {
        height: 150px;
    }
}

@media (max-width: 760px) {
    .product-picture {
        padding: 32px 0 12px;
    }

    .product-picture .product-art {
        height: 115px;
    }

    .product-name {
        font-size: 12px;
        min-height: 32px;
    }

    .product-caption {
        flex-wrap: wrap;
        margin-top: 12px;
        gap: 5px;
    }

    .product-bottom strong {
        font-size: 13px;
    }

    .add-button {
        padding: 7px;
    }

    .add-button svg {
        width: 17px;
        height: 17px;
    }
}
</style>
