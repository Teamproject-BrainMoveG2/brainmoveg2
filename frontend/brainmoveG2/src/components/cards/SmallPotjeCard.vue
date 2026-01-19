<script setup>
import { BatteryMedium } from 'lucide-vue-next';

import { computed } from 'vue';

const props = defineProps({
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
    },
    isConnected: {
        type: Boolean,
        default: true
    }
});

const isLowBattery = computed(() => props.battery < 25);
</script>

<template>
    <div class="c-smallPotjeCard" :class="{ 'c-smallPotjeCard--disconnected': !isConnected }">
        <div class="c-smallPotjeCard__section">
            <div class="c-smallPotjeCard__color" :style="{ backgroundColor: color }"></div>
            <p class="c-smallPotjeCard__name small-body">{{ name }}</p>
        </div>
        <div class="c-smallPotjeCard__section c-smallPotjeCard__section--battery">
            <template v-if="isConnected">
                <p class="small-body" :class="{ 'c-smallPotjeCard__percentage--low': isLowBattery }">{{ battery }}%</p>
                <BatteryMedium class="c-battery-icon" :class="{ 'c-battery-icon--low-battery': isLowBattery }" />
            </template>
            <template v-else>
                <p class="c-smallPotjeCard__connecting">Connecting...</p>
                <BatteryMedium class="c-battery-icon c-battery-icon--disconnected" />
            </template>
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
    transition: all 0.2s;
}

.c-smallPotjeCard--disconnected {
    background-color: var(--red-light-5);
    justify-content: flex-start;
    gap: var(--spacing-baseline);
}

@media (max-width: 380px) {
    .c-smallPotjeCard__name {
        display: none;
    }
    
}


.c-smallPotjeCard__section {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--spacing-03);
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
    transition: color 0.2s;
}

.c-battery-icon--low-battery {
    color: var(--red);
}

.c-battery-icon--disconnected {
    display: none;
}

.c-smallPotjeCard__percentage--low {
    color: var(--red);
}

.c-smallPotjeCard__connecting {
    color: var(--red);
}
</style>
