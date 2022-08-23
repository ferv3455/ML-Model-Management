<template>
  <div id="servicePageDivBox">
    <h1>
      服务列表页面
      <div class="modelNow">当前模型：{{ modelName }}</div>
    </h1>
    <table id="servicePageServiceTable">
      <tr>
        <th>服务名称</th>
        <th>创建时间</th>
        <th>服务状态</th>
        <th>服务次数</th>
        <th>平均响应时长</th>
        <th>最大响应时长</th>
        <th>最小响应时长</th>
        <th>删除服务</th>
      </tr>
      <tr v-for="service in services" :key="service" onmouseover="this.style.backgroundColor='var(--buttonTransColor)';"
        onmouseout="this.style.backgroundColor='var(--backgroundColor)'">
        <td @mouseover="dialogClickToPredictPage">
          <router-link :to="{ name: 'predict', params: { modelID: modelID, serviceID: service.id } }">
            {{ service.name }}
          </router-link>
        </td>
        <td>{{ formatDate(service.time) }}</td>
        <td>
          <div class="servicePageStatusBox">
            <p>{{ service.status }}</p>
            <div @click="changeStatus(service.id)" @mouseover="dialogClickToChangeStatus" class="changeStatusButton">
              <img class="changeStatusIcon" src="../assets/changeStatusIcon.png" title="切换服务状态" alt="changeIcon">
            </div>
          </div>
        </td>
        <td>{{ service.count }}</td>
        <td>{{ service.averResTime }}ms</td>
        <td>{{ service.maxResTime }}ms</td>
        <td>{{ service.minResTime }}ms</td>
        <td>
          <div @dblclick="clear(service.id)" @mouseover="dialogClickToDeleteService" class="servicePageClearButton">
            <img src="../assets/deleteIcon.png" title="双击删除" alt="binIcon" class="binIcon">
          </div>
        </td>
      </tr>
      <tr>
        <td colspan="8">
          <div id="addServiceAreaDivBox">
            <p>新服务名 </p>
            <input id="servicePageEnterServiceName" v-model="newServiceName">
            <button @click="upload" @mouseover="dialogClickToAddNewService" id="servicePageUploadButton">
              <img src="../assets/addIcon.png" title="点击添加新服务" alt="addIcon" class="addIcon">
            </button>
          </div>

        </td>
      </tr>
    </table>

    <button @click="goToModelIDPage" @mouseover="dialogClickToGoToModelIDPage" id="servicePageGoToModelIDPage"
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

function changeServicePageDivBoxSize() {
  const cont = document.getElementById('servicePageDivBox');
  if (window.innerWidth <= 1024) {
    cont.style.width = `${window.innerWidth * 0.95}px`;
  } else {
    cont.style.width = `${window.innerWidth * 0.80}px`;
  }
}

export default {
  data() {
    return {
      modelID: parseInt(this.$route.params.modelID, 10),
      modelName: '',
      services: [],
      newServiceName: '',
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
              if (this.services[i].status === 'running') {
                this.services[i].status = 'stopped';
              } else {
                this.services[i].status = 'running';
              }
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
          break;
        }
      }
    },
    clear(serviceID) {
      for (let i = 0; i < this.services.length; i += 1) {
        if (this.services[i].id === serviceID) {
          const path = `/model/${this.modelID}/service/${serviceID}`;
          axios.delete(getBackUrl(path))
            .then((res) => {
              for (let j = i; j < this.services.length - 1; j += 1) {
                this.services[j] = this.services[j + 1];
              }
              this.services.pop();
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
          break;
        }
      }
    },
    upload(event) {
      // upload new service
      if (this.newServiceName === '') {
        alert('服务名为空！');
        return;
      }
      const path = `/model/${this.modelID}/service`;
      axios.post(getBackUrl(path), {
        name: this.newServiceName,
      })
        .then((res) => {
          this.$router.go(0);
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
    dialogClickToGoToModelIDPage(event) {
      setDialog('੭˙ᗜ˙)੭ ♡点击返回上一页，那里可以查看模型详情', 1500);
    },
    dialogClickToPredictPage(event) {
      setDialog('想要部署服务接口,请点击这里!_(:3 ⌒ﾞ)_', 1500);
    },
    dialogClickToChangeStatus(event) {
      setDialog('点击转换服务状态(•ㅅ•)♡', 1500);
    },
    dialogClickToDeleteService(event) {
      setDialog('点击后就找不回了இдஇ！千万不要点错哟！！', 1500);
    },
    dialogClickToAddNewService(event) {
      setDialog('⁽⁽٩(๑˃̶͈̀ ᗨ ˂̶͈́)۶⁾⁾可以添加新的服务哟！', 1500);
    },
    getModelName() {
      const path = `/model/${this.modelID}`;
      axios.get(getBackUrl(path))
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
    },
    formatDate(value) {
      const date = new Date(value * 1000);
      return date.toLocaleString();
    },
  },
  mounted() {
    // Get Service List
    const path = `/model/${this.modelID}/service`;
    axios.get(getBackUrl(path))
      .then((res) => {
        this.services = res.data.services;
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
    this.getModelName();
    changeServicePageDivBoxSize();
    window.onresize = changeServicePageDivBoxSize;
    setTimeout(() => { changeAllImgUrl(); }, 100);
    setTimeout(() => { setDialog('', 0); }, 100);
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

#addServiceAreaDivBox {
  display: flex;
  margin-top: 0px;
  margin-bottom: 0px;
  margin-left: auto;
  margin-right: auto;
  flex-direction: row;
  align-items: center;
  width: 500px;
}

#addServiceAreaDivBox p {
  margin-top: 0px;
  margin-bottom: 5px;
  font-weight: bolder;
  text-align: left;
  width: 110px;
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
  margin-left: auto;
  margin-right: auto;
  padding: 0;
}

.servicePageClearButton {
  width: 25px;
  margin-left: auto;
  margin-right: auto;
  height: 25px;
  background-color: transparent;
  color: transparent;
  box-shadow: none;
  padding: 0;
}

#servicePageUploadButton {
  width: 30px;
  margin-left: 15px;
  margin-right: auto;
  height: 25px;
  background-color: transparent;
  color: transparent;
  box-shadow: none;
  padding: 0;
}
</style>
