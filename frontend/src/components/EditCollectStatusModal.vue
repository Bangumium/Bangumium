<script lang="ts" setup>
import { getEditCollectVerbList, getSubjectType } from '@/functions';
import { ref, onMounted, onUpdated, computed } from 'vue';
import { useToast } from "vue-toastification";

const toast = useToast();

const modalElem = ref<HTMLDialogElement | null>(null);

function openModal() {
  modalElem.value?.showModal();
}

function closeModal() {
  modalElem.value?.close();
}

const loading = ref(true)

const collect_status = ref(1)
const rank = ref(0)
const comment = ref('')
const tag = ref('')

const verbList = ref([])

const collection = ref({})

const isPrivate = ref(false)


function setSubject(id: number, subjectInfoFallback: object) {
  loading.value = true;
  window.pywebview.api.getCollectStatusBySubjectId(id).then((result) => {

    collection.value = result;
    loading.value = false;
    verbList.value = getEditCollectVerbList(result.subject.type);

    collect_status.value = result.type ?? 1;
    rank.value = result.rate ?? 0;
    comment.value = result.comment ?? '';
    tag.value = result.tags.join(',');
    isPrivate.value = result.private ?? false;

  }).catch(() => {
    collection.value = { subject: subjectInfoFallback };
    loading.value = false;
    verbList.value = getEditCollectVerbList(subjectInfoFallback.type);
  });
}

function saveCollectStatus() {
  isSaving.value = true;
  window.pywebview.api.saveCollectStatus(collection.value.subject.id, collect_status.value, rank.value, tag.value.split(/,| /), comment.value, isPrivate.value).then((result) => {
    closeModal();
    toast.success('保存成功');
    isSaving.value = false;
  });
}

const isSaving = ref(false);

function addTag(tag_item: string) {
  if (tag.value.trim() === "") {
    tag.value += tag_item
  } else {

    tag.value += `,${tag_item}`;
  }
}

defineExpose({ openModal, closeModal, setSubject });

</script>
<template>
  <dialog ref="modalElem" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">修改收藏</h3>
      <div class="py-4">
        <div v-if="loading === false && isSaving === false">
          <div>
            <label class="label cursor-pointer" style="width: fit-content; display: inline-block;">
              <input type="radio" name="collect_status" class="radio" :value="1" style="margin-right: 4px;"
                @disabled="isSaving" v-model="collect_status" />
              <span class="label-text">{{ verbList[0] }}</span>
            </label>

            <label class="label cursor-pointer" style="width: fit-content; display: inline-block;">
              <input type="radio" name="collect_status" class="radio" style="margin-right: 4px;" :value="2"
                v-model="collect_status" />
              <span class="label-text">{{ verbList[1] }}</span>
            </label>

            <label class="label cursor-pointer" style="width: fit-content; display: inline-block;">
              <input type="radio" name="collect_status" class="radio" style="margin-right: 4px;" :value="3"
                v-model="collect_status" />
              <span class="label-text">{{ verbList[2] }}</span>
            </label>

            <label class="label cursor-pointer" style="width: fit-content; display: inline-block;">
              <input type="radio" name="collect_status" class="radio" style="margin-right: 4px;" :value="4"
                v-model="collect_status" />
              <span class="label-text">{{ verbList[3] }}</span>
            </label>

            <label class="label cursor-pointer" style="width: fit-content; display: inline-block;">
              <input type="radio" name="collect_status" class="radio" style="margin-right: 4px;" :value="5"
                v-model="collect_status" />
              <span class="label-text">{{ verbList[4] }}</span>
            </label>
          </div>
          <br />
          <p>评分</p><br />
          <select class="select select-secondary w-full max-w-xs" v-model="rank">
            <option :value="0" selected>不评分</option>
            <option :value="1">1</option>
            <option :value="2">2</option>
            <option :value="3">3</option>
            <option :value="4">4</option>
            <option :value="5">5</option>
            <option :value="6">6</option>
            <option :value="7">7</option>
            <option :value="8">8</option>
            <option :value="9">9</option>
            <option :value="10">10</option>
          </select>
          <br /><br />
          <p>标签（使用半角逗号或空格隔开，最多十个）</p>
          <br />
          <input type="text" placeholder="标签" class="input input-bordered w-full" v-model="tag" />
          <br /><br />
          <p>常用标签：<span v-for="(tag, index) of collection.subject.tags" :key="index" @click="addTag(tag.name)"><span
                v-if="index < 10"><button class="btn btn-primary btn-outline btn-sm">{{ tag.name
                  }}</button></span>&nbsp;</span></p>
          <br /><br />
          <p>吐槽</p>
          <br />
          <textarea class="textarea textarea-bordered w-full" placeholder="吐槽" rows="6" v-model="comment"></textarea>
          <br /><br />
          <label class="cursor-pointer">
            <input type="checkbox" class="checkbox" v-model="isPrivate" />
            <span class="label-text">私密</span>
          </label>

          <div class="modal-action">
            <button class="btn" @click="saveCollectStatus">保存</button>
            <button class="btn" @click="closeModal">不保存</button>
          </div>
        </div>
        <div v-if="loading">
          <span class="loading loading-spinner loading-md"></span>正在获取收藏状态数据
        </div>
        <div v-if="isSaving">
          <span class="loading loading-spinner loading-md"></span>正在保存收藏状态
        </div>
      </div>
    </div>
  </dialog>
</template>
