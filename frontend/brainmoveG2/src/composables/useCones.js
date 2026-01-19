import { ref, computed, onMounted } from 'vue';

export function useCones() {
  const cones = ref([]);
  const Ip = `${window.location.hostname}:8000`;

  const colorToDutch = {
    'red': 'Rood',
    'blue': 'Blauw',
    'green': 'Groen',
    'yellow': 'Geel',
    'orange': 'Oranje'
  };

  const fetchCones = async () => {
    try {
      const response = await fetch(`http://${Ip}/cones`);
      const data = await response.json();
      cones.value = data;
    } catch (error) {
      cones.value = [];
    }
  };

  onMounted(() => {
    fetchCones();
  });

  // Show cones in popup if disconnected OR battery < 25
  const warningCones = computed(() => {
    return cones.value.filter(cone => !cone.connected || cone.battery_percentage < 25);
  });

  return {
    cones,
    colorToDutch,
    warningCones,
    fetchCones
  };
}
