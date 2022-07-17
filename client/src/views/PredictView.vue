<template>
  <div>
    <h1>
      部署接口页面
    </h1>
    <p>当前模型：{{ modelID }}</p>
    <div id="predictPageBox">
      <div class="predictPageSmallBox" id="predictPageInputBox">
        <p class="predictPageSmallBoxTitle">Json输入</p>
        <textarea v-model="jsonInput" id="predictPageJsonInput"></textarea>
        <p class="predictPageSmallBoxTitle">Curl代码</p>
        <textarea v-model="curlInput" id="predictPageCurlInput" readonly></textarea>
        <button @click="submit" id="predictPageSubmitButton">提交</button>
        <button @click="generateCurl" id="predictPageGenerateCurl">生成Curl代码</button>
        <button @click="copyCurl" id="predictPageCopyCurl">复制Curl代码</button>
      </div>
      <div class="predictPageSmallBox" id="predictPageOutputBox">
        <p>输出</p>
        <textarea v-model="output" id="predictPageOutput" readonly></textarea>
      </div>
    </div>
    <button @click="goToBatchPage" id="predictPageGoToBatchPage">前往批量任务列表</button>
    <button @click="goToModelIDPage" id="predictPageGoToModelIDPage">返回模型详细信息页面</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      modelID: this.$route.params.modelID,
      output: 'this is output!', // 测试用，提交后等待后端返回输出
      jsonInput: '',
      curlInput: '',
    };
  },
  methods: {
    submit(event) {
      const submitObject = JSON.parse(this.jsonInput);
      // console.log(submitObject);
      // 将submitObject（格式：JS对象——已经处理好了）作为输入参数提交给后端
    },
    generateCurl(event) {
      this.curlInput = 'Get curl code!!';
      // 需要生成向后端请求的curl代码
    },
    goToBatchPage(event) {
      this.$router.push({
        name: 'batch',
        params: {
          modelID: this.modelID,
        },
      });
    },
    goToModelIDPage(event) {
      this.$router.push({
        name: 'modelID',
        params: {
          modelID: this.modelID,
        },
      });
    },
    copyCurl(event) {
      const copyElement = document.getElementById('predictPageCurlInput');
      copyElement.select();
      document.execCommand('copy');
    },
  },
};
</script>

<style>
#predictPageBox {
  display: flex;
  width: 100%;
}

.predictPageSmallBox {
  flex-grow: 1;
  width: 50%;
  margin: 10px;
  background-color: lightgray;
}

#predictPageInputBox {
  display: flex;
  flex-direction: column;
}
</style>
