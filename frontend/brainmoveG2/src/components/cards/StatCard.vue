<script setup>
import { computed } from 'vue';

const props = defineProps({
    label: {
        type: String,
        required: true
    },
    value: {
        type: [String, Number],
        required: true
    },
    icon: {
        type: Object,
        required: true
    },
});


</script>

<template>
    <div class="c-stat-card">
        <p class="c-stat-label">{{ label }}</p>
        <div class="c-stats-content">
            <component :is="icon" class="c-stat-icon" />
            <p class="c-stat-value">{{ value }}</p>
        </div>
    </div>
</template>

<style scoped>
    
.c-stat-card {
    text-align: center;
    background-color: var(--white);
    padding: 16px;
    border-radius: var(--radius-s);
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-height: 140px;
    box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
}

.c-stat-card:nth-child(1),
.c-stat-card:nth-child(4){
    background-color: var(--primary-light);
}

.c-stats-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    gap: 8px;
    align-items: center;
    gap: 4px;
}

.c-stat-icon {
    width: 32px;
    height: 32px;
    color: var(--text-primary);
}

.c-stat-value {
    font-family: "Bebas Neue", sans-serif;
    font-size: 32px;
    line-height: 40px;
    color: var(--text-primary);
    margin: 0;
}

.c-stat-label {
    margin: 0;
}
</style>
