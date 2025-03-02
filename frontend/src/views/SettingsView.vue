<script setup lang="ts">
import { applyCurrentTheme, execAfterPywebviewLoaded, getCurrentTheme, setCurrentTheme, theme_list } from '@/functions';
import { ref, watch } from 'vue';
import { useToast } from 'vue-toastification';

const enableNotifications = ref(true);
const currentTheme = ref('cupcake')

execAfterPywebviewLoaded(() => {
  window.pywebview.api.getUserData().then((result) => {
    if (Object.keys(result).includes('disableNotifications')) {
      enableNotifications.value = !result['disableNotifications'];
    }

    watch(enableNotifications, (newValue) => {
      if (newValue) {
        window.pywebview.api.enable_notifications().then(() => {
          const toast = useToast();
          toast.success('设置已保存');
        });
      } else {
        window.pywebview.api.disable_notifications().then(() => {
          const toast = useToast();
          toast.success('设置已保存');
        });
      }

    });
  });

  window.pywebview.api.getAppVersion().then((result) => {
    versionNumber.value = result;
  })

  getCurrentTheme().then((result) => {
    currentTheme.value = result;

    watch(currentTheme, (newValue) => {
      setCurrentTheme(newValue);
      const toast = useToast();
      toast.success('设置已保存');
    })
  });

})

const versionNumber = ref('')

function reloadPage() {
  window.location.reload();
}

function clearAllUserData() {
  window.pywebview.api.clearAllUserData().then(() => {
    const toast = useToast();
    toast.success('已清空所有用户数据');
    window.location.reload();
  });
}

function clearAllCache() {
  window.pywebview.api.clearAllCache().then(() => {
    const toast = useToast();
    toast.success('已清空缓存');
  });
}

function openUrl(url: string) {
  window.pywebview.api.openUrl(url);
}


</script>

<template>
  <div class="container mx-auto prose">
    <article class="prose">
      <h1>设置</h1>
      <h2>界面</h2>
      <p>主题</p>
      <div class="form-control">
        <select v-model="currentTheme" class="select select-secondary" style="width: fit-content;">
          <option v-for="theme in theme_list" :key="theme" :value="theme">
            {{ theme }}{{ theme === 'cupcake' ? ' (默认主题)' : '' }}
          </option>
        </select>
      </div>
      <br />
      <h2>通知</h2>
      <div class="form-control">
        <label class="cursor-pointer label" style="width: fit-content;">

          <input type="checkbox" checked="true" class="checkbox checkbox-secondary" style="margin-right: 4px;"
            v-model="enableNotifications" />
          <span class="label-text">在时间线上有新动态时发送系统通知</span>
        </label>
      </div>
      <h2>高级</h2>
      <button class="btn btn-secondary" @click="clearAllUserData">清空所有数据</button>&nbsp;
      <button class="btn btn-secondary" @click="reloadPage">强制刷新界面</button>
      <h2>关于</h2>
      <p>版本：{{ versionNumber }}&nbsp;</p>
      <p>By <a href="javascript:void(0)" @click="openUrl('https://byn.moe/')">柏园猫</a>、<a href="javascript:void(0)"
          @click="openUrl('https://apeiria.net')">Misaka13514</a>、
        <a href="javascript:void(0)" @click="openUrl('https://koishi514.moe')">scientificworld</a>、
        <a href="javascript:void(0)" @click="openUrl('https://chihuo2104.dev')">chihuo2104</a>
      </p>
      <p>软件的源代码使用 MIT 协议开源，本程序不含任何担保。</p>
      <p><a href="javascript:void(0)"
          @click="openUrl('https://github.com/Bangumium/Bangumium')">GitHub</a>&nbsp;|&nbsp;<a href="javascript:void(0)"
          @click="openUrl('https://github.com/Bangumium/Bangumium/issues')">问题反馈</a></p>
    </article>
  </div>
</template>
