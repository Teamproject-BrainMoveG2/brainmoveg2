<script setup>
const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: ''
    },
    type: {
        type: String,
        default: 'text'
    }
});

const emit = defineEmits(['update:modelValue']);

const handleInput = (event) => {
    emit('update:modelValue', event.target.value);
};
</script>

<template>
    <form action="#" class="c-form">
        <input 
            :type="type"
            :value="modelValue"
            @input="handleInput"
            class="c-input small-body" 
            :placeholder="placeholder"
            :required="$route.name === 'gamesettings'"
            maxlength="45"
        />
    </form>
</template>

<style scoped>
.c-form {
    width: 100%;
}

.c-input {
    width: 100%;
    padding: var(--spacing-05) var(--spacing-05);
    border: 1px solid var(--grey-15);
    border-radius: var(--radius);
    font-size: var(--font-size-base);
    transition: border 0.3s ease;
    color: var(--grey-70);
    box-sizing: border-box;
}

.c-input:focus, .c-input:hover, .c-input:active {
    outline: none;
    border-color: var(--primary);
}
</style>
