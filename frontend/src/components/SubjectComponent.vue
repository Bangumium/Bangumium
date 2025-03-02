<script lang="ts" setup>
import router from '@/router';
import type { Subject } from '@/types'

defineProps({
  subject: {
    type: Object as () => Subject,
    required: true
  }
})
</script>

<template>
  <div class="card shadow-xl">
    <img class="absolute inset-0 w-full h-full object-cover shadow-xl" style="border-radius: 20px;"
      :style="`background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url(${subject.image}); background-position: center center; background-repeat: no-repeat; background-size: cover;`" />
    <div class="relative card-body text-white">

      <h2 class="text-white" style="font-weight:normal;">
        {{ subject.name }} <span class="text-sm">{{ subject.name_cn }}</span>

      </h2>
      <div>
        <div class="badge badge-secondary">{{ subject.platform ? subject.platform : "未知类别" }}</div>&nbsp;
        <div class="badge badge-accent">{{
          subject.date ? subject.date : "未知日期" }}</div>&nbsp;
        <div class="badge badge-primary">Rank: #{{ subject.rating.rank ? subject.rating.rank : "无排名" }}</div>
        &nbsp;
        <div class="badge badge-secondary">Score: {{ subject.rating.score ? subject.rating.score : "无分数" }}★
        </div>
      </div>
      <p style="display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
          text-overflow: ellipsis;">
        {{ subject.summary }}</p>
      <div class="card-actions justify-end" @click="router.push({ name: 'subject', params: { id: subject.id } })">
        <button class="btn btn-primary">查看详情</button>
      </div>
    </div>
  </div>
  <br />
</template>
