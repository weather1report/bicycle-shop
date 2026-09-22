export async function api(path, options = {}) {
    let response;
    try {
        response = await fetch('/api' + path, {
            credentials: 'same-origin',
            ...options,
            headers: { 'Content-Type': 'application/json', ...options.headers },
        });
    } catch {
        throw new Error('Не удалось связаться с сервером. Проверьте подключение и попробуйте снова.');
    }
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        let message = data.detail || 'Не удалось выполнить запрос. Попробуйте ещё раз.';
        if (Array.isArray(message)) message = 'Проверьте заполнение полей: ' + message.map(item => item.loc.at(-1)).join(', ');
        const error = new Error(message);
        error.status = response.status;
        throw error;
    }
    return data;
}

export const money = value => new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(value / 100);
