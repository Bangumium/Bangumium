<script setup lang="ts">

import { ref } from 'vue';
import { getEditCollectVerbList } from '@/functions';
import router from '@/router';

const props = defineProps<{
  username: string,
  initital_tab?: string
}>()

const tab = ref(props.initital_tab ? props.initital_tab : 'animation')
const currentDataList = ref([])
const loading = ref(true)

const query = function () {
  window.pywebview.api.getUserCollectionListByUsername(props.username, tab.value === 'animation' ? 2 : tab.value === 'game' ? 4 : tab.value === 'book' ? 1 : null).then((result) => {
    currentDataList.value = result.data
    loading.value = false
  })
}
query()
</script>
<template>
  <div role="tablist" class="tabs tabs-bordered" style="width:300px">
    <a role="tab" class="tab" :class="tab === 'animation' ? 'tab-active' : ''"
      @click="loading = true; tab = 'animation'; query()">动画</a>
    <a role="tab" class="tab" :class="tab === 'game' ? 'tab-active' : ''"
      @click="loading = true; tab = 'game'; query()">游戏</a>

    <a role="tab" class="tab" :class="tab === 'book' ? 'tab-active' : ''"
      @click="loading = true; tab = 'book'; query()">图书</a>
  </div>
  <br />
  <div v-if="loading === false">
    <div class="card shadow-lg" v-for="item in currentDataList" :key="item.subject_id">
      <div class="card-body">
        <h2 class="card-title">{{ item.subject.name }} <div class="badge badge-primary">{{
          getEditCollectVerbList(item.subject.type)[item.type - 1] }} </div>

        </h2>

        <div class="prose">
          <p>{{ item.subject.short_summary }}</p>
          <a href="javascript:void(0)"
            @click="router.push({ name: 'subject', params: { id: item.subject_id } })">查看条目详情</a>
        </div>
        <div v-if="item.comment !== null || item.rate !== 0" class="bg-base-300 rounded-xl" style="padding: 20px">
          <p><b>来自 {{ username }} 的评价</b> 于 {{ item.updated_at }}</p>
          <div class="badge badge-secondary" v-if="item.rate !== 0">{{ item.rate }}/10★</div>
          <span v-if="item.comment !== null">{{ item.comment }}</span>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="loading loading-lg"></div>
  </div>
</template>
