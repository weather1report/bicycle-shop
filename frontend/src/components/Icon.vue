<script setup>
defineProps({ name: String });
const paths = {
    arrow: 'M4 12h16m-6-6 6 6-6 6',
    bag: 'M5 7h14l1 14H4L5 7zm3 0V5a4 4 0 0 1 8 0v2',
    user: 'M20 21v-2a8 8 0 0 0-16 0v2 M16 6a4 4 0 1 1-8 0 4 4 0 0 1 8 0',
    search: 'm21 21-5-5 M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0',
    check: 'm5 12 4 4L19 6',
    truck: 'M1 5h13v12H1V5zm13 4h4l4 5v3h-8 M8 18a2 2 0 1 1-4 0 2 2 0 0 1 4 0 M20 18a2 2 0 1 1-4 0 2 2 0 0 1 4 0',
    shield: 'm12 2 9 4v6c0 5-9 10-9 10S3 17 3 12V6l9-4zm-4 9 3 3 5-5',
    close: 'm6 6 12 12M18 6 6 18',
    menu: 'M3 6h18M3 12h18M3 18h18',
};
</script>
<template><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path :d="paths[name] || paths.arrow" /></svg></template>
