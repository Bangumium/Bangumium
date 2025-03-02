<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavbarComponent from './components/NavbarComponent.vue';
import { applyCurrentTheme, execAfterPywebviewLoaded } from './functions';

execAfterPywebviewLoaded(() => {

  applyCurrentTheme();
})
</script>

<template>
  <NavbarComponent></NavbarComponent>
  <RouterView :key="$route.fullPath" />
</template>
