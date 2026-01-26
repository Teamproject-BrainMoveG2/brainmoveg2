
<script setup>
import { computed } from 'vue';
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
    },
    showErrors: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['update:modelValue']);

const handleInput = (event) => {
    emit('update:modelValue', event.target.value);
};

const isInvalid = computed(() => {
    return props.showErrors && (!props.modelValue || props.modelValue.trim() === '') && (props.placeholder.toLowerCase().includes('gebruikersnaam'));
});
</script>

<template>
    <form action="#" class="c-form" @submit.prevent>
        <input 
            :type="type"
            :value="modelValue"
            @input="handleInput"
            :class="['c-input', 'small-body', { 'c-input--error': isInvalid }]"
            :placeholder="placeholder"
            maxlength="45"
        />
        <div v-if="isInvalid" class="c-input-error">Geef een gebruikersnaam</div>
    </form>
</template>


<style scoped>
.c-form {
    width: 100%;
}

 .c-input-error {
    color: var(--red);
    font-size: 0.9em;
    margin-top: 4px;
    text-align: left;
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

.c-input--error {
    border-color: var(--red);
}

.c-input:focus, .c-input:hover, .c-input:active {
    outline: none;
    border-color: var(--primary);
}
</style>
