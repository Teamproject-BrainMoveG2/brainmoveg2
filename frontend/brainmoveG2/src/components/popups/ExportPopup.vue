<script setup>
import { ref, watch } from 'vue';
import PopupCloseButton from '../buttons/PopupCloseButton.vue';
import { VDatePicker } from 'vuetify/components';
import { useDate } from 'vuetify';

const props = defineProps({
  show: { type: Boolean, required: true },
  initialDate: { type: Date, default: () => new Date() }
});
const emit = defineEmits(['close']);

const selectedDate = ref(props.initialDate);
const adapter = useDate();

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
  // Today as start
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
  <div v-if="show" class="c-popup-overlay" @click="closePopup">
    <div class="c-popup" @click.stop>
      <div class="c-popup__header">
        <h2 class="c-popup__title">Vanaf wanneer wilt u exporteren?</h2>
        <PopupCloseButton @close="closePopup" />
      </div>
      <div class="c-popup__content">
        <label for="export-date">Kies een datum:</label>
        <VDatePicker
          v-model="selectedDate"
          :max="new Date().toISOString().substr(0, 10)"
          hide-title="true"
          id="export-date"
          style="width: 100%;;"
        />
        <button class="c-btn c-btn--primary" @click="handleDownload">Download</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.c-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: start;
  justify-content: center;
  z-index: 1000;
  padding: var(--spacing-04);
}
.c-popup {
  background: var(--white);
  border-radius: var(--radius-s);
  padding: var(--spacing-05);
  max-width: 700px;
  width: 100%;
  height: auto;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}
.c-popup__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-05);
}
.c-popup__title {
  font-size: var(--font-size-5);
  font-weight: var(--font-weight-bold);
  color: var(--grey-85);
  margin: 0;
}
.c-popup__content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-03);
}
label {
  margin-bottom: 8px;
  font-size: 1rem;
}
</style>
