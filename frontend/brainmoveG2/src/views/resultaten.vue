<script setup>
  import { Download } from 'lucide-vue-next';
  import TabSwitcher from '../components/tabs/TabSwitcher.vue';
  import StatCard from '../components/cards/StatCard.vue';
  import { Clock } from 'lucide-vue-next';
  import { ref, onMounted, computed } from 'vue';
  import ResultTableRow from '../components/table/ResultTableRow.vue';
  import ResultSelect from '../components/ResultSelect.vue';
  import ResultSearch from '../components/ResultSearch.vue';
  import ExportButton from '../components/buttons/ExportButton.vue';
  import { useGames } from '../composables/useGames';
  import ExportPopup from '../components/popups/ExportPopup.vue';

  // Export popup state
  const showExportPopup = ref(false);
  const exportInitialDate = ref(new Date());

  function openExportPopup() {
    showExportPopup.value = true;
  }
  function closeExportPopup() {
    showExportPopup.value = false;
  }

  const { modes, fetchGames } = useGames();
  const selectedMode = ref('all');
  const searchQuery = ref('');

  const gameOptions = computed(() => {
    const options = [{ label: 'Alle Gamemodes', value: 'all' }];
    if (Array.isArray(modes.value)) {
      modes.value.forEach(game => {
        options.push({ label: game.naam, value: game.spelmodus_id });
      });
    }
    return options;
  });

  const activeTab = ref('Vandaag');
  const data = ref(null);
  const Ip = `${window.location.hostname}:8000`;

  const filteredData = computed(() => {
    if (!data.value || !data.value.data) {
      return [];
    }

    let filtered = data.value.data;

  
    if (selectedMode.value !== 'all') {
      filtered = filtered.filter(item => item.spelmodus_id == selectedMode.value);
    }

   
    if (searchQuery.value && searchQuery.value.trim() !== '') {
      const query = searchQuery.value.trim().toLowerCase();
      filtered = filtered.filter(item => item.username && item.username.toLowerCase().includes(query));
    }

    return filtered;
  });

  async function fetchDataToday() {
    try {
      const response = await fetch(`http://${Ip}/data/today`);
      if (!response.ok) throw new Error('Failed to fetch modes');
      data.value = await response.json();
    } catch (e) {
      data.value = [];
    }
  }

  async function fetchDataWeek() {
    try {
      const response = await fetch(`http://${Ip}/data/week`);
      if (!response.ok) throw new Error('Failed to fetch modes');
      data.value = await response.json();
    } catch (e) {
      data.value = [];
    }
  }

  async function fetchDataMonth() {
    try {
      const response = await fetch(`http://${Ip}/data/month`);
      if (!response.ok) throw new Error('Failed to fetch modes');
      data.value = await response.json();
    } catch (e) {
      data.value = [];
    }
  }

  async function fetchDataAlltime() {
    try {
      const response = await fetch(`http://${Ip}/data/alltime`);
      if (!response.ok) throw new Error('Failed to fetch modes');
      data.value = await response.json();
    } catch (e) {
      data.value = [];
    }
  }

  function handleTabSelect(tabValue) {
    switch (tabValue) {
      case 'Vandaag':
        fetchDataToday();
        break;
      case 'Week':
        fetchDataWeek();
        break;
      case 'Maand':
        fetchDataMonth();
        break;
      case 'Begin':
        fetchDataAlltime();
        break;
    }
  }

  onMounted(() => {
    fetchDataToday();
    fetchGames();
  });
</script>

<template>
    <div class="c-header">
        <div class="c-header__content">
          <div class="c-header__title-wrapper">
            <h1>Resultaten</h1>
            <ExportButton :icon="Download" label="Exporteer" @click="openExportPopup" />
          </div>
          <p class="small-body">Bekijk het totale aantal resultaten </p>
        </div>
      </div>
    <TabSwitcher
      v-model:activeTab="activeTab"
      :tabs=" [
        { label: 'Vandaag', value: 'Vandaag' },
        { label: 'Week', value: 'Week' },
        { label: 'Maand', value: 'Maand' },
        { label: 'Begin', value: 'Begin' }
      ]"
      @select="handleTabSelect"
    />
    <main class="c-content-wrapper">
      <section class="c-result-grid" v-if="data">
      <StatCard 
        label="Accuraatheid" 
        :value="`${Math.round(data.avg_accuracy)}`"
        
        />
      <StatCard 
        label="Gem. snelheid" 
        :value="`${Math.round(data.avg_reaction_speed)}`"
        :icon="Clock"
      />
    </section>
    <section class="c-resultaten-filter">
      <h2>Resultaten:</h2>
      <ResultSelect v-model="selectedMode" :options="gameOptions" />
      <ResultSearch v-model="searchQuery" placeholder="Gebruiker zoeken..." @search="onSearch" />
  </section>
  <section class="c-table--resultaten-wrapper" v-if="data && data.data">
  <table class="c-table c-table--resultaten">
  <thead>
    <tr class="c-table__headings">
      <th>Naam</th>
      <th>ACCURAATHEID</th>
      <th>GEM. REACTIE</th>
      <th>MOEILIJKHEID</th>
    </tr>
  </thead>
  <tbody>
    <ResultTableRow 
      v-for="item in filteredData" 
      :key="item.spelsessie_id"
      :name="item.username" 
      :accuracy="`${Math.round(item.accuracy_percent)}%`" 
      :reaction="`${Math.round(item.avg_reactietijd_ms)}`" 
      :difficulty="!item.naam || item.naam === 'null' ? 'geen' : item.naam" />
  </tbody>
</table>
</section>
</main>
<ExportPopup
  :show="showExportPopup"
  :initialDate="exportInitialDate"
  @close="closeExportPopup"
/>
</template>

<style scoped>


.c-resultaten-filter {
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
  width: 100%;
}

.c-result-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  width: 100%;
  
}

.c-header {
  display: flex;
  align-items: center;
  padding: 0 var(--spacing-06);
  margin-bottom: var(--spacing-06);
  margin-left: auto;
  margin-right: auto;

  max-width: 26.25rem;
  


  @media (min-width: 768px) {

    max-width: 500px;
    gap: var(--spacing-08);
    padding: 0;

  }

  @media (min-width: 1024px) {

      max-width: 550px;
      gap: var(--spacing-09);
      padding: 0;

  }

}


.c-header__content {
  
  width: 100%;
  display: flex;
  flex-direction: column;
  max-width: 26.25rem;
  gap: var(--spacing-03);
  color: var(--grey-85);

  @media (max-width: 480px) {
   
    padding: 0;

  }
   @media (min-width: 768px) {
   
    max-width: 500px;

  }

  @media (min-width: 1024px) {
     
      max-width: 550px;

  }
}

.c-header__title-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}

:deep(.c-tab) {
  font-size: var(--font-size-3);
}

.c-table--resultaten-wrapper {
  width: 100%;
  overflow-x: auto;
}

.c-table--resultaten {
  min-width: 400px;
  width: 100%;
  border-collapse: collapse;
}

.c-table__headings {
  color: var(--grey-85);
  text-align: left;
  gap: 0
  
}

.c-table--resultaten th {
  padding: 0;
  width: 25%;
  box-sizing: border-box;
  text-align: left;
}
</style>