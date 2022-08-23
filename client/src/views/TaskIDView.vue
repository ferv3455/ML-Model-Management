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
    <button @click="goToBatchPage" @mouseover="dialogClickToBatchPage" id="goToBatchPageButton"
      class="roundButton returnButton">
      <img class="returnIcon" src="../assets/returnIcon.png" alt="return">
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import setDialog from '@/live2dSetDialog';
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
      modelID: parseInt(this.$route.params.modelID, 10),
      modelName: '',
      taskID: parseInt(this.$route.params.taskID, 10),
      serviceID: parseInt(this.$route.params.serviceID, 10),
      serviceName: '',
      status: '', // 从后端获取
      result: '', // 从后端获取
    };
  },
  methods: {
    goToBatchPage(event) {
      this.$router.push({
        name: 'batch',
        params: {
          modelID: this.modelID,
          serviceID: this.serviceID,
        },
      });
    },
    dialogClickToBatchPage(event) {
      setDialog('ヽ(✿ﾟ▽ﾟ)ノ点击返回批量任务列表页面', 1500);
    },
    getModelAndServiceName() {
      axios.get(getBackUrl(`/model/${this.modelID}`))
        .then((res) => {
          this.modelName = res.data.name;
        })
        .catch((error) => {
          console.log(error);
          if (error.response && error.response.status === 404) {
            alert('信息不存在');
          } else if (error.response && error.response.status === 406) {
            alert('系统处理错误');
          } else {
            alert('服务器错误');
          }
        });
      console.log(this.serviceID);
      axios.get(getBackUrl(`/model/${this.modelID}/service`))
        .then((res) => {
          const tmpServices = res.data.services;
          console.log(tmpServices);
          for (let i = 0; i < tmpServices.length; i += 1) {
            if (tmpServices[i].id === this.serviceID) {
              this.serviceName = tmpServices[i].name;
              return;
            }
          }
          alert('信息不存在');
        })
        .catch((error) => {
          console.log(error);
          if (error.response && error.response.status === 404) {
            alert('信息不存在');
          } else if (error.response && error.response.status === 406) {
            alert('系统处理错误');
          } else {
            alert('服务器错误');
          }
        });
    },
  },
  mounted() {
    changeTaskIDPageDivBoxSize();
    window.onresize = changeTaskIDPageDivBoxSize;
    this.getModelAndServiceName();
    changeAllImgUrl();
    setTimeout(() => { setDialog('', 0); }, 100);
    // getTaskInfo
    const path = `/model/${this.modelID}/service/${this.serviceID}/task/${this.taskID}`;
    axios.get(getBackUrl(path))
      .then((res) => {
        this.status = res.data.status;
        this.result = JSON.stringify(res.data.result, null, 2);
      })
      .catch((error) => {
        console.log(error);
        if (error.response && error.response.status === 404) {
          alert('信息不存在');
        } else if (error.response && error.response.status === 406) {
          alert('系统处理错误');
        } else {
          alert('服务器错误');
        }
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
