<template>
  <div id="PreProPageBox">
    <h1 id="PreProPageTitle">
      预处理文件载入页面
      <div class="modelNow">当前模型：{{ modelName }}</div>
    </h1>
    <div id="uploadPageImportPrePro" class="divUse">
      <p class="loadedPrePRoFile" id="LoadedPreProInfo">当前预处理脚本文件：</p>
      <div id="LoadedDiv" v-if="Loaded === true">
        <a :href="LoadedProPath">{{ LoadedProName }}</a>
        <button @click="DeletePrePro" id="deletePrePro">删除当前文件</button>
      </div>
      <p v-else id="NoLoaded">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;无已载入的预处理脚本文件</p>
      <p class="loadedPrePro" id="LoadedPreProInfo">当前预处理脚本描述：</p>
      <textarea v-model="LoadedProDescription" id="LoadedProDescription" readonly></textarea>
      <p class="uploadPageImportPreProDetail" id="uploadPagePreProDescription">预处理描述</p>
      <textarea v-model="ProDescription" id="uploadPageEnterProDescription"></textarea>
      <p class="uploadPageImportPreProDetail" id="uploadPagePreProFile">预处理文件</p>
      <input id="uploadPageEnterPreProFile" type="file" :accept="'.' + 'py'">
      <button @click="uploadNewPreprocess" id="preproPageUploadButton">
        <img id="preproPageUploadIcon" src="../assets/uploadIcon.png" alt="Icon">
        上传
      </button>
      <button @click="backToModelIDPage" id="goToModelIDPageButton" class="roundButton returnButton">
        <img class="returnIcon" src="../assets/returnIcon.png" alt="return">
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import getBackUrl from '../getIP';

export default {
  data() {
    return {
      // 从表单获得的信息（此处不包含模型文件信息）
      modelID: this.$route.params.modelID,
      modelName: this.$route.params.modelName,
      ProDescription: '',
      LoadedProDescription: '并未加载预处理脚本文件',
      LoadedProPath: '',
      LoadedProName: '',
      Loaded: false,
    };
  },
  methods: {
    getPrePro() {
      const path = `/model/${this.modelID}/preprocess`;
      axios.get(getBackUrl(path), {
        params: {},
      })
        .then((res) => {
          if (res.data.state === 'success') {
            this.LoadedProDescription = res.data.ProDescription;
            this.LoadedProPath = res.data.LoadedProPath;
            this.LoadedProName = res.data.LoadedProName;
            this.Loaded = true;
          } else if (res.data.state === 'empty') {
            this.LoadedProDescription = '并未加载预处理脚本文件';
            this.Loaded = false;
          } else {
            alert('加载预处理脚本信息失败');
          }
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
    DeletePrePro(event) {
      const path = `/model/${this.modelID}/preprocess/delete`;
      axios.post(getBackUrl(path), {
        LoadedProPath: this.LoadedProPath,
        fileName: this.LoadedProName,
      })
        .then((res) => {
          this.getPrePro();
          this.Loaded = false;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    uploadNewPreprocess(event) {
      const path = `/model/${this.modelID}/preprocess`;
      const f = document.getElementById('uploadPageEnterPreProFile').files[0];
      const fileName = f.name;
      axios.post(getBackUrl(path), {
        ProDescription: this.ProDescription,
        file: f,
        fileName,
      })
        .then((res) => {
          this.getPrePro();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    this.getPrePro();
  },
};
</script>

<style>
#PreProPageBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: auto;
  margin-right: auto;
}

#uploadPageImportPrePro {
  padding: 30px 60px;
  justify-items: center;
  align-items: center;
}

#preproPageUploadButton {
  margin-top: 30px;
  grid-area: button;
  display: flex;
  align-items: center;
}

#preproPageUploadIcon {
  width: 30px;
  margin-left: 35px;
  margin-right: 5px;
}

#NoLoaded {
  font-size: 80%;
  font-weight: lighter;
}

#LoadedDiv {
  display: flex;
  align-items: center;
  flex-direction: row;
}
</style>
