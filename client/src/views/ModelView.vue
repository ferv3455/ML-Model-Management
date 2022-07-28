<template>
  <div>
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
      <tr v-for="model in models" :key="model">
        <td>
          <router-link :to="{ name: 'modelID', params: { modelID: model.id } }">
            {{ model.id }}
          </router-link>
        </td>
        <td>{{ model.des }}</td>
        <td>{{ model.type }}</td>
        <td>{{ model.algo }}</td>
        <td>{{ model.time }}</td>
        <td>{{ model.status }}</td>
      </tr>

    </table>
    <button @click="changePageToUpload" id="mainPageUploadButton">上传新模型</button>
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
</style>
