<script setup>

import { CirclePlay } from 'lucide-vue-next';
import ClockIcon from '../../assets/svg/clock.svg';
import BrainIcon from '../../assets/svg/brain.svg';
import TargetIcon from '../../assets/svg/target.svg';


const props = defineProps({
    title: {
        type: String,
        required: true
    },
    gameId: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true
    },
    icon: {
        type: String,
        required: true
    }
});
const iconMap = {
    clock: ClockIcon,
    brain: BrainIcon,
    target: TargetIcon
};

</script>

<template>
    <router-link :to="`/gamesettings/${gameId}`" class="c-game-card">
        <div class="c-game-card__content">
                <CirclePlay class="c-game-card__play-icon" />
            <div class="c-game-card__text">
                <h2>{{ title }}</h2>
                <p class="small-body">{{ description }}</p>
            </div>
        </div>
        <div class="c-game-card__clock">
            <img :src="`/svg/${icon}.svg`" :alt="`${icon} icon`" />
        </div>
    </router-link>
</template>

<style scoped>
.c-game-card {
    border-radius: var(--radius);
    padding: var(--spacing-06);
    background-color: var(--accent-green-light);
    display: flex;
    justify-content: space-between;
    text-align: start;
    align-items: center;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: visible;
    text-decoration: none;
    color: inherit;
}

.c-game-card:nth-child(2){
    background-color: var(--accent-orange-light);
}

.c-game-card:nth-child(3){
    background-color: var(--primary-light);
}

.c-game-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.c-game-card__content {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-05);
    flex: 1;
}

.c-game-card__play-icon {
    width: 2rem;
    height: 2rem;
    color: var(--accent-green);
}

.c-game-card:nth-child(2) .c-game-card__play-icon{
    color: var(--accent-orange);
}

.c-game-card:nth-child(3) .c-game-card__play-icon{
    color: var(--primary);
}

.c-game-card__text {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-03);
}

.c-game-card__text h2 {
    color: var(--grey-90);
    margin: 0;
}

.c-game-card__clock {
    position: absolute;
    right: -0.1rem;
    top: -1.2rem;
    display: flex;
}

.c-game-card__clock img {
    height: auto;
    opacity: 0.9;
}

@media (min-width: 768px) {
    .c-game-card__clock {
        right: -0.1rem;
        top: -1.2rem;
    }
    
    .c-game-card__clock img {
        width: 8rem;
    }
}
</style>
