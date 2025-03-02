<script setup lang="ts">

import router from '@/router';
import { ref } from 'vue';
import UserCollectionList from '@/components/UserCollectionList.vue';

const username = router.currentRoute.value.params.username;
const loading = ref(true)
const avatar = ref('')
const userNickname = ref('')
const userBio = ref('')
const userInfo = ref({})

window.pywebview.api.getUserInfoByUsername(username).then((result) => {
  avatar.value = result.avatar.large
  userNickname.value = result.nickname
  userBio.value = result.sign
  userInfo.value = result
  loading.value = false
})
</script>

<template>
  <div class="container mx-auto" style="margin-top: 40px; padding: 0px 10%;">

    <div v-if="loading">
      <span class="loading loading-spinner loading-md"></span> 正在获取用户信息
    </div>

    <div v-else>
      <div class="bg-base-200 rounded-xl" style="padding:20px 10%">
        <div class="avatar" style="display: inline-block;">
          <div class="w-24 rounded-full">
            <img :src="avatar" />
          </div>
        </div>
        <div style="display: inline-block; vertical-align: top; margin-left: 20px;">
          <h1 style="font-size: xx-large;">{{ userNickname }} <div class="badge badge-secondary">@{{ userInfo.username
              }}
            </div>
          </h1>
          <p>{{ userBio }}</p>
        </div>


      </div>

      <br />
      <div style="padding:20px 10%">


        <h2 style="font-size: xx-large;">用户收藏</h2>
        <br />
        <UserCollectionList :username="username"></UserCollectionList>
      </div>
    </div>
  </div>
</template>
