<script setup>
import { ref, watch } from 'vue';
import BasePopup from './BasePopup.vue';
import { VDatePicker } from 'vuetify/components';

const props = defineProps({
  show: { type: Boolean, required: true },
  initialDate: { type: Date, default: () => new Date() }
});
const emit = defineEmits(['close']);

const selectedDate = ref(props.initialDate);

watch(() => props.show, (val) => {
  if (val) {
    selectedDate.value = props.initialDate;
  }
});

function closePopup() {
  emit('close');
}

async function handleDownload() {
  
  let endDateObj = selectedDate.value;
  if (!(endDateObj instanceof Date) || isNaN(endDateObj)) {
    endDateObj = new Date(endDateObj);
  }
  if (isNaN(endDateObj)) {
    endDateObj = new Date();
  }

  const todayObj = new Date();
  const pad = n => n.toString().padStart(2, '0');
  const end = `${todayObj.getFullYear()}-${pad(todayObj.getMonth() + 1)}-${pad(todayObj.getDate())}`;
  const  start= `${endDateObj.getFullYear()}-${pad(endDateObj.getMonth() + 1)}-${pad(endDateObj.getDate())}`;
  const Ip = `${window.location.hostname}:8000`;
  try {
    const response = await fetch(`http://${Ip}/data/excel?start=${start}&end=${end}`);
    console.log('Export response:', response);
    if (!response.ok) throw new Error('Failed to fetch export');
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `export_${start}_to_${end}.xlsx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (e) {
    alert('Export mislukt. Probeer opnieuw.');
  }
  closePopup();
}
</script>

<template>
  <BasePopup 
    :show="show" 
    title="Vanaf wanneer wilt u exporteren?"
    @close="closePopup"
  >
    <label for="export-date">Kies een datum:</label>
    <VDatePicker
      v-model="selectedDate"
      :max="new Date().toISOString().substr(0, 10)"
      hide-title="true"
      id="export-date"
      style="width: 100%;;"
    />
    <button class="c-btn c-btn--primary" @click="handleDownload">Download</button>
  </BasePopup>
</template>

<style scoped>
label {
  margin-bottom: var(--spacing-baseline);
  font-size: 1rem;
}
</style>
