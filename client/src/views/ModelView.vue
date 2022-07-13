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
        <td>{{ model.id }}</td>
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

export default {
  data() {
    return {
      // 需从后端请求当前存在的model
      models: [{
        id: 'model1',
        des: 'model 1 is xxxxxx',
        tyle: 'pmml',
        algo: 'suanfa',
        time: '2022/06/19 13:78',
        status: 'stop',
      }, {
        id: 'model2',
        des: 'model 2 is xxxxxx',
        tyle: 'onnx',
        algo: 'suanfa',
        time: '2022/06/19 06:35',
        status: 'run',
      },
      ],
    };
  },
  methods: {
    changePageToUpload(event) {
      this.$router.push({
        name: 'upload',
      });
    },
  },
};

</script>

<style>
</style>
