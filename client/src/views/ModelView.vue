<template>
  <div class="alignCenter">
    <h1 id="mainPageTitle">
      主页:模型列表页面
    </h1>
    <table id="mainPageUploadTable">
      <tr>
        <th>模型ID</th>
        <th>描述</th>
        <th>类型</th>
        <th>算法</th>
        <th>上传时间</th>
        <th>服务状态</th>
      </tr>
      <tr v-for="model in models" :key="model" onmouseover="this.style.backgroundColor='var(--buttonTransColor)';"
        onmouseout="this.style.backgroundColor='transparent'">
        <td>
          <router-link :to="{ name: 'modelID', params: { modelID: model.id } }">
            {{ model.id }}
          </router-link>
        </td>
        <td>{{ model.des }}</td>
        <td>{{ model.type }}</td>
        <td>{{ model.algo }}</td>
        <td>{{ formatDate(model.time) }}</td>
        <td>{{ model.status }}</td>
      </tr>

    </table>
    <button @click="changePageToUpload" id="mainPageUploadButton">
      <img id="mainPageUploadIcon" src="../assets/uploadIcon.png" alt="Icon">
      上传模型
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import getBackUrl from '../getIP';

export default {
  data() {
    return {
      models: [],
    };
  },
  methods: {
    changePageToUpload(event) {
      this.$router.push({
        name: 'upload',
      });
    },
    formatDate(value) {
      const date = new Date(value * 1000);
      return date.toLocaleString();
    },
  },
  mounted() {
    axios.get(getBackUrl('/model'), {
      params: {},
    }).then((res) => {
      this.models = res.data.models;
    }).catch((error) => {
      console.log(error);
    });
  },
};

</script>

<style>
#mainPageUploadTable {
  min-width: 80%;
  text-align: center;
  border-style: solid;
  border-color: var(--textColor);
  border-radius: 10px;
  border-width: 3px;
}

#mainPageUploadTable th {
  border-bottom-style: solid;
  border-color: var(--textColor);
  border-collapse: collapse;
  border-width: 2px;
  padding: 7px;
}

#mainPageUploadTable td {
  padding: 7px;
}

#mainPageUploadButton {
  margin-top: 25px;
  display: flex;
  align-items: center;
}

#mainPageUploadIcon {
  width: 30px;
  margin-left: 15px;
  margin-right: 5px;
}
</style>
