<script setup lang="ts">
import { ref, nextTick } from 'vue'
import EpStatus from '@/components/EpStatus.vue'
import EditCollectStatusModal from '@/components/EditCollectStatusModal.vue'
import router from '@/router'

const userCollections = ref([])
// 定义一个数组 ref 来收集 EpStatus 组件实例
const epStatusRefs = ref([])

const tab = ref('animation')


const loading = ref(true)

function query() {
  window.pywebview.api.getUserProgress(tab.value === 'animation' ? 2 : tab.value === 'book' ? 1 : null).then((result) => {
    userCollections.value = result.data
    loading.value = false
  })
}

query()

function viewEpStatus(e: Event, id: number, index: number) {
  // 当选项被勾选后
  if ((e.target as HTMLInputElement).checked) {
    nextTick(() => {
      // 从数组中取出对应的组件实例
      const epStatusComponent = epStatusRefs.value[index]
      if (epStatusComponent && typeof epStatusComponent.setSubjectId === 'function') {
        epStatusComponent.setSubjectId(id, tab.value === 'book'?true:false)
      } else {
        console.warn(`找不到 index 为 ${index} 的 EpStatus 组件实例`)
      }
    })
  }
}

const editCollectStatusModal = ref(null)

function editCollectStatus(subjectId, subject) {
  editCollectStatusModal.value.setSubject(subjectId, subject)
  editCollectStatusModal.value.openModal()
}

</script>

<template>

  <div class="mx-auto w-2/3 container">

    <div class="prose">
      <h2>我的进度</h2>
      <br />
    </div>
    <div v-if="loading">
      <span class="loading loading-spinner loading-md"></span>正在获取收藏状态数据
    </div>
    <div v-else>
      <div role="tablist" class="tabs tabs-bordered" style="width:300px">
        <a role="tab" class="tab" :class="tab === 'animation' ? 'tab-active' : ''"
          @click="loading = true; tab = 'animation'; query()">动画</a>

        <a role="tab" class="tab" :class="tab === 'book' ? 'tab-active' : ''"
          @click="loading = true; tab = 'book'; query()">图书</a>
      </div>
      <br />
      <div v-for="(item, index) in userCollections" :key="index">
        <div class="collapse bg-base-200 collapse-arrow" @change="e => viewEpStatus(e, item.subject_id, index)"
          style="overflow: visible !important;">
          <input type="radio" name="user_progress" />
          <div class="collapse-title text-xl font-medium">{{ item.subject.name }}</div>
          <div class="collapse-content">
            <EpStatus class="ep_status" ref="epStatusRefs" />
            <div class="prose" style="padding-left: 20px;display: inline-block;margin-top:0">
              <a href="javascript:void(0)"
                @click="() => { editCollectStatus(item.subject_id, item.subject) }">编辑收藏状态</a> |
              <a href="javascript:void(0)"
                @click="router.push({ name: 'subject', params: { id: item.subject_id } })">前往条目</a>
              <br /><br />
            </div>
          </div>
        </div>
        <br />
      </div>
    </div>

  </div>
  <EditCollectStatusModal ref="editCollectStatusModal" />
</template>
