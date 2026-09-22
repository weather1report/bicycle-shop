<script setup>
defineProps({ kind: { default: 'bike' }, color: { default: '#728276' } });
</script>

<template>
    <svg class="product-art" viewBox="0 0 600 380" fill="none" aria-hidden="true">
        <ellipse cx="302" cy="321" rx="237" ry="13" fill="#26392e" opacity=".07"/>
        <g v-if="kind === 'bike'" stroke-linecap="round" stroke-linejoin="round">
            <g stroke="#9ca29b" stroke-width="1.5" opacity=".7"><path d="m141 248-72-53m72 53 73-53m-73 53v-89m0 89-74 49m74-49 76 49m-76-49v88m309-88-73-53m73 53 73-53m-73 53v-89m0 89-74 49m74-49 75 49m-75-49v88"/></g>
            <g stroke="#29312d" stroke-width="13"><circle cx="141" cy="248" r="86"/><circle cx="450" cy="248" r="86"/></g>
            <g stroke="#bbc0b5" stroke-width="3"><circle cx="141" cy="248" r="75"/><circle cx="450" cy="248" r="75"/></g>
            <path d="m141 248 90-133 71 133H141l243-123-153-10m153 10 66 123" :stroke="color" stroke-width="14"/>
            <path d="m302 248 82-123" :stroke="color" stroke-width="20"/>
            <path d="m231 115-12-29m165 39-15-43 34-8" stroke="#29312d" stroke-width="9"/>
            <path d="M188 86h57m153-12 20-3" stroke="#27332c" stroke-width="13"/>
            <path d="m388 91 41 52-11 27" stroke="#677368" stroke-width="2"/>
            <circle cx="302" cy="248" r="22" stroke="#3d4940" stroke-width="7"/><path d="m302 248 26 28h15m-41-28-23-25h-14" stroke="#303b34" stroke-width="7"/>
            <path d="m141 249 156 18m-156-18 159-21" stroke="#536053" stroke-width="2"/>
            <path d="m432 197 18 51" stroke="#35463a" stroke-width="10"/>
            <path d="m315 208 27-44" stroke="#e2e5d8" stroke-width="3"/>
        </g>
        <g v-else-if="kind === 'helmet'" :fill="color" stroke="#36463c" stroke-width="5"><path d="M149 235c-6-85 45-144 142-144 104 0 155 54 159 132l-67 45-207-1z"/><path d="m177 269 75 44 100-41" fill="none" stroke-width="12"/><path d="m224 135-20 67m68-82-11 76m61-76 6 76m41-62 22 64" stroke="#293a2f" stroke-width="16"/><path d="m153 229 284-3" fill="none" stroke-width="9"/></g>
        <g v-else-if="kind === 'bottle'" :fill="color" stroke="#42574a" stroke-width="4"><path d="M259 80h82v38l17 28v151q0 16-17 16h-82q-17 0-17-16V146l17-28z"/><path d="M266 59h68v25h-68z" fill="#35483b"/><path d="M280 48h40v12h-40z" fill="#222e27"/><path d="M244 177h112v76H244z" fill="#e2e7db" stroke="none"/><text x="261" y="222" fill="#35483b" stroke="none" font-size="24" font-family="Arial" font-weight="bold">VELO</text></g>
        <g v-else-if="kind === 'tire'" stroke="#303932"><ellipse cx="300" cy="195" rx="115" ry="125" stroke-width="36"/><ellipse cx="300" cy="195" rx="115" ry="125" stroke="#697166" stroke-width="3" stroke-dasharray="8 9"/></g>
        <g v-else-if="kind === 'pedal'" :fill="color" stroke="#33443a" stroke-width="7"><path d="m157 167 125-33 53 90-128 33zM344 126l76 25 24 102-82-19z"/><path d="m191 177 69-18 24 48-69 20zM369 159l29 8 12 46-28-7z" fill="#eff0e9"/><path d="m290 169 49-13m-192 80 41-11" stroke-width="14"/></g>
        <g v-else-if="kind === 'saddle'" :fill="color" stroke="#344138" stroke-width="5"><path d="M165 154c-45 97 44 101 94 76 36-18 73-15 150-11 66 3 73-26 14-44-53-17-93-24-135-48-67-41-98-20-123 27z"/><path d="m215 247 120 26 55-49" fill="none" stroke-width="10"/></g>
        <g v-else-if="kind === 'lock'" stroke="#34463a" stroke-width="25"><path d="M232 256V150a68 68 0 0 1 136 0v106"/><rect x="207" y="247" width="186" height="40" rx="12" :fill="color" stroke-width="5"/></g>
        <g v-else-if="kind === 'pump'" stroke="#35473c" stroke-linecap="round"><path d="m213 291 152-180" :stroke="color" stroke-width="37"/><path d="m349 131 38-46" stroke-width="16"/><path d="m369 68 38 33" stroke-width="19"/><path d="m218 285-32 6-18-17" stroke-width="12"/></g>
        <g v-else-if="kind === 'gloves'" :fill="color" stroke="#34453a" stroke-width="5"><path d="m182 266-25-88 14-10 26 31-14-65 18-5 20 57-7-74 20-1 12 73 5-69 20 2-1 71 20-51 17 9-27 106-28 33z"/><path d="m346 271-27-101 20-4 21 40-6-73 21-1 11 68 8-80 20 4-2 83 19-63 18 8-14 65 25-39 16 14-45 92z"/></g>
        <g v-else-if="kind === 'glasses'" :fill="color" stroke="#304437" stroke-width="9"><path d="m137 181 126-6-16 71-79-4zM337 175l126 6-31 61-79 4z"/><path d="M263 191q37-28 74 0m-196-9 37-51h53m230 51-37-51h-53" fill="none"/></g>
        <g v-else-if="kind === 'computer'" :fill="color" stroke="#324437" stroke-width="6"><rect x="222" y="83" width="156" height="219" rx="28"/><rect x="239" y="105" width="122" height="143" rx="8" fill="#dce3cc"/><text x="251" y="174" fill="#354338" stroke="none" font-size="44" font-family="monospace">24.8</text><path d="M259 203h80m-69 73h60"/><text x="273" y="230" font-size="17" fill="#354338" stroke="none">KM/H</text></g>
        <g v-else :fill="color" stroke="#34463b" stroke-width="5"><path d="m186 173 152-45 74 27 7 69-166 42-65-26z"/><ellipse cx="215" cy="207" rx="39" ry="44" fill="#e7e7cb"/><ellipse cx="215" cy="207" rx="24" ry="29" fill="#faf9e8"/><path d="m281 251 21 47 37-10-15-43"/><path d="m283 165 47-12" stroke="#cad7c6" stroke-width="10"/></g>
    </svg>
</template>

<style scoped>
.product-art {
    display: block;
    width: 100%;
    height: auto;
}
</style>
