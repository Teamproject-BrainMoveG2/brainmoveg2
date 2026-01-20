<script setup>
  import { Download } from 'lucide-vue-next';
  import TabSwitcher from '../components/TabSwitcher.vue';
  import StatCard from '../components/cards/StatCard.vue';
  import { Clock } from 'lucide-vue-next';
  import { ref } from 'vue';
  import ResultTableRow from '../components/ResultTableRow.vue';
  import ResultSelect from '../components/ResultSelect.vue';
  import ResultSearch from '../components/ResultSearch.vue';
  import ExportButton from '../components/ExportButton.vue';
  const selectedMode = ref('all');
  const searchQuery = ref('');
  const selectOptions = [
    { label: 'Alle Gamemodes', value: 'all' }
  ];
  function onSearch() {
    // Implement search logic here
  }
</script>

<template>
    <header class="c-header">
    <div class="c-header__content">
      <div class="c-header__title-wrapper">
        <h1>Resultaten</h1>
        <ExportButton :icon="Download" label="Exporteer" />
      </div>
      <p class="small-body">Bekijk het totale aantal resultaten </p>
    </div>
  </header>
    <TabSwitcher
      v-model:activeTab="activeTab"
      :tabs=" [
        { label: 'Vandaag', value: 'Vandaag' },
        { label: 'Week', value: 'Week' },
        { label: 'Maand', value: 'Maand' },
        { label: 'Begin', value: 'Begin' }
      ]"
    />
    <main class="c-content-wrapper">
      <div class="c-result-grid">
      <StatCard 
        label="Gem. accuracy" 
        :value="`76`"
        
        />
      <StatCard 
        label="Avg. snelheid" 
        :value="`250MS`"
        :icon="Clock"
      />
    </div>
    <div class="c-resultaten-filter">
      <h2>Resultaten:</h2>
      <ResultSelect v-model="selectedMode" :options="selectOptions" />
      <ResultSearch v-model="searchQuery" placeholder="Gebruiker zoeken..." @search="onSearch" />
  </div>
  <div class="c-table--resultaten-wrapper">
  <table class="c-table c-table--resultaten">
  <thead>
    <tr class="c-table__headings">
      <th>NAME</th>
      <th>ACCURATHEID</th>
      <th>GEM. REACTIE</th>
      <th>MOEILIJKHEID</th>
    </tr>
  </thead>
  <tbody>
    <ResultTableRow name="Name1" accuracy="54%" reaction="950ms" difficulty="Intense" />
    <ResultTableRow name="Name2" accuracy="73%" reaction="650ms" difficulty="Challenging" />
    <ResultTableRow name="Name3" accuracy="35%" reaction="135ms" difficulty="Relaxed" />
  </tbody>
</table>
</div>
    </main>
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
  padding: var(--spacing-06);
  display: flex;
  justify-content: center;
  align-items: center;
}

.c-header__content {
  width: 100%;
  display: flex;
  flex-direction: column;
  max-width: 26.25rem;
  gap: var(--spacing-03);
  color: var(--grey-85);


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

::v-deep .c-tab {
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