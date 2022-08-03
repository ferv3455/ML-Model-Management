<template>
  <div id="predictPageDivBox">
    <h1>
      部署接口页面
      <div class="modelNow">当前服务：{{ serviceID }}</div>
      <div class="modelNowInService">当前模型：{{ modelID }}</div>
    </h1>
    <div id="predictPageBox">
      <div class="predictPageSmallBox" id="predictPageInputBox">
        <h2 class="predictPageSmallBoxTitle">Json输入</h2>
        <textarea v-model="jsonInput" id="predictPageJsonInput"></textarea>
        <div id="predictPageCurlBox">
          <h2 class="predictPageSmallBoxTitle">Curl代码</h2>
          <div id="predictPageCurlBoxGrow"></div>
          <button @click="generateCurl" id="predictPageGenerateCurl">
            <img src="../assets/generateIcon.png" title="生成curl代码" alt="generateIcon" class="generateIcon">
          </button>
          <button @click="copyCurl" id="predictPageCopyCurl">
            <img src="../assets/copyIcon.png" title="复制curl代码" alt="copyIcon" class="copyIcon">
          </button>
        </div>
        <textarea v-model="curlInput" id="predictPageCurlInput" readonly></textarea>
        <div id="predictPageButton">
          <button @click="submit" id="predictPageSubmitButton">提交</button>
        </div>
      </div>
      <div class="predictPageSmallBox" id="predictPageOutputBox">
        <h2>输出</h2>
        <textarea v-model="output" id="predictPageOutput" readonly></textarea>
      </div>
    </div>
    <button @click="goToBatchPage" id="predictPageGoToBatchPage">前往批量任务列表</button>
    <button @click="goToServicePage" id="predictPageGoToServicePage" class="roundButton returnButton">
      <img class="returnIcon" src="../assets/returnIcon.png" alt="return">
    </button>
  </div>
</template>

<script>
import axios from 'axios';

function changePredictPageBoxDirection() {
  const cont = document.getElementById('predictPageBox');
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
      serviceID: this.$route.params.serviceID,
      output: 'this is output!', // 测试用，提交后等待后端返回输出
      jsonInput: '',
      curlInput: '',
    };
  },
  methods: {
    submit(event) {
      const submitObject = JSON.parse(this.jsonInput);
      // console.log(submitObject);
      // put submitObject
      path = '/model/' + this.modelID.toString() + '/service/' + this.serviceID.toString() + '/quick';
      axios.post(getBackUrl(path), {
        submitObject: submitObject,
      })
        .then((res) => {
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    generateCurl(event) {
      this.curlInput = 'Get curl code!!';
      // TODO
      // 需要生成向后端请求的curl代码
    },
    goToBatchPage(event) {
      this.$router.push({
        name: 'batch',
        params: {
          modelID: this.modelID,
          serviceID: this.serviceID,
        },
      });
    },
    goToServicePage(event) {
      this.$router.push({
        name: 'service',
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
  mounted() {
    changePredictPageBoxDirection();
    window.onresize = changePredictPageBoxDirection;
  },
};
</script>

<style>
#predictPageDivBox {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#predictPageBox {
  display: flex;
}

.predictPageSmallBox {
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

#predictPageInputBox {
  display: flex;
  flex-direction: column;
}

.predictPageSmallBox h2 {
  margin: 0px;
  margin-bottom: 10px;
}

.predictPageSmallBoxTitle {
  font-size: 28px;
}

#predictPageInputBox textarea {
  width: 99%;
  height: 180px;
  margin-bottom: 20px;
}

#predictPageOutput {
  width: 99%;
  height: 500px;
}

#predictPageCopyCurl {
  width: 25px;
  height: 25px;
  background-color: transparent;
  box-shadow: none;
  margin-right: 20px;
  margin-top: 12px;
}

#predictPageGenerateCurl {
  width: 26px;
  height: 26px;
  background-color: transparent;
  box-shadow: none;
  margin-top: 12px;
  margin-right: 10px;
}

#predictPageCurlBox {
  display: flex;
  flex-direction: row;
}

#predictPageCurlBoxGrow {
  flex-grow: 1;
}

#predictPageButton {
  display: flex;
  justify-content: center;
  margin-top: -5px;
}

#predictPageGoToBatchPage {
  position: absolute;
  top: 85px;
  right: 10px;
}
</style>
