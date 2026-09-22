import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';
import CatalogView from './views/CatalogView.vue';
import ProductView from './views/ProductView.vue';
import CartView from './views/CartView.vue';
import AuthView from './views/AuthView.vue';
import AccountView from './views/AccountView.vue';
import CheckoutView from './views/CheckoutView.vue';
import InfoView from './views/InfoView.vue';

const router = createRouter({
    history: createWebHistory(),
    scrollBehavior: () => ({ top: 0 }),
    routes: [
        { path: '/', component: HomeView, meta: { title: 'Движение начинается здесь' } },
        { path: '/catalog', component: CatalogView, meta: { title: 'Каталог' } },
        { path: '/product/:id', component: ProductView, meta: { title: 'Товар' } },
        { path: '/cart', component: CartView, meta: { title: 'Корзина' } },
        { path: '/login', component: AuthView, meta: { title: 'Вход' } },
        { path: '/register', component: AuthView, meta: { title: 'Регистрация' } },
        { path: '/account', component: AccountView, meta: { title: 'Личный кабинет' } },
        { path: '/checkout', component: CheckoutView, meta: { title: 'Оформление заказа' } },
        { path: '/delivery', component: InfoView, meta: { title: 'Доставка и оплата' } },
        { path: '/about', component: InfoView, meta: { title: 'О магазине' } },
        { path: '/:pathMatch(.*)*', component: InfoView, meta: { title: 'Страница не найдена' } },
    ],
});
router.afterEach(to => document.title = `${to.meta.title} — Вело`);
export default router;
