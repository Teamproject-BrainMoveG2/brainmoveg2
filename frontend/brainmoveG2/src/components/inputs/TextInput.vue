
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
    }
});

const emit = defineEmits(['update:modelValue']);

const handleInput = (event) => {
    emit('update:modelValue', event.target.value);
};

const isInvalid = computed(() => {
    return (!props.modelValue || props.modelValue.trim() === '') && (props.placeholder.toLowerCase().includes('gebruikersnaam'));
});
</script>

<template>
    <form action="#" class="c-form">
        <input 
            :type="type"
            :value="modelValue"
            @input="handleInput"
            class="c-input small-body" 
            :placeholder="placeholder"
            :required="placeholder.toLowerCase().includes('gebruikersnaam')"
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

.c-input:invalid {
    border-color: var(--red);
}

.c-input:focus, .c-input:hover, .c-input:active {
    outline: none;
    border-color: var(--primary);
}
</style>
