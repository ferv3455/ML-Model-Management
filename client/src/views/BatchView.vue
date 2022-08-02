<template>
  <div id="batchPageDivBox">
    <h1>
      批量任务列表页面
      <div class="modelNow">当前服务：{{ serviceID }}</div>
      <div class="modelNowInService">当前模型：{{ modelID }}</div>
    </h1>
    <table id="batchPageTaskTable">
      <tr>
        <th>任务ID</th>
        <th>任务状态</th>
      </tr>
      <tr v-for="task in tasks" :key="task" onmouseover="this.style.backgroundColor='var(--buttonTransColor)';"
        onmouseout="this.style.backgroundColor='transparent'">
        <td>
          <router-link :to="{ name: 'task', params: { modelID: modelID, serviceID: serviceID, taskID: task.id } }">
            {{ task.id }}
          </router-link>
        </td>
        <td>{{ task.status }}</td>
      </tr>
    </table>
    <div id="batchPageAddTaskArea" class="divUse">
      <h2>创建新任务</h2>
      <!--TODO 还未确定可输入文件的类型！（跟后端沟通后再加上）-->
      <input id="batchPageEnterModelFile" type="file">
      <button @click="upload" id="batchPageUploadButton">添加</button>
    </div>
    <button @click="goToPredictPage" id="BatchPageGoTopredictPage" class="roundButton returnButton">
      <img class="returnIcon" src="../assets/returnIcon.png" alt="return">
    </button>
  </div>
</template>

<script>
import axios from 'axios';

function changeBatchPageDivBoxSize() {
  const cont = document.getElementById('batchPageDivBox');
  if (window.innerWidth <= 800) {
    cont.style.width = `${window.innerWidth * 0.90}px`;
  } else {
    cont.style.width = '720px';
  }
}

export default {
  data() {
    return {
      modelID: this.$route.params.modelID,
      serviceID: this.$route.params.serviceID,
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
      // TODO
      // 将上传文件提交给后端
      // 将后端返回的任务ID提示给用户（通过alert方法）
    },
    goToPredictPage(event) {
      this.$router.push({
        name: 'predict',
        params: {
          modelID: this.modelID,
          serviceID: this.serviceID,
        },
      });
    },
  },
  mounted() {
    // TODO
    // 从后端获取数据
    changeBatchPageDivBoxSize();
    window.onresize = changeBatchPageDivBoxSize;
  },
};

</script>

<style>
#batchPageDivBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: auto;
  margin-right: auto;
}

#batchPageTaskTable {
  min-width: 100%;
  text-align: center;
  border-style: solid;
  border-color: var(--textColor);
  border-radius: 10px;
  border-width: 3px;
  margin-bottom: 15px;
}

#batchPageTaskTable th {
  border-bottom-style: solid;
  border-color: var(--textColor);
  border-collapse: collapse;
  border-width: 2px;
  padding: 7px;
}

#batchPageTaskTable td {
  padding: 7px;
}

#batchPageAddTaskArea {
  width: 100%;
  flex-grow: 1;
  margin: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#batchPageAddTaskArea h2 {
  margin: 0;
  font-size: 25px;
  margin-bottom: 15px;
}

#batchPageEnterModelFile {
  width: 100%;
  margin-bottom: 20px;
}
</style>
