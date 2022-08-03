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
    <div id="servicePageAddServiceArea" class="divUse">
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
import getBackUrl from '../getIP';

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
          let option = '';
          if (this.services[i].status === 'running') {
            option = 'pause';
          } else {
            option = 'start';
          }
          // service change request
          const path = `/model/${this.modelID}/service/${serviceID}`;
          axios.post(getBackUrl(path), {
            opr: option,
          })
            .then((res) => {
              if (res.data.status === 'success') {
                if (this.services[i].status === 'running') {
                  this.services[i].status = 'stopped';
                } else {
                  this.services[i].status = 'running';
                }
              } else {
                const mes = '更改服务状态失败';
                alert(mes);
              }
            })
            .catch((error) => {
              console.log(error);
            });
          break;
        }
      }
    },
    clear(serviceID) {
      for (let i = 0; i < this.services.length; i += 1) {
        if (this.services[i].id === serviceID) {
          const option = 'delete';
          // delete service request
          const path = `/model/${this.modelID}/service/${serviceID}`;
          axios.post(getBackUrl(path), {
            opr: option,
          })
            .then((res) => {
              if (res.data.status === 'success') {
                for (let j = i; j < this.services.length - 1; j += 1) {
                  this.services[j] = this.services[j + 1];
                }
                this.services.pop();
              } else {
                const mes = '删除服务失败';
                alert(mes);
              }
            })
            .catch((error) => {
              console.log(error);
            });
          break;
        }
      }
    },
    upload(event) {
      // upload new service
      const path = `/model/${this.modelID}/service`;
      axios.post(getBackUrl(path), {
        id: this.newServiceID,
      })
        .then((res) => {
          if (res.data.status === 'success') {
            // Get Service List
            const path2 = `/model/${this.modelID}/service`;
            axios.get(getBackUrl(path2), {
              params: {},
            })
              .then((res2) => {
                this.services = res2.data.services;
              })
              .catch((error) => {
                console.log(error);
              });
            changeServicePageDivBoxSize();
            window.onresize = changeServicePageDivBoxSize;
          } else {
            const mes = '新建服务失败';
            alert(mes);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    // Get Service List
    const path = `/model/${this.modelID}/service`;
    axios.get(getBackUrl(path), {
      params: {},
    })
      .then((res) => {
        this.services = res.data.services;
      })
      .catch((error) => {
        console.log(error);
      });
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
  padding: 0;
}

.servicePageClearButton {
  width: 30px;
  margin-right: 10px;
  height: auto;
  background-color: transparent;
  box-shadow: none;
  padding: 0;
}
</style>
