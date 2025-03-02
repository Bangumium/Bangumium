<script setup lang="ts">
import { ref } from 'vue'
import { execAfterPywebviewLoaded } from '@/functions'
import TimelineItemComponent from '@/components/TimelineItemComponent.vue';

const timeline = ref([])
const isLoading = ref(true)

function load(page = 1) {
  window.pywebview.api.getIndexTimeline(page).then((result) => {
    if (result['error'] && result['error'] === 'Unauthorized') {
      window.location.reload();
    }
    timeline.value = timeline.value.concat(result)
    isLoading.value = false
  })
}

execAfterPywebviewLoaded(() => {
  load();
})

const page = ref(1)

function loadMore() {
  isLoading.value = true
  page.value += 1
  load(page.value)
}

</script>

<template>
  <div class="bg-base-300">
    <div style="display: block;" class="mx-auto w-2/3 container">
      <br /><br />
      <div class="prose">

        <h1>好友的时间线</h1>
      </div>
      <br /><br />
    </div>
    <div class="bg-base-200" style="min-height: 75vh;">
      <div class="mx-auto container">
        <div style="border-radius: 20px; text-align: center;">
          <TimelineItemComponent v-for="item in timeline" :key="item.uuid" :item="item">
          </TimelineItemComponent>
          <br />
          <div v-if="isLoading === false && timeline.length !== 0">

            <button class="btn btn-wide btn-outline btn-primary" @click="loadMore">加载更多</button>
            <br /><br /><br /><br /><br />
          </div>
        </div>
        <div v-if="isLoading" class="mx-auto w-3/4">
          <br /><br />
          <p><span class="loading loading-spinner loading-md"></span> 正在获取时间线。。。</p>
          <br /><br />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
