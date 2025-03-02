<script lang="ts" setup>
import EditCollectStatusModal from '@/components/EditCollectStatusModal.vue';
import RatingBarChart from '@/components/RatingBarChart.vue';
import { execAfterPywebviewLoaded } from '@/functions';
import router from '@/router';
import { nextTick, ref } from 'vue';
import { getEditCollectVerbList } from '@/functions';
import EpStatus from '@/components/EpStatus.vue';

const epStatus = ref(null);

const id = ref(router.currentRoute.value.params.id);
const subject = ref({});
const isLoaded = ref(false);
const verbList = ref(getEditCollectVerbList(1));

execAfterPywebviewLoaded(() => {
  window.pywebview.api.getSubjectById(id.value).then((result) => {
    subject.value = result;
    isLoaded.value = true;
    verbList.value = getEditCollectVerbList(subject.value.type);
    nextTick(() => {
      epStatus.value.setSubjectId(id.value);
    });
    meta_tags.value = [...new Set(result.meta_tags)];
  });
});

const translatedSummary = ref(null);
const isTranslating = ref(false)

function translateIntro() {
  translatedSummary.value = "正在翻译...";
  isTranslating.value = true
  window.pywebview.api.translateText(subject.value.summary).then((result) => {
    translatedSummary.value = result;
  }).catch(() => {
    translatedSummary.value = "翻译失败";
  }).finally(() => {
    isTranslating.value = false
  });
}

function closeTranslation() {
  translatedSummary.value = null;
}

const editCollectStatusModal = ref(null);


const editCollectStatus = () => {
  editCollectStatusModal.value.openModal();
  editCollectStatusModal.value.setSubject(id.value, subject.value);
}

const isLoadingCollectionBox = ref(true);
const collectionType = ref(0);
const collectionDate = ref('');

window.pywebview.api.getCollectStatusBySubjectId(router.currentRoute.value.params.id).then((result) => {
  isLoadingCollectionBox.value = false;
  if (result.error) {

    isLoadingCollectionBox.value = false;
    collectionType.value = 0;
  } else {

    collectionType.value = result.type;
    collectionDate.value = result.updated_at
  }
}).catch(() => {
  isLoadingCollectionBox.value = false;
  collectionType.value = 0;
});

const meta_tags = ref([]);

</script>
<template>
  <div class="container mx-auto px-8">

    <br />
    <div v-if="!isLoaded">
      <div class="w-full">
        <div class="skeleton h-64 w-1/3" style="display: inline-block;"></div>
        &nbsp;&nbsp;&nbsp;
        <div class="skeleton h-64 w-1/4" style="display: inline-block;"></div>
        <br /><br />
        <div class="skeleton h-12 w-1/2"></div>
        <br />
        <div class="skeleton h-12 w-1/2"></div>
      </div>

    </div>
    <div v-if="isLoaded">
      <div class="prose" style="max-width: 100%;;">

        <h1>{{ subject.name }} <small>{{ subject.name_cn }}</small></h1>
        <br />
      </div>
      <div class="grid grid-cols-4 gap-4">
        <div class="">
          <img :src="subject.images.common" />
          <div class="overflow-x-auto">
            <table class="table">
              <!-- head -->
              <thead>
                <tr>
                  <th></th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr class="hover" v-for="(info, index) of subject.infobox" :key="index">
                  <td>{{ info.key }}</td>
                  <td><span v-if="typeof (info.value) === 'string'">{{ info.value }}</span><span v-else>
                      <span v-for="(value, index) of info.value" :key="index">
                <tr>
                  <td v-if="value.k">{{ value.k }}</td>
                  <td>{{ value.v }}</td>
                </tr></span>
                </span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="col-span-2">
          <EpStatus ref="epStatus"></EpStatus>
          <div>
            {{ subject.summary }}
          </div>
          <br />
          <a class="link link-primary" @click="translateIntro" v-if="translatedSummary === null">翻译简介到中文</a>
          <a class="link link-primary" @click="closeTranslation"
            v-if="translatedSummary !== null && isTranslating === false">关闭翻译</a>
          <br />
          <div v-if="translatedSummary">
            <br />
            <div class="bg-base-200 border-xl border-2 rounded-lg p-4">
              {{ translatedSummary }}
              <br /><br />
              <b v-if="isTranslating === false">以上翻译由 Google 翻译提供</b>
            </div>
          </div>
          <br />
          <div class="px-4 py-4 bg-base-200 rounded-lg prose">
            <h3>大家把 {{ subject.name }} 标注为</h3>
            <div class="badge badge-secondary" v-for="(tag, index) of meta_tags" :key="index" style="margin-right:5px">
              {{ tag }}</div>
            <div class="badge badge-default" v-for="(tag, index) of subject.tags" :key="index" style="margin-right:5px">
              {{ tag.name }} <small>{{ tag.count }}</small></div>
          </div>
        </div>
        <div>
          <div class="px-4 py-4 bg-base-200 rounded-lg prose">
            <h2>收藏盒</h2>
            <div>
              <div v-if="isLoadingCollectionBox">
                <div class="loading loading-lg"></div>
              </div>
              <div v-else>
                <div v-if="collectionType === 0">
                  <button class="btn btn-primary btn-outline btn-sm" @click="editCollectStatus">{{ verbList[0]
                    }}</button>&nbsp;
                  <button class="btn btn-primary btn-outline btn-sm" @click="editCollectStatus">{{ verbList[1]
                    }}</button>&nbsp;
                  <button class="btn btn-primary btn-outline btn-sm" @click="editCollectStatus">{{ verbList[2]
                    }}</button>&nbsp;
                  <button class="btn btn-primary btn-outline btn-sm" @click="editCollectStatus">{{ verbList[3]
                    }}</button>&nbsp;
                  <button class="btn btn-primary btn-outline btn-sm" @click="editCollectStatus">{{ verbList[4]
                    }}</button>
                </div>
                <div v-else>
                  我{{ getEditCollectVerbList(subject.type)[collectionType - 1] }}这部作品 <a href="javascript:void(0)"
                    @click="editCollectStatus">修改</a>
                  <br />
                  {{ collectionDate }}
                </div>
              </div>

            </div>
          </div>
          <br />

          <div class="rounded-lg bg-base-200"
            style="font-size: xx-large;padding: 12px 12px;display: inline-block; border: 2px solid oklch(var(--s))">{{
              subject.rating.score }}</div>
          <div style="display: inline-block; margin-left: 20px">
            <p><span style="color: grey">Bangumi Ranked #</span><b>{{
              subject.rating.rank
                }}</b></p>
            <p><b>{{ subject.rating.total }}</b> votes</p>
          </div>
          <RatingBarChart :chart-data="Object.values(subject.rating.count)"></RatingBarChart>
          <EditCollectStatusModal ref="editCollectStatusModal"></EditCollectStatusModal>
        </div>
      </div>
    </div>
  </div>
</template>
