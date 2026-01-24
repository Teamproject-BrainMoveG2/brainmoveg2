<script setup>
import { Wifi, WifiOff } from 'lucide-vue-next';
import { computed, toRef } from 'vue';
import { useBattery } from '../../composables/useBattery';

const props = defineProps({
    name: {
        type: String,
        required: true
    },
    batteryPercentage: {
        type: Number,
        required: true
    },
    isConnected: {
        type: Boolean,
        default: true
    }
});

const circleColor = computed(() => {
    const colorName = props.name.toLowerCase();
    
    const colorMap = {

        'groen': 'var(--accent-green)',
        'oranje': 'var(--accent-orange)',
        'geel': 'var(--yellow)',
        'blauw': 'var(--blue)',
        'rood': 'var(--red)',
 
        'green': 'var(--accent-green)',
        'orange': 'var(--accent-orange)',
        'yellow': 'var(--yellow)',
        'blue': 'var(--blue)',
        'red': 'var(--red)',
    };
    
    return colorMap[colorName] || 'var(--accent-green)';
});

const { isLowBattery, batteryIcon } = useBattery(toRef(props, 'batteryPercentage'));
</script>

<template>
    <div class="c-cardpotje" :class="{ 'c-cardpotje--disconnected': !isConnected }">
        <div class="c-cardpotje__title">
            <div class="c-cardpotje__circle" :style="{ backgroundColor: circleColor }"></div>
            <p class="small-body">{{ name }}</p>
        </div>
        <div class="c-cardpotje__content">
            <div class="c-cardpotje__status" v-if="isConnected">
                <p class="c-cardpotje__percentage" :class="{ 'c-cardpotje__percentage--low': isLowBattery }">{{ batteryPercentage }}%</p>
                <component :is="batteryIcon" class="c-cardpotje__icon" :class="{ 'c-cardpotje__icon--low-battery': isLowBattery }" />
            </div>
            <p class="c-cardpotje__connecting" v-else>Connecting ...</p>
            <Wifi v-if="isConnected" class="c-cardpotje__icon" />
            <WifiOff v-else class="c-cardpotje__icon" />
        </div>
    </div>
</template>

<style scoped>
.c-cardpotje {
    border-radius: var(--radius-s);
    padding: var(--spacing-05);
    background-color: var(--white);
    display: flex;
    flex-direction: column;
    color: var(--grey-85);
    gap: var(--spacing-baseline);
}

.c-cardpotje--disconnected {
    background-color: var(--red-light-5);
}

.c-cardpotje__circle {
    width: .9375rem;
    height: .9375rem;
    border-radius: 50%;
}

.c-cardpotje__title {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--spacing-04);
}

.c-cardpotje__content {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.c-cardpotje__status {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--spacing-03);
}

.c-cardpotje__percentage {
    font-family: bebas-neue, sans-serif;
    font-size: var(--font-size-8);
    font-weight: var(--font-weight-bold);
    line-height: 2.5rem;
}

.c-cardpotje__percentage--low {
    color: var(--red);
}

.c-cardpotje__icon {
    width: 1.875rem;
    height: 1.875rem;
    line-height: 2rem;
}

.c-cardpotje__icon--low-battery {
    color: var(--red);
}

.c-cardpotje--disconnected .c-cardpotje__icon {
    color: var(--red);
}

.c-cardpotje__connecting {
    font-size: var(--font-size-2);
    color: var(--grey-60);
}

/* Smaller fonts for screens below 360px */
@media (max-width: 395px) {
    .c-cardpotje__percentage {
        font-size: var(--font-size-7);
        line-height: 2rem;
    }

    .c-cardpotje__icon {
        width: 1.5rem;
        height: 1.5rem;
        line-height: 1.5rem;
    }

    .c-cardpotje__connecting {
        font-size: var(--font-size-1);
    }

    .c-cardpotje {
        padding: var(--spacing-04);
    }
}

</style>
