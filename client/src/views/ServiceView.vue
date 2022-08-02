<template>
  <div id="servicePageDivBox">
    <h1>
      服务列表页面
      <div class="modelNow">当前模型：{{ modelID }}</div>
    </h1>
    <table id="servicePageServiceTable">
      <tr>
        <th>服务ID</th>
        <th>创建时间</th>
        <th>服务状态</th>
        <th>服务次数</th>
        <th>平均响应时长</th>
        <th>最大响应时长</th>
        <th>最小响应时长</th>
        <th>删除服务</th>
      </tr>
      <tr v-for="service in services" :key="service" onmouseover="this.style.backgroundColor='var(--buttonTransColor)';"
        onmouseout="this.style.backgroundColor='transparent'">
        <td>
          <router-link :to="{ name: 'predict', params: { modelID: modelID, serviceID: service.id } }">
            {{ service.id }}
          </router-link>
        </td>
        <td>{{ service.time }}</td>
        <td>
          <div class="servicePageStatusBox">
            <p>{{ service.status }}</p>
            <button @click="changeStatus(service.id)" class="changeStatusButton">
              <img class="changeStatusIcon" src="../assets/changeStatusIcon.png" title="切换模型状态" alt="changeIcon">
            </button>
          </div>
        </td>
        <td>{{ service.count }}</td>
        <td>{{ service.averResTime }}</td>
        <td>{{ service.maxResTime }}</td>
        <td>{{ service.minResTime }}</td>
        <td>
          <button @dblclick="clear(service.id)" class="servicePageClearButton">
            <img src="../assets/deleteIcon.png" title="双击删除" alt="binIcon" class="binIcon">
          </button>
        </td>
      </tr>
    </table>
    <div id="servicePageAddServiceArea">
      <h2>添加新服务</h2>
      <div id="addServiceAreaDivBox">
        <p>新服务ID :</p>
        <input id="servicePageEnterServiceID" v-model="newServiceID">
      </div>
      <button @click="upload" id="servicePageUploadButton">添加</button>
    </div>
    <button @click="goToModelIDPage" id="servicePageGoToModelIDPage" class="roundButton returnButton">
      <img class="returnIcon" src="../assets/returnIcon.png" alt="return">
    </button>
  </div>
</template>

<script>
import axios from 'axios';

function changeServicePageDivBoxSize() {
  const cont = document.getElementById('servicePageDivBox');
  if (window.innerWidth <= 1000) {
    cont.style.width = `${window.innerWidth * 0.90}px`;
  } else {
    cont.style.width = `${window.innerWidth * 0.80}px`;
  }
}

export default {
  data() {
    return {
      modelID: this.$route.params.modelID,
      services: [
        {
          id: 'service1',
          time: 'xxx',
          status: 'running',
          count: 'xxx',
          averResTime: 'xxx',
          maxResTime: 'xxx',
          minResTime: 'xxx',
        },
        {
          id: 'service2',
          time: 'xxx',
          status: 'stopped',
          count: 'xxx',
          averResTime: 'xxx',
          maxResTime: 'xxx',
          minResTime: 'xxx',
        },
        {
          id: 'service3',
          time: 'xxx',
          status: 'stopped',
          count: 'xxx',
          averResTime: 'xxx',
          maxResTime: 'xxx',
          minResTime: 'xxx',
        },
      ],
      newServiceID: '',
    };
  },
  methods: {
    goToModelIDPage(event) {
      this.$router.push({
        name: 'modelID',
        params: {
          modelID: this.modelID,
        },
      });
    },
    changeStatus(serviceID) {
      for (let i = 0; i < this.services.length; i += 1) {
        if (this.services[i].id === serviceID) {
          if (this.services[i].status === 'running') {
            // TODO 向后段发送更改服务状态请求，成功后执行下面代码
            this.services[i].status = 'stopped';
          } else {
            // TODO 向后段发送更改服务状态请求，成功后执行下面代码
            this.services[i].status = 'running';
          }
          break;
        }
      }
    },
    clear(serviceID) {
      for (let i = 0; i < this.services.length; i += 1) {
        if (this.services[i].id === serviceID) {
          // TODO 向后段发送删除服务请求，成功后执行下面代码
          for (let j = i; j < this.services.length - 1; j += 1) {
            this.services[j] = this.services[j + 1];
          }
          this.services.pop();
          break;
        }
      }
    },
    upload(event) {
      // TODO 向后端添加一个新服务
    },
  },
  mounted() {
    // TODO
    // 从后端获取数据
    changeServicePageDivBoxSize();
    window.onresize = changeServicePageDivBoxSize;
  },
};
</script>

<style>
#servicePageDivBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: auto;
  margin-right: auto;
}

#servicePageServiceTable {
  min-width: 100%;
  text-align: center;
  border-style: solid;
  border-color: var(--textColor);
  border-radius: 10px;
  border-width: 3px;
  margin-bottom: 15px;
}

#servicePageServiceTable th {
  border-bottom-style: solid;
  border-color: var(--textColor);
  border-collapse: collapse;
  border-width: 2px;
  padding: 7px;
}

#servicePageServiceTable td {
  padding: 7px;
}

#servicePageAddServiceArea {
  width: 100%;
  flex-grow: 1;
  margin: 10px;
  border-style: solid;
  border-color: var(--textColor);
  border-radius: 10px;
  border-width: 3px;
  box-sizing: border-box;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#servicePageAddServiceArea h2 {
  margin: 0;
  font-size: 25px;
  margin-bottom: 5px;
}

#addServiceAreaDivBox {
  display: flex;
  align-items: center;
  width: 100%;
}

#addServiceAreaDivBox p {
  width: 140px;
}

.servicePageStatusBox {
  display: flex;
  align-items: center;
  margin-left: auto;
  margin-right: auto;
}

.servicePageStatusBox p {
  margin: 0;
  min-width: 80px;
  flex-grow: 1;
}

.changeStatusButton {
  background-color: transparent;
  color: transparent;
  box-shadow: none;
  width: 30px;
  height: 30px;
  margin-right: 10px;
}

.servicePageClearButton {
  width: 25px;
  margin-right: 10px;
  height: auto;
  background-color: transparent;
  box-shadow: none;
}
</style>
