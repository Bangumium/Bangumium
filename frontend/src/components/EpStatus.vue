<script setup lang="ts">
import { ref } from 'vue';

const isLoading = ref(true)
const isBook = ref(false)
const subject_id = ref(0)

function setSubjectId(id: number, book_type: boolean = false) {
  isLoading.value = true
  subject_id.value = id
  if (!book_type) {
    window.pywebview.api.getEpisodeStatusBySubjectId(id).then((result) => {
      if (result.data) {
        episodes.value = result.data
      }

      isLoading.value = false
    })
  } else {

    isBook.value = true
    window.pywebview.api.getCollectStatusBySubjectId(id).then((result) => {
      volStatus.value = result.vol_status
      isLoading.value = false
    })
  }
}

const episodes = ref([])
const volStatus = ref(0)

defineExpose({
  setSubjectId
})

function handleHoverOnEp() {
  const tip = (event.target as HTMLElement).querySelector('.ep_tip') as HTMLElement
  tip.style.display = 'block'
}

function handleMouseLeaveOnEp() {
  const tip = (event.target as HTMLElement).querySelector('.ep_tip') as HTMLElement
  tip.style.display = 'none'
}

function changeEpStatus(ep_id, type) {
  isLoading.value = true
  window.pywebview.api.changeEpisodeStatus(ep_id, type).then((result) => {
  }).finally(() => {
    setSubjectId(episodes.value[0].episode.subject_id)
  })
}

function completedAllBeforeEp(subject_id, ep_id) {
  isLoading.value = true
  window.pywebview.api.completedAllBeforeEp(subject_id, ep_id).then((result) => {
  }).finally(() => {
    setSubjectId(subject_id)
  })
}

function handleBlurOnInput() {
  isLoading.value = true
  window.pywebview.api.updateVolStatus(subject_id.value, volStatus.value).then((result) => {
  }).finally(() => {
    setSubjectId(subject_id.value, true)
  })
}
</script>
<template>
  <div class="bg-base-200" style="padding: 24px;margin-bottom: 20px; border-radius: 20px;"
    v-show="episodes.length > 0 || isLoading || (isBook && isLoading === false)">
    <div v-if="isLoading">
      <p><span class="loading loading-spinner loading-md"></span> 正在获取章节收藏状态</p>
    </div>
    <div v-else class="prose" style="margin-bottom: 0;">
      <p>观看进度管理：</p>
      <span v-if="isBook === false">
        <span v-for="(ep, index) of episodes" :key="index" @mouseenter="handleHoverOnEp"
          @mouseleave="handleMouseLeaveOnEp" style="position: relative; display: inline-block;">
          <a href="javascript:void(0)" style="text-decoration: none;">
            <div class="ep-card" :class="`ep-card-${ep.type}`">{{ parseInt(ep.episode.ep) < 10 ? '0' : '' }}{{
              ep.episode.ep }}</div>
          </a>
          <div style="position: absolute; padding: 3px 8px; border-radius: 8px; width: 250px; display: none;z-index: 3;"
            class="ep_tip shadow-md bg-base-100">
            <p><b>ep.{{ ep.episode.ep }} {{ ep.episode.name }}</b></p>
            <p>
              <a href="javascript:void(0)" @click="() => { changeEpStatus(ep.episode.id, 2) }">看过</a> |
              <a href="javascript:void(0)"
                @click="() => { completedAllBeforeEp(ep.episode.subject_id, ep.episode.id) }">看到</a> |
              <a href="javascript:void(0)" @click="() => { changeEpStatus(ep.episode.id, 1) }">想看</a> |
              <a href="javascript:void(0)" @click="() => { changeEpStatus(ep.episode.id, 3) }">抛弃</a><span
                v-if="ep.type !== 0">
                | <a href="javascript:void(0)" @click="() => { changeEpStatus(ep.episode.id, 0) }">撤销</a>
              </span>
            </p>
          </div>
          &nbsp;
        </span>

      </span>

      <span v-else>
        <input type="text" placeholder="chapter" class="input input-bordered w-full max-w-xs" v-model="volStatus" @blur="handleBlurOnInput" /> / ??
      </span>
    </div>
  </div>
</template>

<style scoped>
.ep-card {
  padding: 2px 5px;
  border: 1px solid grey;
  background-color: #e0e0e0;
  display: inline-block;
  color: #909090;
  margin-bottom: 6px !important;
}

.ep-card:hover {
  font-weight: bold;
  border-top-width: 2px;
}

.ep-card-2 {
  background-color: #4897ff;
  color: white;
  border-color: #1175a8;
}

.ep-card-1 {
  background-color: #ffadd1;
  color: #ff2293;
  border-color: #ff2293;
}

.ep-card-3 {
  background-color: #ccc;
  color: #fff;
  border-color: #666;
  text-decoration: line-through;
}
</style>
