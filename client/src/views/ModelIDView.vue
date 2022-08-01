<template>
  <div>
    <h1 id="modelIDPageTitle">
      模型详细信息页面
    </h1>
    <div id="modelIDPageModelDetail">
      <div id="modelIDPageModelDetailBasic">
        <p class="modelIDPageModelInfo">ID</p>
        <p class="modelIDPageGetModelInfo">{{ modelID }}</p>
        <p class="modelIDPageModelInfo">描述</p>
        <p class="modelIDPageGetModelInfo">{{ modelDes }}</p>
        <p class="modelIDPageModelInfo">类型</p>
        <p class="modelIDPageGetModelInfo">{{ modelType }}</p>
        <p class="modelIDPageModelInfo">算法</p>
        <p class="modelIDPageGetModelInfo">{{ modelAlgo }}</p>
        <p class="modelIDPageModelInfo">状态</p>
        <div id="modelIDPageStatusBox">
          <p class="modelIDPageGetModelInfo">{{ modelStatus }}</p>
          <button @click="changeModelStatus" id="modelIDPageChangeModelStatus">
            <img class="changeStatusIcon" src="../assets/changeStatusIcon.png" title="切换模型状态" alt="changeIcon">
          </button>
        </div>
        <p class="modelIDPageModelInfo">上传时间</p>
        <p class="modelIDPageGetModelInfo">{{ modelTime }}</p>
      </div>
      <div id="modelIDPageModelVar">
        <div class="modelIDPageModelVarTable">
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
        </div>
        <div class="modelIDPageModelVarTable">
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
        </div>
      </div>
      <div id="modelIDPageModelTimeInfo">
        <p class="modelIDPageModelInfo">执行次数</p>
        <p class="modelIDPageGetModelInfo">{{ modelCount }}</p>
        <p class="modelIDPageModelInfo">平均响应时间</p>
        <p class="modelIDPageGetModelInfo">{{ modelAverResTime }}ms</p>
        <p class="modelIDPageModelInfo">最大响应时间</p>
        <p class="modelIDPageGetModelInfo">{{ modelMaxResTime }}ms</p>
        <p class="modelIDPageModelInfo">最小响应时间</p>
        <p class="modelIDPageGetModelInfo">{{ modelMinResTime }}ms</p>
      </div>
      <div>
        <button @click="goToTestPage" id="modelIDPageGoToTestPage">进入模型测试</button>
        <button @click="goToPredictPage" id="modelIDPageGoToPredictPage">进入部署接口页面</button>
      </div>
    </div>
    <button @click="backToModelPage" id="modelIDPageBackToModelPage" class="roundButton returnButton">
      <img class="returnIcon" src="../assets/returnIcon.png" alt="return">
    </button>
  </div>
</template>

<script>
import axios from 'axios';

function changeModelDetailSize() {
  const cont = document.getElementById('modelIDPageModelDetailBasic');
  const cont2 = document.getElementById('modelIDPageModelVar');
  const cont3 = document.getElementById('modelIDPageModelTimeInfo');
  if (window.innerWidth <= 800) {
    cont.style.width = `${window.innerWidth * 0.95}px`;
    cont2.style.width = `${window.innerWidth * 0.95}px`;
    cont3.style.width = `${window.innerWidth * 0.95}px`;
  } else {
    cont.style.width = '700px';
    cont2.style.width = '700px';
    cont3.style.width = '700px';
  }
}

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
        {
          name: 'input3',
          type: 'double',
          measure: 'continuous',
          value: 1080,
        },
        {
          name: 'input4',
          type: 'double',
          measure: 'continuous',
          value: 1080,
        },
        {
          name: 'input5',
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
        // TODO
        // 此处需要使用axios向后端发出切换模型状态的请求，成功后才可执行以下操作
        this.modelStatus = 'stop';
      } else {
        // TODO
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
  mounted() {
    changeModelDetailSize();
    window.onresize = changeModelDetailSize;

    // TODO
    // 从后端获取数据
  },
};
</script>

<style>
#modelIDPageModelDetail {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#modelIDPageModelDetailBasic {
  border-style: solid;
  border-color: var(--textColor);
  border-radius: 10px;
  border-width: 3px;
  box-sizing: border-box;
  padding: 20px;
  padding-bottom: 25px;
  display: grid;
  grid-template-columns: 20% 20% 25% 35%;
  grid-template-rows: 50px 50px 50px;
}

#modelIDPageModelDetailBasic .modelIDPageModelInfo {
  text-align: right;
  margin-right: 30px;
  font-weight: bolder;
}

#modelIDPageModelVar {
  margin-top: 35px;
  border-style: solid;
  border-color: var(--textColor);
  border-radius: 10px;
  border-width: 3px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  padding: 20px;
  align-items: center;
}

.modelIDPageModelVarTable {
  width: 95%;
  margin: 5px;
  flex-grow: 1;
}

.modelIDPageModelVarTable .modelIDPageModelInfo {
  margin: 10px;
  margin-top: 0px;
  font-weight: bolder;
  text-align: left;
}

.modelIDPageModelVarTable table {
  width: 100%;
  text-align: center;
  border-style: solid;
  border-color: var(--buttonColor);
  border-radius: 5px;
  border-width: 2px;
}

.modelIDPageModelVarTable th {
  border-bottom-style: solid;
  border-color: var(--buttonColor);
  border-collapse: collapse;
  border-width: 2px;
  padding: 5px;
}

#modelIDPageModelTimeInfo {
  margin-top: 35px;
  margin-bottom: 35px;
  border-style: solid;
  border-color: var(--textColor);
  border-radius: 10px;
  border-width: 3px;
  box-sizing: border-box;
  padding: 20px;
  padding-bottom: 30px;
  display: grid;
  grid-template-columns: 30% 20% 30% 20%;
  grid-template-rows: 50px 50px;
}

#modelIDPageModelTimeInfo .modelIDPageModelInfo {
  text-align: right;
  margin-right: 25px;
  font-weight: bolder;
}

#modelIDPageInputTable {
  margin-bottom: 30px;
}

#modelIDPageChangeModelStatus {
  background-color: transparent;
  color: transparent;
  box-shadow: none;
  width: 30px;
  height: 30px;
  margin-left: 10px;
}

#modelIDPageStatusBox {
  display: flex;
  align-items: center;
  margin-top: 18px;
}

#modelIDPageStatusBox .modelIDPageGetModelInfo {
  width: 60px;
}

#modelIDPageGoToTestPage {
  margin-right: 30px;
}
</style>
