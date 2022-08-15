<template>
  <div id="predictPageDivBox">
    <h1>
      部署接口页面
      <div class="modelNow">当前服务：{{ serviceName }}</div>
      <div class="modelNowInService">当前模型：{{ modelName }}</div>
    </h1>
    <div id="predictPageBox">
      <div class="predictPageSmallBox divUse" id="predictPageInputBox">
        <h2 class="predictPageSmallBoxTitle">Json输入</h2>
        <textarea v-model="jsonInput" id="predictPageJsonInput"></textarea>
        <div id="predictPageCurlBox">
          <h2 class="predictPageSmallBoxTitle">Curl代码</h2>
          <div id="predictPageCurlBoxGrow"></div>
          <button @click="generateCurl" @mouseover="dialogClickToGenerateCurl" id="predictPageGenerateCurl">
            <img src="../assets/generateIcon.png" title="生成curl代码" alt="generateIcon" class="generateIcon">
          </button>
          <button @click="copyCurl" @mouseover="dialogClickToCopyCurl" id="predictPageCopyCurl">
            <img src="../assets/copyIcon.png" title="复制curl代码" alt="copyIcon" class="copyIcon">
          </button>
        </div>
        <textarea v-model="curlInput" id="predictPageCurlInput" readonly></textarea>
        <div id="predictPageButton">
          <button @click="submit" @mouseover="dialogClickToSummit" id="predictPageSubmitButton">提交</button>
        </div>
      </div>
      <div class="predictPageSmallBox divUse" id="predictPageOutputBox">
        <h2>输出</h2>
        <textarea v-model="output" id="predictPageOutput" readonly></textarea>
      </div>
    </div>
    <button @click="goToBatchPage" @mouseover="dialogClickToBatchPage" id="predictPageGoToBatchPage">前往批量任务列表</button>
    <button @click="goToServicePage" @mouseover="dialogClickToServicePage" id="predictPageGoToServicePage"
      class="roundButton returnButton">
      <img class="returnIcon" src="../assets/returnIcon.png" alt="return">
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import setDialog from '@/live2dSetDialog';
import changeAllImgUrl from '@/getThemeImg';
import getBackUrl from '../getIP';

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
      modelName: this.$route.params.modelName,
      serviceID: this.$route.params.serviceID,
      serviceName: this.$route.params.serviceName,
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
      const path = `/model/${this.modelID}/service/${this.serviceID}/quick`;
      axios.post(getBackUrl(path), {
        submitObject,
      })
        .then((res) => {
          this.output = res.data.output;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    generateCurl(event) {
      this.curlInput = 'Get curl code!!';
      // 生成向后端请求的curl代码
      let curlCode = 'curl -d "';
      const jsonObject = JSON.parse(this.jsonInput);
      Object.keys(jsonObject).map((key) => {
        curlCode = `${curlCode}${key}=${jsonObject[key]}&`;
        return null;
      });
      curlCode = curlCode.slice(0, curlCode.length - 1);
      curlCode += '" -X POST ';
      const path = `/model/${this.modelID}/service/${this.serviceID}/quick`;
      const posurl = getBackUrl(path);
      curlCode += posurl;
      this.curlInput = curlCode;
    },
    goToBatchPage(event) {
      this.$router.push({
        name: 'batch',
        params: {
          modelID: this.modelID,
          modelName: this.modelName,
          serviceID: this.serviceID,
          serviceName: this.serviceName,
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
    copyCurl(event) {
      const copyElement = document.getElementById('predictPageCurlInput');
      copyElement.select();
      document.execCommand('copy');
    },
    dialogClickToServicePage(event) {
      setDialog('点击可以返回服务列表页哟(*´∀`)~♥', 1500);
    },
    dialogClickToGenerateCurl(event) {
      setDialog('点击生成curl代码前记得确保json格式的正确性哟!~♥', 1500);
    },
    dialogClickToCopyCurl(event) {
      setDialog('一键复制curl代码,解放Ctrl-C Ctrl-V(◍>o<◍)✩', 1500);
    },
    dialogClickToSummit(event) {
      setDialog('(๑ơ₃ơ)♥提交前记得确保输入的json格式是正确的哟~', 1500);
    },
    dialogClickToBatchPage(event) {
      setDialog('想要布置新任务，可以前往批量任务列表页哟(*´∀`)', 1500);
    },
  },
  mounted() {
    changePredictPageBoxDirection();
    window.onresize = changePredictPageBoxDirection;
    changeAllImgUrl();
    setTimeout(() => { setDialog('', 0); }, 100);
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
