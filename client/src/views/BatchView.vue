<template>
  <div id="batchPageDivBox">
    <h1>
      批量任务列表页面
      <div class="modelNow">当前服务：{{ serviceName }}</div>
      <div class="modelNowInService">当前模型：{{ modelName }}</div>
    </h1>
    <table id="batchPageTaskTable">
      <tr>
        <th>任务ID</th>
        <th>任务状态</th>
      </tr>
      <tr v-for="task in tasks" :key="task" onmouseover="this.style.backgroundColor='var(--buttonTransColor)';"
        onmouseout="this.style.backgroundColor='var(--backgroundColor)'">
        <td>
          <router-link @mouseover="dialogClickToTaskPage"
            :to="{ name: 'task', params: { modelID: modelID, serviceID: serviceID, taskID: task.id } }">
            {{ task.id }}
          </router-link>
        </td>
        <td>{{ task.status }}</td>
      </tr>
    </table>
    <div id="batchPageAddTaskArea" class="divUse">
      <h2>创建新任务</h2>
      <input id="batchPageEnterModelFile" type="file" accept=".csv,.zip">
      <button @click="upload" @mouseover="dialogClickToUpload" id="batchPageUploadButton">添加</button>
    </div>
    <button @click="goToPredictPage" @mouseover="dialogClickToPredictPage" id="BatchPageGoTopredictPage"
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
      modelID: parseInt(this.$route.params.modelID, 10),
      modelName: '',
      serviceID: parseInt(this.$route.params.serviceID, 10),
      serviceName: '',
      // 需从后端请求当前存在的tasks
      tasks: [{
        id: 1,
        status: 'waiting',
      }, {
        id: 2,
        status: 'running',
      }, {
        id: 3,
        status: 'finished',
      },
      ],
    };
  },
  methods: {
    upload(event) {
      // FileUpload
      // 将上传文件提交给后端
      const path = `/model/${this.modelID}/service/${this.serviceID}/task`;
      const f = document.getElementById('batchPageEnterModelFile').files[0];
      const postRequest = new FormData();

      if (document.getElementById('batchPageEnterModelFile').value === '') {
        alert('任务文件为空！');
        return;
      }

      postRequest.append('file', f);
      axios.post(getBackUrl(path), postRequest, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
        .then((res) => {
          // 将后端返回的任务ID提示给用户
          const idMes = `任务ID：${res.data.id}`;
          alert(idMes);
          this.$router.go(0);
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
          serviceID: this.serviceID,
        },
      });
    },
    dialogClickToTaskPage(event) {
      setDialog('点击前往任务详情页面♡◝(\'ω\'◝)', 1500);
    },
    dialogClickToUpload(event) {
      setDialog('添加新任务了~(｡・ω・｡)', 1500);
    },
    dialogClickToPredictPage(event) {
      setDialog('点击返回部署接口页面٩(๑❛ᴗ❛๑)۶', 1500);
    },
    getModelAndServiceName() {
      axios.get(getBackUrl(`/model/${this.modelID}`))
        .then((res) => {
          if (res.data.exist === true) {
            this.modelName = res.data.name;
          } else {
            alert('模型不存在');
          }
        })
        .catch((error) => {
          console.log(error);
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
          alert('服务不存在');
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    changeBatchPageDivBoxSize();
    window.onresize = changeBatchPageDivBoxSize;
    changeAllImgUrl();
    this.getModelAndServiceName();
    setTimeout(() => { setDialog('', 0); }, 100);
    // getBatchInfo
    const path = `/model/${this.modelID}/service/${this.serviceID}/task`;
    axios.get(getBackUrl(path), {
      params: {},
    })
      .then((res) => {
        if (res.data.status === 'fail') {
          alert('获取任务列表失败');
          return;
        }
        this.tasks = res.data.tasks;
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        alert('服务器错误');
      });
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
