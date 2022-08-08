<template>
  <div>
    <h1 id="modelIDPageTitle">
      模型详细信息页面
    </h1>
    <div id="modelIDPageModelDetail">
      <div id="modelIDPageModelDetailBasic" class="divUse">
        <p class="modelIDPageModelInfo">名称</p>
        <p class="modelIDPageGetModelInfo">{{ modelName }}</p>
        <p class="modelIDPageModelInfo">类型</p>
        <p class="modelIDPageGetModelInfo">{{ modelType }}</p>
        <p class="modelIDPageModelInfo">算法</p>
        <p class="modelIDPageGetModelInfo">{{ modelAlgo }}</p>
        <p class="modelIDPageModelInfo">上传时间</p>
        <p class="modelIDPageGetModelInfo">{{ modelTime }}</p>
        <!--TODO 添加换行时的自适应 -->
        <p class="modelIDPageModelInfo">描述</p>
        <p class="modelIDPageGetModelInfo" id="modelIDPageModelDes">{{ modelDes }}</p>
      </div>
      <div id="modelIDPageModelVar" class="divUse">
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
      <div>
        <button @click="goToTestPage" id="modelIDPageGoToTestPage" @mouseover="clickToGoToTestPage">进入模型测试</button>
        <button @click="goToServicePage" id="modelIDPageGoToServicePage"
          @mouseover="clickToGoToServicePage">进入服务列表</button>
      </div>
    </div>
    <button @click="backToModelPage" @mouseover="clickToGoToModelPage" id="modelIDPageBackToModelPage"
      class="roundButton returnButton">
      <img class="returnIcon themeImage" name="returnIcon.png" alt="return">
    </button>
  </div>
</template>

<script>
import changeAllImgUrl from '@/getThemeImg';
import getBackUrl from '@/getIP';
import setDialog from '@/live2dSetDialog';
import axios from 'axios';

function changeModelDetailSize() {
  const cont = document.getElementById('modelIDPageModelDetailBasic');
  const cont2 = document.getElementById('modelIDPageModelVar');
  if (window.innerWidth <= 800) {
    cont.style.width = `${window.innerWidth * 0.95}px`;
    cont2.style.width = `${window.innerWidth * 0.95}px`;
  } else {
    cont.style.width = '700px';
    cont2.style.width = '700px';
  }
}

export default {
  data() {
    return {
      // 从表单获得的信息（此处不包含模型文件信息）
      modelID: this.$route.params.modelID,
      modelName: 'testName',
      modelDes: 'xxxxxxxxxxxxxxx xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
      modelType: 'pmml',
      modelAlgo: 'xxxxxx',
      modelTime: '13:20',
      modelInputs: [
        {
          name: 'input1',
          type: 'image',
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
    };
  },
  methods: {
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
          modelName: this.modelName,
          modelInputs: JSON.stringify(this.modelInputs),
        },
      });
    },
    goToServicePage(event) {
      this.$router.push({
        name: 'service',
        params: {
          modelID: this.modelID,
          modelName: this.modelName,
        },
      });
    },
    clickToGoToTestPage(event) {
      setDialog('从这可以进入模型测试页❤︎', 1500);
    },
    clickToGoToModelPage(event) {
      setDialog('点击返回模型列表页ʕ•̀ o •́ʔ', 1500);
    },
    clickToGoToServicePage(event) {
      setDialog('(◍>o<◍)✩这里可以查看此模型有多少个服务', 1500);
    },
  },
  mounted() {
    changeModelDetailSize();
    window.onresize = changeModelDetailSize;
    changeAllImgUrl();
    setTimeout(() => { setDialog('', 0); }, 100);

    // get modelID info
    const path = `/model/${this.modelID}`;
    axios.get(getBackUrl(path), {
      params: {},
    })
      .then((res) => {
        if (res.data.exist === true) {
          this.modelName = res.data.name;
          this.modelDes = res.data.des;
          this.modelType = res.data.type;
          this.modelAlgo = res.data.algo;
          this.modelTime = res.data.time;
          this.modelInputs = res.data.inputs;
          this.modelOutputs = res.data.outputs;
        } else {
          alert('模型不存在');
        }
      })
      .catch((error) => {
        console.log(error);
      });
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
  padding: 20px;
  padding-bottom: 25px;
  display: grid;
  grid-template-columns: 20% 20% 25% 35%;
  grid-template-rows: 50px 50px auto;
}

#modelIDPageModelDetailBasic .modelIDPageModelInfo {
  text-align: right;
  margin-right: 30px;
  font-weight: bolder;
}

#modelIDPageModelVar {
  margin-top: 35px;
  display: flex;
  flex-direction: column;
  padding: 20px;
  align-items: center;
  margin-bottom: 20px;
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

#modelIDPageInputTable {
  margin-bottom: 30px;
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

#modelIDPageModelDes {
  background-color: transparent;
  width: 380%;
  overflow: hidden;
  text-overflow: ellipsis;
  word-wrap: break-word;
  margin-top: 20px;
  height: auto;
}
</style>
