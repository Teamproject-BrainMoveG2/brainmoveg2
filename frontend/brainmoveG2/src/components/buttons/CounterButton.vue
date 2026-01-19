<script setup>
import { Minus, Plus } from 'lucide-vue-next';

const props = defineProps({
    modelValue: {
        type: Number,
        required: true
    },
    min: {
        type: Number,
        default: 1
    },
    max: {
        type: Number,
        default: Infinity
    }
});

const emit = defineEmits(['update:modelValue']);

const increment = () => {
    if (props.modelValue < props.max) {
        emit('update:modelValue', props.modelValue + 1);
    }
};

const decrement = () => {
    if (props.modelValue > props.min) {
        emit('update:modelValue', props.modelValue - 1);
    }
};
</script>

<template>
    <div class="c-counter">
        <button class="c-counter__button" @click="decrement">
            <Minus class="c-counter__icon" />
        </button>
        <span class="body-large">{{ modelValue }}</span>
        <button class="c-counter__button" @click="increment">
            <Plus class="c-counter__icon" />
        </button>
    </div>
</template>

<style scoped>
.c-counter {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-05);
    background-color: var(--white);
    border-radius: var(--radius-s);
    padding: var(--spacing-baseline);
    width: 100%;
}

.c-counter__button {
    background-color: var(--primary);
    border: none;
    border-radius: var(--radius-s);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: opacity 0.2s;
    color: var(--white);
    padding: var(--spacing-baseline) var(--spacing-05);
}

.c-counter__icon {
    width: 1rem;
    height: 1rem;
}

.c-counter__button:hover {
    opacity: 0.9;
}

.c-counter__button:active {
    opacity: 0.7;
}

@media  (max-width: 380px) {
    .c-counter__button {
        padding: var(--spacing-baseline) var(--spacing-03);
    }
}
</style>
