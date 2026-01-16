<script setup>
import { BatteryMedium } from 'lucide-vue-next';

defineProps({
    name: {
        type: String,
        required: true
    },
    color: {
        type: String,
        required: true
    },
    battery: {
        type: Number,
        required: true
    }
});
</script>

<template>
    <div class="c-smallPotjeCard">
        <div class="c-smallPotjeCard__section">
            <div class="c-smallPotjeCard__color" :style="{ backgroundColor: color }"></div>
            <p class="small-body">{{ name }}</p>
        </div>
        <div class="c-smallPotjeCard__section c-smallPotjeCard__section--battery">
            <p class="small-body">{{ battery }}%</p>
            <BatteryMedium class="c-battery-icon" />
        </div>
    </div>
</template>

<style scoped>
.c-smallPotjeCard {
    display: flex;
    padding: var(--spacing-baseline);
    background-color: var(--white);
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    border-radius: var(--radius-s);
}

.c-smallPotjeCard__section {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--spacing-03);
}

.c-smallPotjeCard__section--battery {
    gap: var(--spacing-02);
}

.c-smallPotjeCard__color {
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 50%;
}

.c-battery-icon {
    color: var(--grey-85);
    width: 1.5rem;
    height: 1.5rem;
}
</style>
