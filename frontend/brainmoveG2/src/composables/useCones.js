import { ref, computed, onMounted } from 'vue';
import io from 'socket.io-client';

export function useCones() {
  const cones = ref([]);
  const Ip = `${window.location.hostname}:8000`;
  let socket = null;

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

  const connectSocket = () => {
    if (socket) return;
    socket = io(`http://${Ip}`);
    socket.on('connect', () => {
      console.log('Socket connected:', socket.id);
    });
    socket.on('cone_update', () => {
      
      fetchCones();
      
    });
    socket.on('disconnect', () => {
      console.log('Socket disconnected');
    });
  };

  onMounted(() => {
    fetchCones();
    connectSocket();
  });

  // Show cones in popup if disconnected OR battery < 25
  const warningCones = computed(() => {
    return cones.value.filter(cone => !cone.connected || cone.battery_percentage < 25);
  });

  return {
    cones,
    colorToDutch,
    warningCones,
    fetchCones,
    connectSocket
  };
}
