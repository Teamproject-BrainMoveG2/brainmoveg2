<script setup>
import { computed } from 'vue';
import { formatSnelheid } from '../../composables/useFormatSnelheid';

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
        required: false
    },
});

const circleColor = '#13B5D1';
const radius = 45;
const circumference = 2 * Math.PI * radius;
const filledValue = computed(() => {
    return Math.max(0, Math.min(100, Number(props.value)));
});
const filledDashOffset = computed(() => {
    return circumference - (filledValue.value / 100) * circumference;
});

const displayValue = computed(() => formatSnelheid(props.label, props.value));

</script>

<template>
    <div class="c-stat-card">
        <p class="c-stat-label">{{ label }}</p>
        <div class="c-stats-content">
            <template v-if="icon">
                <component :is="icon" class="c-stat-icon" />
                <p class="c-stat-value">{{ displayValue }}</p>
            </template>
            <template v-else>
                <div class="c-stat-circle">
                    <svg viewBox="0 0 100 100" class="c-stat-svg">
                        <circle class="c-stat-bg" cx="50" cy="50" r="45" fill="none" stroke="#10A8C9" stroke-width="10" />
                        <circle class="c-stat-fg" cx="50" cy="50" r="45" fill="none" :stroke="circleColor" stroke-width="10" stroke-linecap="round"
                            :stroke-dasharray="circumference"
                            :stroke-dashoffset="filledDashOffset"
                            transform="rotate(-90 50 50)" />
                    </svg>
                    <div class="c-stat-percentage">{{ filledValue }}<span class="c-stat-percent">%</span></div>
                </div>
            </template>
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

.c-stat-circle {
    position: relative;
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 8px auto;
}
.c-stat-svg {
    width: 100px;
    height: 100px;
    display: block;
}
.c-stat-bg {
    stroke: var(--white);
}
.c-stat-fg {
    stroke: var(--primary);
    transition: stroke-dashoffset 0.5s ease;
}
.c-stat-percentage {
    position: absolute;
    top: 53%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: "Bebas Neue", sans-serif;
    font-size: 2rem;
    display: flex;
    align-items: baseline;
    line-height: 2.5rem;
}
.c-stat-percent {
    font-size: 18px;
    margin-left: 2px;
}
</style>
