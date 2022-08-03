<template>
  <div id="testPageDivBox">
    <h1>
      模型测试页面
      <div class="modelNow">当前模型：{{ modelID }}</div>
    </h1>
    <div id="testPageLeftRight">
      <div class="testPageSmallBox">
        <h2 class="testPageSmallBoxTitle"> 输入</h2>
        <div id="testPageShowMode">
          <p>当前模式：{{ mode }}</p>
          <button @click="changeMode" id="testPageChangeMode">
            <img class="changeStatusIcon" title="切换输入模式" src="../assets/changeStatusIcon.png" alt="changeIcon">
          </button>
          <div style="flex-grow: 1"></div>
          <button @dblclick="clear" id="testPageClearButton">
            <img src="../assets/binIcon.png" title="双击清除当前输入" alt="binIcon" class="binIcon">
          </button>
        </div>
        <div v-if="mode === 'json'">
          <textarea v-model="jsonInput" id="testPageJsonInput"></textarea>
        </div>
        <div v-if="mode === 'form'">
          <div id="testPageFormArea">
            <div class="testPageInputVariance" v-for="variance in variances" :key="variance">
              <p>{{ variance.name }}</p>
              <input :id="'var_' + variance.name">
            </div>
          </div>
        </div>
        <div id="testPageButton">
          <button @click="submit" id="testPageSubmitButton">提交</button>
        </div>
      </div>
      <div class="testPageSmallBox">
        <h2 class="testPageSmallBoxTitle"> 输出</h2>
        <textarea v-model="output" readonly id="testPageOutput"></textarea>
      </div>
    </div>
  </div>
  <button @click="backToModelIDPage" id="testPageReturnButton" class="roundButton returnButton">
    <img class="returnIcon" src="../assets/returnIcon.png" alt="return">
  </button>
</template>

<script>
import axios from 'axios';

function changeTextPageLeftRightBoxDirection() {
  const cont = document.getElementById('testPageLeftRight');
  if (window.innerWidth <= 800) {
    cont.style.width = `${window.innerWidth * 0.90}px`;
    cont.style.flexDirection = 'column';
  } else {
    cont.style.width = `${window.innerWidth * 0.8}px`;
    cont.style.flexDirection = 'row';
  }
}

export default {
  data() {
    return {
      modelID: this.$route.params.modelID,
      mode: 'form',
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
      // put submitObject
      let path = '/model/' + this.modelID.toString() + '/test';
      axios.post(getBackUrl(path), {
        submitObject: submitObject,
      })
        .then((res) => {
          this.output = res.data.output;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
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
  mounted() {
    changeTextPageLeftRightBoxDirection();
    window.onresize = changeTextPageLeftRightBoxDirection;
  },
};

</script>

<style>
#testPageLeftRight {
  display: flex;
}

.testPageSmallBox {
  flex-grow: 1;
  width: 100%;
  margin: 10px;
  border-style: solid;
  border-color: var(--textColor);
  border-radius: 10px;
  border-width: 3px;
  box-sizing: border-box;
  padding: 20px;
}

.testPageSmallBoxTitle {
  margin: 0px;
  margin-bottom: 10px;
}

#testPageDivBox {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#testPageClearButton {
  width: 25px;
  margin-right: 15px;
  height: auto;
  background-color: transparent;
  box-shadow: none;
}

#testPageChangeMode {
  background-color: transparent;
  color: transparent;
  box-shadow: none;
  width: 30px;
  height: 30px;
  margin-left: 30px;
}

#testPageShowMode {
  display: flex;
  align-items: center;
  margin: 0px;
  margin-top: -10px;
  width: 100%;
}

#testPageShowMode p {
  width: 150px;
  margin: 0px;
}

#testPageJsonInput {
  height: 250px;
  width: 99%;
}

#testPageButton {
  display: flex;
  justify-content: center;
}

.testPageInputVariance p {
  margin: 0px;
  margin-bottom: 10px;
  font-weight: bolder;
}

.testPageInputVariance input {
  margin: 0px;
  margin-bottom: 20px;
  width: 99%;
}

#testPageFormArea {
  height: 250px;
  overflow: scroll;
  overflow-x: hidden;
}

#testPageOutput {
  width: 99%;
  height: 340px;
}
</style>
