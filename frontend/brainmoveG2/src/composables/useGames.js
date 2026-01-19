import { ref } from 'vue';

export function useGames() {
  const modes = ref([]);
  const Ip = `${window.location.hostname}:8000`;

  async function fetchGames() {
    try {
      const response = await fetch(`http://${Ip}/modes`);
      if (!response.ok) throw new Error('Failed to fetch modes');
      modes.value = await response.json();
    } catch (e) {
      modes.value = [];
    }
  }

  return {
    modes,
    fetchGames
  };
}
