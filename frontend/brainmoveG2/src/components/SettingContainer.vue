<script setup>
const props = defineProps({
    title: {
        type: String,
        default: ''
    },
    layout: {
        type: String,
        default: 'flex'
    },
    showGridError: {
        type: Boolean,
        default: false
    },
    gridErrorMessage: {
        type: String,
        default: ''
    }
});
</script>

<template>
    <div class="c-setting-section">
        <p class="small-body" v-if="title">{{ title }}</p>
        <div :class="['c-setting-options', layout === 'grid' ? 'c-setting-options--grid' : '']">
            <slot></slot>
            
        </div>
        <p v-if="layout === 'grid' && showGridError" class="c-error-message">
        {{ gridErrorMessage }}
        </p>
    </div>
</template>

<style scoped>

.c-error-message{
   color: var(--red);
   margin-top: var(--spacing-02);
    font-size: 0.9rem;
}

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

.c-setting-options--grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-05);
}


@media (max-width: 410px) {
    .c-setting-options {
        flex-wrap: wrap;
    }
}

</style>