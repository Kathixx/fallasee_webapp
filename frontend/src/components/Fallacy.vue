<script setup>
defineProps([
    'title', 'explanation'
])
</script>

<template>
    <div class="row">
        <div class="col-2">
            <div class="symbol"></div>
        </div>
        <div class="col-10">
            <h2>{{title}}</h2>
            <p>{{ explanation }}</p>
        </div>
    </div>
</template>

<style scoped>
.row {
    margin: 2em 0px;
}
.symbol{
    background-color: var(--yellow);
    width: 100px;
    height: 100px;
    border-radius: 20px;
}
</style>