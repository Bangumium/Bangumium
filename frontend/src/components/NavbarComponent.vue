<script setup lang="ts">
import { ref } from 'vue'
import { execAfterPywebviewLoaded } from '@/functions'
import router from '@/router'
import { useRoute } from 'vue-router'

const appName = ref('')

execAfterPywebviewLoaded(() => {
  window.pywebview.api.getAppName().then((appNameResult: string) => {
    appName.value = appNameResult
  })
  loadAccountInfo()
})

const loginAttemptStatus = ref('NONE')

const accountInfo = ref({
  is_logged_in: false,
  cookies: '',
  oauthToken: ''
})

const userInfo = ref({
  'avatar': {}
})

function loadAccountInfo() {
  window.pywebview.api.getLogin().then((result) => {
    accountInfo.value = result
    if (result.is_logged_in) {
      window.pywebview.api.getUserInfo().then((userInfoResult) => {
        if (userInfoResult['error'] === "Unauthorized") {
          accountInfo.value['is_logged_in'] = false
          window.location.reload()
        }

        if(!userInfoResult) {
          // run into weird error, force reload required
          window.location.reload()
        }

        userInfo.value = userInfoResult
      })
    } else {
      showLoginModal()
    }
  })
}

function loginBangumiAccount() {
  window.pywebview.api.startBangumiLogin()
  const intervalIdOfCheckingLoginStatus = setInterval(() => {
    window.pywebview.api.queryLoginAttemptStatus().then((loginStatus: string) => {
      loginAttemptStatus.value = loginStatus
      if (loginAttemptStatus.value === 'SUCCESS' || loginAttemptStatus.value === 'FAILED') {
        clearInterval(intervalIdOfCheckingLoginStatus)
      }

      if (loginAttemptStatus.value === 'SUCCESS') {
        document.getElementById('require_login_modal')?.close()
        window.location.reload()
      }
    })
  }, 1000)
}

const route = useRoute()

function showLoginModal() {
  loginAttemptStatus.value = 'NONE'
  document.getElementById('require_login_modal')?.showModal()
}

function exitLogin() {
  window.pywebview.api.exitLogin().then(() => {
    window.location.reload()
  })
}


</script>

<template>
  <div class="navbar bg-base-100 fixed z-10">
    <div class="flex-1">
      <a class="btn btn-ghost text-xl" @click="router.push('/')">{{ appName }}</a>
    </div>
    <div class="flex-none">
      <ul class="menu menu-horizontal px-1 menu-md" style="justify-items: center; align-items: center;">
        <li><a @click="router.push('/')" :class="route.fullPath === '/' ? 'active' : ''">时间线</a></li>
        <li><a @click="router.push('/progress')" :class="route.fullPath === '/progress' ? 'active' : ''">进度管理</a>
        </li>


        <li><a class="text-lg" @click="router.push('/search')"
            :class="route.fullPath === '/search' ? 'active' : ''"><font-awesome-icon
              icon="fa-solid fa-magnifying-glass" /></a></li>
        <li><a class="text-lg" :class="route.fullPath === '/settings' ? 'active' : ''"
            @click="router.push('/settings')"><font-awesome-icon icon="fa-solid fa-gear" /></a></li>
        <li v-if="!accountInfo.is_logged_in">
          <div class="dropdown dropdown-bottom dropdown-end">
            <div tabindex="0">
              <div class="avatar">
                <div class="w-12 rounded-full border-secondary  border-2">
                  <img src="/Akkarin.webp" />
                </div>
              </div>
            </div>
            <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] w-52 p-2 shadow">
              <li><a @click="showLoginModal">登录 Bangumi 账户</a></li>
            </ul>
          </div>
        </li>
        <li v-if="accountInfo.is_logged_in">
          <div class="dropdown dropdown-bottom dropdown-end">
            <div tabindex="0">
              <div class="avatar">
                <div class="w-12 rounded-full border-secondary  border-2">
                  <img :src="userInfo.avatar.medium" />
                </div>
              </div>
            </div>
            <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] w-80 shadow">
              <li><a @click="router.push({ name: 'user', params: { username: userInfo.username } })">
                  <div style="display: flex;">
                    <div class="avatar">
                      <div class="w-16 rounded-full border-secondary  border-2">
                        <img :src="userInfo.avatar.medium" />
                      </div>
                    </div>
                    &nbsp;&nbsp;
                    <span><span class="text-lg">{{ userInfo.nickname }}</span><br />
                      <span>{{ userInfo.sign }}</span></span>
                  </div>
                </a></li>
              <li><a @click="router.push({ name: 'user', params: { username: userInfo.username } })">用户主页</a></li>
              <!--
              <li><a @click="router.push(`/user/${userInfo.username}/collections`)">收藏</a></li>
              <li><a @click="router.push(`/user/${userInfo.username}/mono`)">人物</a></li>
              <li><a @click="router.push(`/user/${userInfo.username}/blog`)">日志</a></li>
              <li><a @click="router.push(`/user/${userInfo.username}/index`)">目录</a></li>
              <li><a @click="router.push(`/user/${userInfo.username}/timeline`)">时间胶囊</a></li>
              <li><a @click="router.push(`/user/${userInfo.username}/groups`)">小组</a></li>
              <li><a @click="router.push(`/user/${userInfo.username}/friends`)">好友</a></li>
              <li><a @click="router.push(`/user/${userInfo.username}/wiki`)">维基</a></li>
              -->
              <hr />
              <li><a @click="exitLogin">退出登录</a></li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
  </div>
  <br /><br /><br /><br />
  <dialog id="require_login_modal" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">你还未登录</h3>
      <p class="py-4">要继续使用本程序，你需要登录 Bangumi 账号</p>
      <div role="alert" class="alert" v-if="loginAttemptStatus !== 'NONE'">
        <span v-if="loginAttemptStatus === 'PENDING'"><span class="loading loading-spinner loading-md"></span>
          等待用户登录中</span>
        <span v-if="loginAttemptStatus === 'OPERATING'"><span class="loading loading-spinner loading-md"></span>
          正在校验登录状态，请稍候 [此操作需要一段时间，请耐心等待]</span>
        <span v-if="loginAttemptStatus === 'OAUTH_PENDING'"><span class="loading loading-spinner loading-md"></span>
          等待用户完成OAuth中</span>
        <span v-if="loginAttemptStatus === 'OPERATING_OAUTH'"><span class="loading loading-spinner loading-md"></span>
          正在尝试完成登录，请稍候 [此操作需要一段时间，请耐心等待]</span>
        <span v-if="loginAttemptStatus === 'FAILED'" style="color: red;"><font-awesome-icon icon="fa-solid fa-xmark" />
          登录失败，请重新尝试</span>
        <span v-if="loginAttemptStatus === 'SUCCESS'" style="color: green;"><font-awesome-icon
            icon="fa-solid fa-check" />
          登录成功</span>
      </div>
      <div class="modal-action">


        <button class="btn btn-secondary" @click="loginBangumiAccount"
          :disabled="loginAttemptStatus !== 'NONE' && loginAttemptStatus !== 'SUCCESS' && loginAttemptStatus !== 'FAILED'">登录
          Bangumi
          账户</button>
      </div>
    </div>
  </dialog>
</template>
