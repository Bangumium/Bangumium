<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import router from '@/router';
defineProps({
  item: {
    type: Object,
    required: true
  }
})

const enterTarget = (target: any) => {
  if (target.type === 'subject') {
    router.push({ name: 'subject', params: { id: target.id } })
  } else if (target.type === "user") {
    router.push({ name: 'user', params: { username: target.id } })
  }
}
</script>

<template>
  <div class="card bg-base-100 shadow-xl"
    style="display: inline-block!important; margin: 20px; width: 20%;text-align: left; min-width: 250px;">
    <div class="relative card-body">
      <h2 class="card-title" style="font-weight:normal; cursor: pointer;"
        @click="() => { enterTarget({ 'type': 'user', 'id': item.username }) }">
        <div class="avatar">
          <div class="rounded-full" style="height: 50px; width: 50px;">
            <img :src="item.avatar" />
          </div>
        </div>{{ item.userNickname }}
      </h2>
      <span v-if="item.target.length > 0">
        <p class="prose">{{ item.verb }} <a href="javascript:void(0)" @click="() => { enterTarget(item.target[0]) }">{{
          item.target[0].name }}</a> <span v-if="item.a_of_b">{{ item.a_of_b }}</span><span
            v-if="item.target.length > 1">
            (<a href="javascript:void(0)" @click="() => { enterTarget(item.target[1]) }">{{ item.target[1].name }}</a>)
          </span></p>
      </span>
      <div style="padding: 10px;" class="bg-base-200 rounded-xl" v-if="item.comment !== null || item.rating !== null">
        <div class="badge badge-secondary" v-if="item.rating !== null">{{ item.rating }}/10★</div>
        <p class="prose" style="margin: 0;" v-if="item.comment !== null">{{ item.comment }}</p>
      </div>

      <p><small><font-awesome-icon icon="fa-solid fa-clock" /> {{ item.date }}</small></p>
    </div>
  </div>
</template>

<style scoped>
.card:hover {
  transform: scale(1.05);
  transition: transform 0.2s;
}

a {
  color: oklch(var(--p))
}
</style>
