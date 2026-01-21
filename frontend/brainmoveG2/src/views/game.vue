<script setup>

import { onMounted, onUnmounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CloseButton from '../components/buttons/CloseButton.vue';
import io from 'socket.io-client';

const Ip = `${window.location.hostname}:8000`;
const route = useRoute();
const router = useRouter();
const gameId = ref(route.params.id);

const showCountdown = ref(true);
const countdownValue = ref(3);
const currentRound = ref(0);
const currentColor = ref('');
const backgroundColor = ref('var(--grey-2)');
const showResultOverlay = ref(false);
const roundResult = ref('');
const totalRounds = ref(0);
let socket = null;

const colorMap = {
            'blue': 'var(--blue)',
            'green': 'var(--accent-green)',
            'orange': 'var(--accent-orange)',
            'red': 'var(--red)',
            'yellow': 'var(--yellow)'
        };

const settings = route.query;
console.log('Received game settings from previous page:', JSON.stringify(settings, null, 2));

const startCountdown = () => {
    const interval = setInterval(() => {
        if (countdownValue.value > 1) {
            countdownValue.value--;
        } else if (countdownValue.value === 1) {
            countdownValue.value = 0; 
            setTimeout(() => {
                showCountdown.value = false;
                clearInterval(interval);
  
                startGame();
            }, 1000);
        }
    }, 1000);
};

const stopGame = async () => {
    try {
        await fetch(`http://${Ip}/games/stop`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
    } catch (error) {
        console.error('Error stopping game:', error);
    }
    if (socket) {
        socket.disconnect();
    }
    router.push({ name: 'dashboard' });
};

const startGame = async () => {
    try {
        const response = await fetch(`http://${Ip}/games/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: settings.username || 'speler',
                mode_id: settings.mode_id,
                difficulty_id: settings.difficulty_id,
                aantal_rondes: settings.aantal_rondes,
                aantal_kleuren: settings.aantal_kleuren
            })
        });
        const data = await response.json();
        console.log('Game started:', data);
    } catch (error) {
        console.error('Error starting game:', error);
    }
};

const connectSocketColorGames = () => {
    socket = io(`http://${Ip}`);
    
    socket.on('connect', () => {
        console.log('Socket connected:', socket.id);
    });
    
    socket.on('round_start', (data) => {
        console.log('Round started:', data);
        currentRound.value = data.round;
        currentColor.value = data.color;
        totalRounds.value = data.max_rounds;

        showResultOverlay.value = false;
      
        backgroundColor.value = colorMap[data.color?.toLowerCase()] || 'var(--grey-2)';
    });

    socket.on('user_round_start', (data) => {
        // Show a message or overlay indicating the user is playing
        console.log('Round result:', data);
        roundResult.value = "bezig met spelen";
        showResultOverlay.value = true;
        backgroundColor.value = 'var(--grey-2)';
    });
    
    socket.on('round_result', (data) => {
        console.log('Round result:', data);
        roundResult.value = data.result;
        showResultOverlay.value = true;
   
        backgroundColor.value = 'var(--grey-2)';
    });
    
    socket.on('game_over', (data) => {
        console.log('Game over:', data);
     
        setTimeout(() => {
          
            const gameStats = JSON.parse(data);
            router.push({
                name: 'gameoverzicht',
                params: { id: gameId.value },
                state: { gameStats }
            });
        }, 2000);
    });
    
    socket.on('disconnect', () => {
        console.log('Socket disconnected');
    });
};

const connectSocketMemoryGames = () => {
    socket = io(`http://${Ip}`);

    socket.on('connect', () => {
        console.log('Socket connected:', socket.id);
    });

    socket.on('round_start', (data) => {
        console.log('Round started:', data);
        currentRound.value = data.round;
        currentColor.value = data.color;
        totalRounds.value = data.max_rounds;

        showResultOverlay.value = false;
      
        backgroundColor.value = colorMap[data.color?.toLowerCase()] || 'var(--grey-2)';
    });

    

    socket.on('game_over', (data) => {
        console.log('Game over:', data);
        setTimeout(() => {
            const gameStats = JSON.parse(data);
            router.push({
                name: 'gameoverzicht',
                params: { id: gameId.value },
                state: { gameStats }
            });
        }, 2000);
    });

    socket.on('disconnect', () => {
        console.log('Socket disconnected');
    });
};

onMounted(() => {
    startCountdown();
    connectSocketColorGames();
    
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
     <CloseButton @close="stopGame"/>
      <span class="c-round-counter">{{ currentRound }}/{{ totalRounds }}</span>
    </div>
  </header>
    <main class="u-viewport-height" :style="{ backgroundColor: backgroundColor }">
        <div v-if="showCountdown" class="c-countdown-overlay">
            <div class="c-countdown-number" v-if="countdownValue > 0">
                {{ countdownValue }}
            </div>
            <div class="c-countdown-go" v-else>
                GO!
            </div>
        </div>
        <div v-if="showResultOverlay" class="c-result-overlay">
            <div class="c-result-text" :class="`c-result-${roundResult}`">
                {{ roundResult.toUpperCase() }}
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
  justify-content: center;
  align-items: center;
  background-color: var(--white);
}

.c-game-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
    max-width: 26.25rem;

   @media (min-width: 768px) {

    max-width: 500px;
    gap: var(--spacing-08);

  }

  @media (min-width: 1024px) {

      max-width: 550px;
      gap: var(--spacing-09);

  }
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

.c-result-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.c-result-text {
    font-family: "Bebas Neue", sans-serif;
    font-size: var(--font-size-22);
    font-weight: var(--font-weight-bold);
    animation: resultPulse 0.5s ease-in-out;
    color: var(--white); 
}

.c-result-goed {
    color: var(--accent-green);
}

.c-result-fout {
    color: var(--red);
}

.c-result-gemist {
    color: var(--accent-orange);
}

@keyframes resultPulse {
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
</style>