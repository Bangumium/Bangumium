<script setup lang="ts">
import SubjectComponent from '@/components/SubjectComponent.vue';
import type { Subject } from '@/types';
import { ref } from 'vue';

const keyword = ref('')
const searchResult = ref([])
const isSearching = ref(false)

function searchSubjectByKeyword() {
  isSearching.value = true
  searchResult.value = []
  window.pywebview.api.searchSubjectByKeyword(keyword.value).then((result) => {
    isSearching.value = false
    searchResult.value = result.data as Subject[]
  })
}


</script>

<template>
  <div class="container mx-auto prose">
    <article class="prose">
      <h1>搜索</h1>
      <input type="text" placeholder="搜索条目关键词" class="input input-bordered w-full max-w-xs" v-model="keyword"
        @keydown.enter="searchSubjectByKeyword" />&nbsp;
      <button class="btn btn-secondary" :class="isSearching ? 'btn-disabled' : ''" @click="searchSubjectByKeyword"><span
          v-if="isSearching === false"><font-awesome-icon icon="fa-solid fa-magnifying-glass" /> 搜索 </span>
        <span v-else><font-awesome-icon icon="fa-solid fa-spinner" spin /> 搜索中...</span>
      </button>
      <p style="color: grey;">小提示：可以按 <kbd class="kbd" style="color: grey">Enter</kbd> 来进行搜索</p>
    </article>
    <br />
    <div class="flex w-full flex-col gap-4" v-if="isSearching">
      <div class="skeleton h-32 w-64"></div>
      <div class="skeleton h-4 w-full"></div>
      <div class="skeleton h-4 w-full"></div>
      <div class="skeleton h-4 w-full"></div>
    </div>
    <div v-for="subject in searchResult" :key="subject.id">
      <SubjectComponent :subject="subject"></SubjectComponent>

      <br />
    </div>
  </div>
</template>
