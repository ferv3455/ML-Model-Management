<template>
  <div id="taskIDPageDivBox">
    <h1>
      任务详情页面
      <div class="modelNow">当前服务：{{ serviceName }}</div>
      <div class="modelNowInService">当前模型：{{ modelName }}</div>
    </h1>
    <div id="taskIDPageInfoBox" class="divUse">
      <div class="taskIDPageInfoSmallBox">
        <p class="taskIDPageInfoBoxTitle">当前任务：</p>
        <p>{{ taskID }}</p>
      </div>
      <div class="taskIDPageInfoSmallBox">
        <p class="taskIDPageInfoBoxTitle" id="taskIDPageInfoStatus">任务状态： </p>
        <p>{{ status }}</p>
      </div>
      <div v-if="status === 'finished'">
        <p class="taskIDPageInfoBoxTitle">任务结果：</p>
        <textarea v-model="result" id="testIDPageResult" readonly>
        </textarea>
      </div>
    </div>
    <button @click="goToBatchPage" id="goToBatchPageButton" class="roundButton returnButton">
      <img class="returnIcon themeImage" name="returnIcon.png" alt="return">
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import changeAllImgUrl from '@/getThemeImg';
import getBackUrl from '../getIP';

function changeTaskIDPageDivBoxSize() {
  const cont = document.getElementById('taskIDPageDivBox');
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
      modelName: this.$route.params.modelName,
      taskID: this.$route.params.taskID,
      serviceID: this.$route.params.serviceID,
      serviceName: this.$route.params.serviceName,
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
          modelName: this.modelName,
          serviceID: this.serviceID,
          serviceName: this.serviceName,
        },
      });
    },
  },
  mounted() {
    changeTaskIDPageDivBoxSize();
    window.onresize = changeTaskIDPageDivBoxSize;
    changeAllImgUrl();
    // getTaskInfo
    const path = `/model/${this.modelID}/service/${this.serviceID}/task/${this.taskID}`;
    axios.get(getBackUrl(path), {
      params: {},
    })
      .then((res) => {
        this.status = res.data.status;
        if (this.status === 'finished') {
          this.result = res.data.result;
        }
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
};
</script>

<style>
#taskIDPageDivBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: auto;
  margin-right: auto;
}

#taskIDPageInfoBox {
  flex-grow: 1;
  width: 100%;
  margin: 10px;
  padding: 20px;
}

#taskIDPageInfoBox p {
  margin: 0;
  margin-bottom: 20px;
}

.taskIDPageInfoBoxTitle {
  font-weight: bolder;
  margin-right: 10px;
}

.taskIDPageInfoSmallBox {
  display: flex;
  margin: 0;
}

#testIDPageResult {
  margin-top: -10px;
  width: 100%;
  height: 200px;
}
</style>
