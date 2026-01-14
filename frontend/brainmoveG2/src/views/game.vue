<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import io from 'socket.io-client';
import { X } from 'lucide-vue-next';

const Ip = `${window.location.hostname}:8000`;
const route = useRoute();
const router = useRouter();
const gameId = ref(route.params.id);
const showCountdown = ref(true);
const countdownValue = ref(3);
const currentRound = ref(0);
const currentColor = ref('');
const backgroundColor = ref('var(--grey-2)');
let socket = null;

const startCountdown = () => {
    const interval = setInterval(() => {
        if (countdownValue.value > 1) {
            countdownValue.value--;
        } else if (countdownValue.value === 1) {
            countdownValue.value = 0; // Show "GO!"
            setTimeout(() => {
                showCountdown.value = false;
                clearInterval(interval);
                // Start the game after countdown
                startGame();
            }, 1000);
        }
    }, 1000);
};

const startGame = async () => {
    try {
        const response = await fetch(`http://${Ip}/games/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        console.log('Game started:', data);
    } catch (error) {
        console.error('Error starting game:', error);
    }
};

const connectSocket = () => {
    socket = io(`http://${Ip}`);
    
    socket.on('connect', () => {
        console.log('Socket connected:', socket.id);
    });
    
    socket.on('round_start', (data) => {
        console.log('Round started:', data);
        currentRound.value = data.round;
        currentColor.value = data.color;
        
        // Change background color based on received color
        const colorMap = {
            'blue': 'var(--blue)',
            'green': 'var(--accent-green)',
            'orange': 'var(--accent-orange)',
            'red': 'var(--red)',
            'yellow': 'var(--yellow)'
        };
        backgroundColor.value = colorMap[data.color.toLowerCase()] || 'var(--grey-2)';
    });
    
    socket.on('round_result', (data) => {
        console.log('Round result:', data);
        // Reset background after result
        backgroundColor.value = 'var(--grey-2)';
    });
    
    socket.on('game_over', (data) => {
        console.log('Game over:', data);
        // Parse the JSON string and navigate to game overview page with stats
        const gameStats = JSON.parse(data);
        router.push({
            name: 'gameoverzicht',
            params: { id: gameId.value },
            state: { gameStats }
        });
    });
    
    socket.on('disconnect', () => {
        console.log('Socket disconnected');
    });
};

const recordHit = async (coneId) => {
    try {
        const response = await fetch(`http://${Ip}/games/hit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                cone_id: coneId,
                color: currentColor.value
            })
        });
        const data = await response.json();
        console.log('Hit recorded:', data);
    } catch (error) {
        console.error('Error recording hit:', error);
    }
};

onMounted(() => {
    startCountdown();
    connectSocket();
});

onUnmounted(() => {
    if (socket) {
        socket.disconnect();
    }
});

</script>

<template>
    <header class="c-header">
    <div class="c-game-header">
      <button @click="stopGame" class="c-stop-button" aria-label="Stop game">
        <X :size="24" />
        <span>Stoppen</span>
      </button>
      <span class="c-round-counter">{{ currentRound }}/{{ totalRounds }}</span>
    </div>
  </header>
    <main class="c-content-wrapper" :style="{ backgroundColor: backgroundColor }">
        <!-- Countdown Overlay -->
        <div v-if="showCountdown" class="c-countdown-overlay"/>
        <!-- Countdown Overlay -->
        <div v-if="showCountdown" class="c-countdown-overlay">
            <div class="c-countdown-number" v-if="countdownValue > 0">
                {{ countdownValue }}
            </div>
            <div class="c-countdown-go" v-else>
                GO!
            </div>
        </div>
    </main>
</template>

<style scoped>

.c-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: var(--spacing-06);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--white);
}

.c-game-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.c-stop-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--grey-85);
  padding: var(--spacing-03);
  display: flex;
  align-items: center;
  gap: var(--spacing-02);
  font-family: inherit;
  font-size: var(--font-size-3);
  transition: color 0.3s ease;
}

.c-stop-button:hover {
  color: var(--red);
}

.c-round-counter {
  font-size: var(--font-size-3);
  color: var(--grey-85);
  font-weight: var(--font-weight-medium);
}

.c-countdown-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.c-countdown-number {
    font-family: "Bebas Neue", sans-serif;
    font-size: var(--font-size-22);
    color: var(--white);
    font-weight: var(--font-weight-bold);
    animation: countdownPulse 1s ease-in-out;
}

.c-countdown-go {
    font-family: "Bebas Neue", sans-serif;
    font-size: var(--font-size-20);
    color: var(--accent-green);
    font-weight: var(--font-weight-bold);
    animation: goPulse 1s ease-in-out;
}

@keyframes countdownPulse {
    0% {
        transform: scale(0.5);
        opacity: 0;
    }
    50% {
        transform: scale(1.2);
        opacity: 1;
    }
    100% {
        transform: scale(1);
        opacity: 1;
    }
}

@keyframes goPulse {
    0% {
        transform: scale(0.5);
        opacity: 0;
    }
    50% {
        transform: scale(1.3);
        opacity: 1;
    }
    100% {
        transform: scale(1.1);
        opacity: 1;
    }
}
</style>