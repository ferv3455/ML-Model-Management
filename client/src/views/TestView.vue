<template>
  <div id="testPageDivBox">
    <h1>
      模型测试页面
      <div class="modelNow">当前模型：{{ modelName }}</div>
    </h1>
    <div id="testPageLeftRight">
      <div class="testPageSmallBox divUse">
        <h2 class="testPageSmallBoxTitle"> 输入</h2>
        <div id="testPageShowMode">
          <p>当前模式：{{ mode }}</p>
          <button @click="changeMode" id="testPageChangeMode">
            <img class="changeStatusIcon themeImage" title="切换输入模式" @mouseover="dialogChangeInputMode"
              name="changeStatusIcon.png" alt="changeIcon">
          </button>
          <div style="flex-grow: 1"></div>
          <button @dblclick="clear" id="testPageClearButton">
            <img name="binIcon.png" title="双击清除当前输入" alt="binIcon" @mouseover="dialogThinkTwiceBeforeClear"
              class="binIcon themeImage">
          </button>
        </div>
        <div v-if="mode === 'json'">
          <textarea v-model="jsonInput" id="testPageJsonInput"></textarea>
        </div>
        <div v-if="mode === 'form'">
          <div id="testPageFormArea">
            <div class="testPageInputVariance" v-for="variance in variances" :key="variance">
              <p>{{ variance.name }}</p>
              <div v-if="variance.type !== 'image'">
                <input :id="'var_' + variance.name">
              </div>
              <div v-else>
                <input :id="'var_' + variance.name" type="file" ref="file" accept=".png, .jpg, .jpeg, .bmp"
                  @change="onImageChange(variance.name)">
                <img :id="'var_' + variance.name + '_image'" class="testPageUploadImage" alt="inputImage"
                  src="../assets/emptyPic.png">
              </div>
            </div>
          </div>
        </div>
        <div id="testPageButton">
          <button @click="submit" @mouseover="dialogCheckBeforeSubmitInput" id="testPageSubmitButton">提交</button>
        </div>
      </div>
      <div class="testPageSmallBox divUse">
        <h2 class="testPageSmallBoxTitle"> 输出</h2>
        <textarea v-model="output" readonly id="testPageOutput"></textarea>
      </div>
    </div>
  </div>
  <button @click="backToModelIDPage" @mouseover="dialogClickToGoToModelIDPage" id="testPageReturnButton"
    class="roundButton returnButton">
    <img class="returnIcon themeImage" name="returnIcon.png" alt="return">
  </button>
</template>

<script>
import axios from 'axios';
import setDialog from '@/live2dSetDialog';
import changeAllImgUrl from '@/getThemeImg';
import getBackUrl from '../getIP';

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

function getBase64Image(img) {
  const canvas = document.createElement('canvas');
  canvas.width = img.width;
  canvas.height = img.height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0, img.width, img.height);
  const dataURL = canvas.toDataURL('image/png');
  return dataURL.replace('data:image/png;base64,', '');
}

export default {
  data() {
    return {
      modelID: this.$route.params.modelID,
      modelName: this.$route.params.modelName,
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
          if (this.variances[i].type === 'image') {
            const imgFile = document.getElementById(`var_${this.variances[i].name}`);
            document.getElementById(`var_${this.variances[i].name}_image`).classList.remove('testPageImageLoaded');
          }
        }
      }
    },
    submit(event) {
      let submitObject = {};
      if (this.mode === 'json') {
        try {
          submitObject = JSON.parse(this.jsonInput);
        } catch (err) {
          alert(err);
          return;
        }
      } else {
        for (let i = 0; i < this.variances.length; i += 1) {
          const inputBox = document.getElementById(`var_${this.variances[i].name}`);
          if (inputBox.value === '') {
            alert(`变量 ${this.variances[i].name} 为空！`);
            return;
          }
          if (this.variances[i].type !== 'image') {
            submitObject[this.variances[i].name] = inputBox.value;
          } else {
            const inputImg = document.getElementById(`var_${this.variances[i].name}_image`);
            submitObject[this.variances[i].name] = getBase64Image(inputImg);
          }
        }
      }
      console.log(submitObject);
      // put submitObject
      const path = `/model/${this.modelID}/test`;
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
    backToModelIDPage(event) {
      this.$router.push({
        name: 'modelID',
        params: {
          modelID: this.modelID,
        },
      });
    },
    onImageChange(name) {
      const imgFile = document.getElementById(`var_${name}`);
      if (imgFile.files.length === 0) {
        document.getElementById(`var_${name}_image`).classList.remove('testPageImageLoaded');
      } else {
        const imageToShow = window.URL.createObjectURL(imgFile.files[0]);
        document.getElementById(`var_${name}_image`).src = imageToShow;
        document.getElementById(`var_${name}_image`).classList.add('testPageImageLoaded');
      }
    },
    dialogClickToGoToModelIDPage(event) {
      setDialog('੭˙ᗜ˙)੭ ♡点击返回上一页，那里可以查看模型详情', 1500);
    },
    dialogCheckBeforeSubmitInput(event) {
      setDialog('(◍>o<◍)✩记得要填完所有选项才点击提交哟！', 1500);
    },
    dialogChangeInputMode(event) {
      setDialog('不喜欢当前的输入模式的话,可以换一种模式输入哟~', 1500);
    },
    dialogThinkTwiceBeforeClear(event) {
      setDialog('双击会清除当前的所有输入(((> <)))！要三思而后行哟~', 1500);
    },
  },
  mounted() {
    changeTextPageLeftRightBoxDirection();
    window.onresize = changeTextPageLeftRightBoxDirection;
    changeAllImgUrl();
    setTimeout(() => { setDialog('', 0); }, 100);
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

.testPageUploadImage {
  width: 0px;
}

.testPageImageLoaded {
  width: 150px;
}
</style>
