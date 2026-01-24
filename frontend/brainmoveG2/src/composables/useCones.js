import { ref, computed, onMounted, watch } from 'vue';
import io from 'socket.io-client';

export function useCones() {
  const cones = ref([]);

  let audio = null;
  if (typeof window !== 'undefined') {
    const audioUrl = new URL('../assets/audio/notification.wav', import.meta.url).href;
    audio = new Audio(audioUrl);
  }
  const Ip = `${window.location.hostname}:8000`;
  let socket = null;

  const colorToDutch = {
    'red': 'Rood',
    'blue': 'Blauw',
    'green': 'Groen',
    'yellow': 'Geel',
    'orange': 'Oranje',
    'purple': 'Paars'
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
    socket.on('cone_update', (data) => {
      if (Array.isArray(data)) {
        const prevWarning = cones.value.filter(cone => !cone.connected || cone.battery_percentage < 25).length;
        const newWarning = data.filter(cone => !cone.connected || cone.battery_percentage < 25).length;
        cones.value = data;
        if (audio && newWarning > prevWarning) {
          audio.currentTime = 0;
          audio.play();
        }
      }
    });
  };

  onMounted(() => {
    fetchCones();
    connectSocket();
  });

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
