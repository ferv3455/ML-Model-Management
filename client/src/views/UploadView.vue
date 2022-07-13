<template>
  <div>
    <h1 id="uploadPageTitle">
      模型导入页面
    </h1>
    <div id="uploadPageImportModel">
      <p class="uploadPageImportModelDetail">模型ID</p>
      <input v-model="modelID" id="uploadPageEnterModelID">
      <p class="uploadPageImportModelDetail">模型描述</p>
      <input v-model="modelDescription" id="uploadPageEnterModelDescription">
      <p class="uploadPageImportModelDetail">模型类型</p>
      <select v-model="modelType" id="uploadPageEnterModelType" value="pmml">
        <option value="pmml">PMML</option>
        <option value="onnx">ONNX</option>
      </select>
      <p class="uploadPageImportModelDetail">模型文件</p>
      <input id="uploadPageEnterModelFile" type="file" accept=".pmml,.onnx">
    </div>
    <button @click="uploadNewModel" id="uploadPageUploadButton">上传</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // 从表单获得的信息（此处不包含模型文件信息）
      modelID: '',
      modelDescription: '',
      modelType: '',
    };
  },
  methods: {
    // 将上传信息提交给后端，后端回应后执行相应操作
    uploadModel(event) {
    },
  },
};

</script>

<style>
</style>
