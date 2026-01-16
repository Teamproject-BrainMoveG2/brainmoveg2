<script setup>
defineProps({
    difficulty: {
        type: Object,
        required: true
    },
    isActive: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['select']);

const handleClick = () => {
    emit('select');
};
</script>

<template>
    <button 
        :class="['c-difficulty-option', `c-difficulty--${difficulty.color}`, { 'is-active': isActive }]"
        @click="handleClick"
    >
        <p>{{ difficulty.label }}</p>
        <div class="c-difficulty-bars">
            <span class="c-bar c-bar--first" :class="[`c-bar--${difficulty.color}`, { 'is-filled': true }]"></span>
            <span class="c-bar c-bar--middle" :class="[`c-bar--${difficulty.color}`, { 'is-filled': difficulty.id === 'challenging' || difficulty.id === 'intense' }]"></span>
            <span class="c-bar c-bar--last" :class="[`c-bar--${difficulty.color}`, { 'is-filled': difficulty.id === 'intense' }]"></span>
        </div>
    </button>
</template>

<style scoped>
.c-difficulty-option {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-03);
    padding: var(--spacing-03) var(--spacing-05);
    background-color: var(--grey-2);
    border: 2px solid transparent;
    border-radius: var(--radius-s);
    cursor: pointer;
    transition: all 0.3s ease;
    color: var(--grey-85);
}

.c-difficulty-option.is-active {
    border-color: currentColor;
}

.c-difficulty--green.is-active {
    color: var(--accent-green);
}

.c-difficulty--orange.is-active {
    color: var(--accent-orange);
}

.c-difficulty--red.is-active {
    color: var(--red);
}

.c-difficulty-bars {
    display: flex;
    gap: var(--spacing-02);
}

.c-bar {
    width: 20px;
    height: 5px;
    background: var(--white);
    border-radius: 0;
}

.c-bar--first {
    border-radius: 999px 0 0 999px;
}

.c-bar--middle {
    border-radius: 0;
}

.c-bar--last {
    border-radius: 0 999px 999px 0;
}

.c-bar--green {
    border: 2px solid var(--accent-green);
}

.c-bar--orange {
    border: 2px solid var(--accent-orange);
}

.c-bar--red {
    border: 2px solid var(--red);
}

.c-bar--green.is-filled {
    background: var(--accent-green);
}

.c-bar--orange.is-filled {
    background: var(--accent-orange);
}

.c-bar--red.is-filled {
    background: var(--red);
}
</style>
