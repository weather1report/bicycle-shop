<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from '../api';
import ProductCard from '../components/ProductCard.vue';
import Icon from '../components/Icon.vue';
const route = useRoute(), router = useRouter();
const categories = ref([]), products = ref([]), loading = ref(true), error = ref('');
const search = ref(route.query.search || ''), min = ref(''), max = ref('');
let request = 0;
async function load() {
    const current = ++request;
    loading.value = true;
    error.value = '';
    try {
        const params = new URLSearchParams();
        for (const key of ['category', 'search', 'sort', 'min_price', 'max_price']) if (route.query[key]) params.set(key, route.query[key]);
        const data = await api('/products?' + params);
        if (current === request) products.value = data;
    } catch (e) { if (current === request) error.value = e.message; }
    finally { if (current === request) loading.value = false; }
}
function filter(values) { router.push({ path: '/catalog', query: { ...route.query, ...values } }); }
function reset() { search.value = ''; min.value = ''; max.value = ''; router.push('/catalog'); }
watch(() => route.query, () => { search.value = route.query.search || ''; load(); });
onMounted(async () => { load(); try { categories.value = await api('/categories'); } catch (e) { error.value = e.message; } });
</script>
<template>
    <div class="container page">
        <div class="breadcrumb">
            <RouterLink to="/">Главная</RouterLink>
            <span>/</span>
            Каталог
        </div>
        <div class="page-heading">
            <div>
                <span class="eyebrow">ДЛЯ ВАШЕГО СЛЕДУЮЩЕГО МАРШРУТА</span>
                <h1>Каталог</h1>
            </div>
            <p>Хорошая поездка начинается<br>с правильных деталей.</p>
        </div>
        <div class="catalog-layout">
            <aside class="filters">
                <h3>Категории</h3>
                <button :class="{ selected: !route.query.category }" @click="filter({ category: undefined })">Все товары <span>↗</span></button>
                <button v-for="c in categories" :key="c.id" :class="{ selected: Number(route.query.category) === c.id }" @click="filter({ category: c.id })">{{ c.name }}</button>
                <form class="price-filter" @submit.prevent="filter({ min_price: min ? Math.round(min * 100) : undefined, max_price: max ? Math.round(max * 100) : undefined })">
                    <h3>Цена, ₽</h3>
                    <div>
                        <input v-model="min" type="number" min="0" placeholder="От" aria-label="Цена от">
                        <input v-model="max" type="number" :min="min || 0" placeholder="До" aria-label="Цена до">
                    </div>
                    <button class="button secondary">Применить</button>
                </form>
                <button class="reset" @click="reset">Сбросить фильтры</button>
            </aside>
            <section>
                <div class="catalog-toolbar">
                    <form class="search-field" @submit.prevent="filter({ search: search.trim() || undefined })">
                        <input v-model="search" type="search" placeholder="Найти велосипед, шлем, флягу…" aria-label="Поиск по каталогу">
                        <button aria-label="Найти"><Icon name="search"/></button>
                    </form>
                    <select aria-label="Сортировка" :value="route.query.sort || 'popular'" @change="filter({ sort: $event.target.value })">
                        <option value="popular">По умолчанию</option>
                        <option value="price_asc">Сначала дешевле</option>
                        <option value="price_desc">Сначала дороже</option>
                        <option value="new">Сначала новинки</option>
                    </select>
                </div>
                <p class="muted result-count">{{ loading ? 'Загружаем товары…' : `Найдено товаров: ${products.length}` }}</p>
                <div v-if="error" class="notice error" role="alert">
                    {{ error }}
                    <button @click="load">Повторить</button>
                </div>
                <div v-else-if="loading" class="loading">Подбираем товары для вас…</div>
                <div v-else-if="!products.length" class="empty">
                    <h2>Пока ничего не нашлось</h2>
                    <p>Попробуйте другой запрос или сбросьте фильтры.</p>
                    <button class="button" @click="reset">Показать все товары</button>
                </div>
                <div v-else class="product-grid catalog-products">
                    <ProductCard v-for="p in products" :key="p.id" :product="p" />
                </div>
            </section>
        </div>
    </div>
</template>

<style scoped>
.button.secondary {
    background: transparent;
    border: 1px solid #b9c4ae;
    color: var(--green);
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 24px;
}

.page-heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.page-heading .eyebrow {
    margin-bottom: 13px;
    color: var(--muted);
}

.page-heading p {
    font-size: 13px;
    color: var(--muted);
}

.catalog-layout {
    display: grid;
    grid-template-columns: 216px minmax(0, 1fr);
    gap: 39px;
    margin-top: 20px;
}

.filters h3 {
    margin-top: 10px;
}

.filters > button {
    display: flex;
    justify-content: space-between;
    text-align: left;
    width: 100%;
    padding: 13px 12px;
    font-size: 12px;
    border-radius: 5px;
}

.price-filter {
    border-top: 1px solid var(--border);
    margin-top: 24px;
    padding-top: 20px;
}

.price-filter > div {
    display: flex;
    gap: 8px;
}

.price-filter input {
    width: 50%;
    padding: 11px;
    font-size: 12px;
}

.price-filter .button {
    width: 100%;
    margin-top: 12px;
    padding: 10px;
    min-height: 40px;
    font-size: 11px;
}

.filters .reset {
    color: var(--muted);
    justify-content: center;
    text-decoration: underline;
    font-size: 11px;
}

.catalog-toolbar {
    display: flex;
    gap: 15px;
}

.search-field {
    display: flex;
    flex: 1;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: white;
}

.search-field input {
    border: 0;
    flex: 1;
    width: 100%;
    background: transparent;
    font-size: 12px;
}

.search-field button {
    padding: 0 12px;
}

.catalog-toolbar select {
    font-size: 11px;
    max-width: 180px;
}

.catalog-products {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    row-gap: 35px;
}

.result-count {
    font-size: 11px;
    margin: 18px 0 22px;
}

@media (max-width: 1100px) {
    .product-grid {
        gap: 16px;
    }

    .catalog-layout {
        grid-template-columns: 185px minmax(0, 1fr);
        gap: 25px;
    }

    .catalog-products {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 760px) {
    .product-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 26px 13px;
    }

    .page-heading {
        display: block;
    }

    .page-heading > p {
        display: none;
    }

    .catalog-layout {
        grid-template-columns: 1fr;
        gap: 25px;
    }

    .filters {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .filters > h3 {
        display: none;
    }

    .filters > button {
        width: auto;
        border: 1px solid var(--border);
        padding: 9px 10px;
        font-size: 10px;
    }

    .filters > button span {
        display: none;
    }

    .price-filter {
        margin: 5px 0 0;
        padding: 0;
        border: 0;
        width: 100%;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .price-filter h3 {
        display: none;
    }

    .price-filter .button {
        width: auto;
        margin: 0;
    }

    .filters .reset {
        font-size: 10px;
        border: 0;
    }

    .catalog-toolbar {
        gap: 8px;
    }

    .catalog-toolbar select {
        width: 128px;
        padding: 8px 4px;
        font-size: 10px;
    }

    .search-field input {
        padding: 12px;
        font-size: 11px;
    }

    .search-field button {
        padding: 0 8px;
    }
}
</style>
