import { computed, reactive, watch } from 'vue';
import { api } from './api';

function readCart() {
    try {
        const value = JSON.parse(localStorage.getItem('velo-cart') || '[]');
        return Array.isArray(value) ? value.filter(item => Number.isInteger(item.id) && Number.isInteger(item.quantity) && item.quantity > 0).map(item => ({ id: item.id, quantity: Math.min(99, item.quantity) })) : [];
    } catch { return []; }
}

export const store = reactive({ user: null, cart: readCart(), toast: '' });
export const cartCount = computed(() => store.cart.reduce((sum, item) => sum + item.quantity, 0));
let timer;
export function notify(message) {
    store.toast = message;
    clearTimeout(timer);
    timer = setTimeout(() => store.toast = '', 3000);
}
watch(() => store.cart, value => {
    try { localStorage.setItem('velo-cart', JSON.stringify(value)); } catch {  }
}, { deep: true });

export function addToCart(product, quantity = 1) {
    const item = store.cart.find(item => item.id === product.id);
    if ((item?.quantity || 0) + quantity > product.stock) return notify('В корзине уже всё доступное количество');
    if (item) item.quantity += quantity;
    else store.cart.push({ id: product.id, quantity });
    notify('Товар добавлен в корзину');
}
export function removeFromCart(id) { store.cart = store.cart.filter(item => item.id !== id); }
export async function loadUser() {
    try { store.user = await api('/users/me'); }
    catch (error) { if (error.status !== 401) notify(error.message); store.user = null; }
}
export async function logout() {
    await api('/auth/logout', { method: 'POST' });
    store.user = null;
    store.cart = [];
}
