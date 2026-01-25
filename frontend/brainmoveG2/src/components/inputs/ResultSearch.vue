<script setup>
const props = defineProps({
  modelValue: { type: String, required: true },
  placeholder: { type: String, default: 'Zoeken...' },
});
const emit = defineEmits(['update:modelValue', 'search']);
function onInput(e) {
  emit('update:modelValue', e.target.value);
}
function onSearch() {
  emit('search');
}
</script>

<template>
  <div class="c-resultaten-search">
    <input :value="modelValue" @input="onInput" :placeholder="placeholder" class="c-resultaten-input small-body" />
    <button class="c-resultaten-search-btn" @click="onSearch">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="9" cy="9" r="7" stroke="#222" stroke-width="2"/><path d="M15 15L18 18" stroke="#222" stroke-width="2" stroke-linecap="round"/></svg>
    </button>
  </div>
</template>

<style scoped>
.c-resultaten-search {
  width: 100%;
  border-radius: var(--radius);
  border: 1px solid var(--grey-15);
  background: var(--white);
  font-size: 1rem;
  font-family: "Source Sans Pro", sans-serif;
  font-size: var(--font-size-3);
  line-height: 1.5rem;
  font-weight: var(--font-weight-regular);
  color: var(--grey-85);
  box-sizing: border-box;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  padding: 0;
  justify-content: space-between;
}

.c-resultaten-search:hover, .c-resultaten-search:focus {
  border-color: var(--primary);
}
.c-resultaten-input {
  width: 85%;
  border: none;
  outline: none;
  font-size: 1rem;
  padding: var(--spacing-04);
  background: transparent;
  font-family: inherit;
  color: inherit;
  border-radius: var(--radius);
}
.c-resultaten-search-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  color: var(--grey-85);
}
</style>
