<script setup>
defineProps({
    title: {
        type: String,
        default: ''
    },
});
</script>

<template>
    <div class="c-setting-section">
        <p v-if="title">{{ title }}</p>
        <div class="c-setting-options">
            <slot></slot>
        </div>
    </div>
</template>

<style scoped>

.c-setting-section {
    width: 100%;
    gap: var(--spacing-baseline);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.c-setting-options {
    display: flex;
    gap: var(--spacing-04);
    width: 100%;
}

/* Wrap difficulty options on small screens */
@media (max-width: 410px) {
    .c-setting-options {
        flex-wrap: wrap;
    }
}

</style>