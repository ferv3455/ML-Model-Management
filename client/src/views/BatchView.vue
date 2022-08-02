<template>
  <div>
    <h1>
      批量任务列表页面
    </h1>
    <p>当前模型{{ modelID }}</p>
    <table id="batchPageTaskTable">
      <tr>
        <th>任务ID</th>
        <th>任务状态</th>
      </tr>
      <tr v-for="task in tasks" :key="task">
        <td>
          <router-link :to="{ name: 'task', params: { modelID: modelID, taskID: task.id } }">
            {{ task.id }}
          </router-link>
        </td>
        <td>{{ task.status }}</td>
      </tr>
    </table>
    <div id="batchPageAddTaskArea">
      <p>创建新任务</p>
      <!--TODO 还未确定可输入文件的类型！（跟后端沟通后再加上）-->
      <input id="uploadPageEnterModelFile" type="file">
      <button @click="upload" id="batchPageUploadButton">添加</button>
    </div>
    <button @click="goToPredictPage" id="BatchPageGoTopredictPage">返回部署接口页面</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      modelID: this.$route.params.modelID,
      // 需从后端请求当前存在的tasks
      tasks: [{
        id: 'task1',
        status: 'waiting',
      }, {
        id: 'task2',
        status: 'running',
      }, {
        id: 'task3',
        status: 'finished',
      },
      ],
    };
  },
  methods: {
    upload(event) {
      // FileUpload
      // 将上传文件提交给后端
      path = '/model/' + this.modelID.toString() + '/predict/batch/';
      axios.post(getBackUrl(path), {

      })
        .then((res) => {
          // 将后端返回的任务ID提示给用户（通过alert方法）
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    goToPredictPage(event) {
      this.$router.push({
        name: 'predict',
        params: {
          modelID: this.modelID,
        },
      });
    },
  },
  mounted() {
    // getBatchInfo
    path = '/model/' + this.modelID.toString() + '/predict/batch/';
    axios.get(getBackUrl(path), {
      params: {
        modelID: this.modelID,
      }
    })
      .then((res) => {
        this.tasks = res.data.tasks;
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
};

</script>

<style>
</style>
