<template>
  <div>
    <h1 id="modelIDPageTitle">
      模型详细信息页面
    </h1>
    <div id="modelIDPageModelDetail">
      <p class="modelIDPageModelInfo">模型ID</p>
      <p class="modelIDPageGetModelInfo">{{ modelID }}</p>
      <p class="modelIDPageModelInfo">模型描述</p>
      <p class="modelIDPageGetModelInfo">{{ modelDes }}</p>
      <p class="modelIDPageModelInfo">模型类型</p>
      <p class="modelIDPageGetModelInfo">{{ modelType }}</p>
      <p class="modelIDPageModelInfo">算法</p>
      <p class="modelIDPageGetModelInfo">{{ modelAlgo }}</p>
      <p class="modelIDPageModelInfo">上传时间</p>
      <p class="modelIDPageGetModelInfo">{{ modelTime }}</p>
      <p class="modelIDPageModelInfo">输入变量列表</p>
      <table id="modelIDPageInputTable">
        <tr>
          <th>字段</th>
          <th>类型</th>
          <th>测量</th>
          <th>取值</th>
        </tr>
        <tr v-for="input in modelInputs" :key="input">
          <td>{{ input.name }}</td>
          <td>{{ input.type }}</td>
          <td>{{ input.measure }}</td>
          <td>{{ input.value }}</td>
        </tr>
      </table>
      <p class="modelIDPageModelInfo">目标变量列表</p>
      <table id="modelIDPageOutputTable">
        <tr>
          <th>字段</th>
          <th>类型</th>
          <th>测量</th>
          <th>取值</th>
        </tr>
        <tr v-for="output in modelOutputs" :key="output">
          <td>{{ output.name }}</td>
          <td>{{ output.type }}</td>
          <td>{{ output.measure }}</td>
          <td>{{ output.value }}</td>
        </tr>
      </table>
      <p class="modelIDPageModelInfo">当前服务状态</p>
      <p class="modelIDPageGetModelInfo">{{ modelStatus }}</p>
      <p class="modelIDPageModelInfo">执行次数</p>
      <p class="modelIDPageGetModelInfo">{{ modelCount }}</p>
      <p class="modelIDPageModelInfo">平均响应时间</p>
      <p class="modelIDPageGetModelInfo">{{ modelAverResTime }}ms</p>
      <p class="modelIDPageModelInfo">最大响应时间</p>
      <p class="modelIDPageGetModelInfo">{{ modelMaxResTime }}ms</p>
      <p class="modelIDPageModelInfo">最小响应时间</p>
      <p class="modelIDPageGetModelInfo">{{ modelMinResTime }}ms</p>
    </div>
    <button @click="changeModelStatus" id="modelIDPageChangeModelStatus">切换模型服务状态</button>
    <button @click="backToModelPage" id="modelIDPageBackToModelPage">返回模型列表</button>
    <button @click="goToTestPage" id="modelIDPageGoToTestPage">进入模型测试</button>
    <button @click="goToPredictPage" id="modelIDPageGoToPredictPage">进入部署接口页面</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // 从表单获得的信息（此处不包含模型文件信息）
      modelID: this.$route.params.modelID,
      modelDes: 'xxxxxxxx',
      modelType: 'pmml',
      modelAlgo: 'xxxxxx',
      modelTime: '13:20',
      modelStatus: 'stop',
      modelInputs: [
        {
          name: 'input1',
          type: 'double',
          measure: 'continuous',
          value: '',
        },
        {
          name: 'input2',
          type: 'double',
          measure: 'continuous',
          value: 1080,
        },
      ],
      modelOutputs: [
        {
          name: 'output1',
          type: 'double',
          measure: 'continuous',
          value: '',
        },
        {
          name: 'output2',
          type: 'double',
          measure: 'continuous',
          value: 123,
        },
      ],
      modelCount: 17,
      modelAverResTime: 231,
      modelMaxResTime: 7912,
      modelMinResTime: 120,
    };
  },
  methods: {
    changeModelStatus(event) {
      if (this.modelStatus === 'run') {
        // 此处需要使用axios向后端发出切换模型状态的请求，成功后才可执行以下操作
        this.modelStatus = 'stop';
      } else {
        // 同上
        this.modelStatus = 'run';
      }
    },
    backToModelPage(event) {
      this.$router.push({
        name: 'model',
      });
    },
    goToTestPage(event) {
      this.$router.push({
        name: 'test',
        params: {
          modelID: this.modelID,
          modelInputs: JSON.stringify(this.modelInputs),
        },
      });
    },
    goToPredictPage(event) {
      this.$router.push({
        name: 'predict',
        params: {
          modelID: this.modelID,
        },
      });
    },
  },
};
</script>

<style>
</style>
