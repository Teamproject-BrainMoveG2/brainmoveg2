<script setup>
import { RouterView, useRoute } from 'vue-router';
import { computed } from 'vue';
import Navbar from './components/navigatie/Navbar.vue';
import Header from './components/navigatie/Header.vue';

const route = useRoute();
const showNavbar = computed(() => route.meta.showNavbar !== false);
const showHeader = computed(() => route.meta.showHeader !== false);
</script>


<template>
    <transition name="fade" mode="out-in">
        <div :key="route.fullPath" class="page-content">
            <Header v-if="showHeader" />
            <div :style="showNavbar ? 'padding-bottom: 100px;' : ''">
                <RouterView />
            </div>
        </div>
    </transition>
    <Navbar v-if="showNavbar" />
</template>

<style>

.page-content {
    width: 100%;
    height: 100%;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>

