<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavbarComponent from './components/NavbarComponent.vue';
import { applyCurrentTheme, execAfterPywebviewLoaded, triggerOnceTimelineCheck } from './functions';

execAfterPywebviewLoaded(() => {
  triggerOnceTimelineCheck();
  setInterval(() => {
    triggerOnceTimelineCheck();
  }, 300000);
  applyCurrentTheme();
})
</script>

<template>
  <NavbarComponent></NavbarComponent>
  <RouterView :key="$route.fullPath" />
</template>
