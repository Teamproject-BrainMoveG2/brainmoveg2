<script setup>
const props = defineProps({
    instructions: {
        type: Array,
        required: true,
     
    },
    color: {
        type: String,
        default: 'primary',
        validator: (value) => ['primary', 'orange', 'green'].includes(value)
    }
});
</script>

<template>
    <div class="c-instructions">
        <div 
            v-for="instruction in instructions" 
            :key="instruction.number" 
            class="c-instruction-item"
        >
            <span class="c-instruction-number" :class="`c-instruction-number--${color}`">{{ instruction.number }}</span>
            <p class="c-instruction-text">{{ instruction.text }}</p>
        </div>
    </div>
</template>

<style scoped>
.c-instructions {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: var(--spacing-06);
    text-align: left;
}

.c-instruction-item {
    display: flex;
    gap: var(--spacing-05);
    flex-direction: row;
    justify-content: start;
    align-items: center;
}

.c-instruction-number {
    width: 2.5rem;
    height: 2.5rem;
    min-width: 2.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.c-instruction-number--primary {
    background-color: var(--primary-light-5);
}

.c-instruction-number--orange {
    background-color: var(--accent-orange-light);
}

.c-instruction-number--green {
    background-color: var(--accent-green-light);
}

.c-instruction-text {
    font-size: var(--font-size-3);
    line-height: 24px;
    margin: 0;
    color: var(--grey-85);
}

@media (min-width: 768px) {
    .c-instruction-text {
        font-size: var(--font-size-4);
        line-height: 28px;
    }
}

@media (min-width: 1024px) {
    .c-instruction-number {
        font-size: var(--font-size-8);
    }
    
    .c-instruction-text {
        font-size: var(--font-size-5);
        line-height: 32px;
    }
}
</style>
