<template>
  <div>
    <h1>
      任务详情页面
    </h1>
    <p>当前模型：{{ modelID }}</p>
    <p>当前任务：{{ taskID }}</p>
    <p>任务状态：{{ status }} </p>
    <div v-if="status === 'finished'">
      <p>任务结果：</p>
      <textarea v-model="result" id="testIDPageresult" readonly>
      </textarea>
    </div>
    <button @click="goToBatchPage" id="goToBatchPageButton">返回任务列表</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      modelID: this.$route.params.modelID,
      taskID: this.$route.params.taskID,
      status: 'finished', // 从后端获取
      result: 'this is a result!', // 从后端获取
    };
  },
  methods: {
    goToBatchPage(event) {
      this.$router.push({
        name: 'batch',
        params: {
          modelID: this.modelID,
        },
      });
    },
  },
  mounted() {
    // TODO
    // 从后端获取数据
  },
};
</script>

<style>
</style>
