<template>
  <div id="PreProPageBox">
    <h1 id="PreProPageTitle">
      预处理文件载入页面
      <div class="modelNow">当前模型：{{ modelName }}</div>
    </h1>
    <div id="uploadPageImportPrePro" class="divUse">
      <p class="loadedPrePRoFile" id="LoadedPreProInfo">当前预处理脚本文件：</p>
      <div id="LoadedDiv" v-if="Loaded === true">
        <a :href="LoadedProPath" target="_blank" class="loadedLink" :download="LoadedProName">{{ LoadedProName }}</a>
        <button @click="DeletePrePro" @mouseover="clickToDeletePrePro" id="deletePrePro">删除当前文件</button>
      </div>
      <p v-else id="NoLoaded">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;无已载入的预处理脚本文件</p>
      <p class="loadedPrePro" id="LoadedPreProInfo">当前预处理脚本描述：</p>
      <textarea v-model="LoadedProDescription" id="LoadedProDescription" readonly></textarea>
      <p class="uploadPageImportPreProDetail" id="uploadPagePreProDescription">预处理描述</p>
      <textarea v-model="ProDescription" id="uploadPageEnterProDescription"></textarea>
      <p class="uploadPageImportPreProDetail" id="uploadPagePreProFile">预处理文件</p>
      <input id="uploadPageEnterPreProFile" type="file" @mouseover="clickToGetFile" :accept="'.' + 'py'">
      <div id="preProPageUploadBox">
        <button @click="uploadNewPreprocess" @mouseover="clickToUpload" id="preproPageUploadButton">
          <img id="preproPageUploadIcon" src="../assets/uploadIcon.png" class="uploadIcon" alt="Icon">
          上传
        </button>
      </div>
      <button @click="backToModelIDPage" @mouseover="clickToBackToModelID" id="goToModelIDPageButton"
        class="roundButton returnButton">
        <img class="returnIcon" src="../assets/returnIcon.png" alt="return">
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import setDialog from '@/live2dSetDialog';
import changeAllImgUrl from '@/getThemeImg';
import getBackUrl from '../getIP';

function changePreProViewSize() {
  const cont = document.getElementById('uploadPageImportPrePro');
  if (window.innerWidth <= 800) {
    cont.style.width = `${window.innerWidth * 0.8}px`;
  } else {
    cont.style.width = '640px';
  }
}

export default {
  data() {
    return {
      // 从表单获得的信息（此处不包含模型文件信息）
      modelID: parseInt(this.$route.params.modelID, 10),
      modelName: '',
      ProDescription: '',
      LoadedProDescription: '并未加载预处理脚本文件',
      LoadedProPath: '',
      LoadedProName: 'xxx',
      Loaded: false,
    };
  },
  methods: {
    getPrePro() {
      const path = `/model/${this.modelID}/preprocess`;
      axios.get(getBackUrl(path))
        .then((res) => {
          if (res.data.status === 'success') {
            this.LoadedProDescription = res.data.prodes;
            this.LoadedProName = res.data.name;
            this.Loaded = true;
            const binaryData = [];
            binaryData.push(res.data.f);
            const protype = res.data.type;
            const f = new File(binaryData, this.LoadedProName);
            this.LoadedProPath = window.URL.createObjectURL(f);
          } else if (res.data.status === 'empty') {
            this.LoadedProDescription = '并未加载预处理脚本文件';
            this.Loaded = false;
          }
        })
        .catch((error) => {
          console.log(error);
          if (error.response && error.response.status === 404) {
            alert('信息不存在');
          } else if (error.response && error.response.status === 406) {
            alert('系统处理错误');
          } else {
            alert('服务器错误');
          }
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
      const path = `/model/${this.modelID}/preprocess`;
      axios.delete(getBackUrl(path))
        .then((res) => {
          this.getPrePro();
          this.Loaded = false;
        })
        .catch((error) => {
          console.log(error);
          if (error.response && error.response.status === 404) {
            alert('信息不存在');
          } else if (error.response && error.response.status === 406) {
            alert('系统处理错误');
          } else {
            alert('服务器错误');
          }
        });
    },
    uploadNewPreprocess(event) {
      const path = `/model/${this.modelID}/preprocess`;
      const f = document.getElementById('uploadPageEnterPreProFile').files[0];
      const postRequest = new FormData();

      if (document.getElementById('uploadPageEnterPreProFile').value === '') {
        alert('预处理文件为空！');
        return;
      }

      postRequest.append('prodes', this.ProDescription);
      postRequest.append('file', f);
      postRequest.append('filename', f.name);
      axios.post(getBackUrl(path), postRequest, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
        .then((res) => {
          this.getPrePro();
        })
        .catch((error) => {
          console.log(error);
          if (error.response && error.response.status === 404) {
            alert('信息不存在');
          } else if (error.response && error.response.status === 406) {
            alert('系统处理错误');
          } else {
            alert('服务器错误');
          }
        });
    },
    clickToBackToModelID() {
      setDialog('੭˙ᗜ˙)੭ ♡点击返回上一页，那里可以查看模型详情', 1500);
    },
    clickToDeletePrePro() {
      setDialog('点击会清除当前的预处理文件(((> <)))！要三思而后行哟~', 1500);
    },
    clickToUpload() {
      setDialog('(◍>o<◍)✩记得要填完所有选项才点击提交哟！', 1500);
    },
    clickToGetFile() {
      setDialog('请上传.py类型的文件哟~(=´ω`=)', 1500);
    },
    getModelName() {
      const path = `/model/${this.modelID}`;
      axios.get(getBackUrl(path))
        .then((res) => {
          this.modelName = res.data.name;
        })
        .catch((error) => {
          console.log(error);
          if (error.response && error.response.status === 404) {
            alert('信息不存在');
          } else if (error.response && error.response.status === 406) {
            alert('系统处理错误');
          } else {
            alert('服务器错误');
          }
        });
    },
  },
  mounted() {
    changePreProViewSize();
    changeAllImgUrl();
    this.getModelName();
    window.onresize = changePreProViewSize;
    setTimeout(() => { setDialog('', 0); }, 100);
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

#uploadPageImportPrePro #NoLoaded {
  font-size: 80%;
  font-weight: lighter;
}

#LoadedDiv {
  display: flex;
  align-items: center;
  flex-direction: row;
}

#deletePrePro {
  margin-left: 40px;
  height: 70%;
}

#uploadPageImportPrePro p {
  font-weight: bolder;
}

#uploadPageImportPrePro textarea,
#uploadPageImportPrePro input {
  width: 100%;
}

#preProPageUploadBox {
  display: flex;
  align-items: center;
  flex-direction: column;
}
</style>
