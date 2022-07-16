<template>
  <div>
    <h1>
      模型测试页面
    </h1>
    <p>当前模型：{{ modelID }}</p>
    <div id="testPageLeftRight">
      <div class="testPageSmallBox">
        <h2 class="testPageSmallBoxTitle"> 输入</h2>
        <button @click="changeMode" id="testPageChangeMode">{{ mode }}</button>
        <div v-if="mode === 'json'">
          <textarea v-model="jsonInput" id="testPageJsonInput"></textarea>
        </div>
        <div v-if="mode === 'form'">
          <div v-for="variance in variances" :key="variance">
            <p>{{ variance.name }}</p>
            <input :id="'var_' + variance.name">
          </div>
        </div>
        <button @dblclick="clear" id="testPageClearButton">双击清除</button>
        <button @click="submit" id="testPageSubmitButton">提交</button>
      </div>
      <div class="testPageSmallBox">
        <h2 class="testPageSmallBoxTitle"> 输出</h2>
        <textarea v-model="output" readonly id="testPageOutput"></textarea>
      </div>
    </div>
  </div>
  <button @click="backToModelIDPage">返回模型详细信息页面</button>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      modelID: this.$route.params.modelID,
      mode: 'json',
      output: 'this is output!',
      jsonInput: '',
      variances: JSON.parse(this.$route.params.modelInputs),
    };
  },
  methods: {
    changeMode(event) {
      this.clear(event);
      if (this.mode === 'json') {
        this.mode = 'form';
      } else {
        this.mode = 'json';
      }
      // console.log(this.variances[0].name);
    },
    clear(event) {
      if (this.mode === 'json') {
        this.jsonInput = '';
      } else {
        for (let i = 0; i < this.variances.length; i += 1) {
          const inputBox = document.getElementById(`var_${this.variances[i].name}`);
          inputBox.value = '';
        }
      }
    },
    submit(event) {
      let submitObject = {};
      if (this.mode === 'json') {
        submitObject = JSON.parse(this.jsonInput);
      } else {
        for (let i = 0; i < this.variances.length; i += 1) {
          const inputBox = document.getElementById(`var_${this.variances[i].name}`);
          submitObject[this.variances[i].name] = inputBox.value;
        }
      }
      console.log(submitObject);
      // 将submitObject（格式：JS对象——已经处理好了）作为输入参数提交给后端
    },
    backToModelIDPage(event) {
      this.$router.push({
        name: 'modelID',
        params: {
          modelID: this.modelID,
        },
      });
    },
  },
};

</script>

<style>
#testPageLeftRight {
  display: flex;
  width: 100%;
}

.testPageSmallBox {
  flex-grow: 1;
  margin: 10px;
  background-color: lightgray;
}
</style>
