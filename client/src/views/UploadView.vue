<template>
  <div id="uploadPageBox">
    <h1 id="uploadPageTitle">
      模型导入页面
    </h1>
    <div id="uploadPageImportModel" class="divUse">
      <p class="uploadPageImportModelDetail" id="uploadPageModelName">模型名称</p>
      <input v-model="modelName" id="uploadPageEnterModelName">
      <p class="uploadPageImportModelDetail" id="uploadPageModelDescription">模型描述</p>
      <textarea v-model="modelDescription" id="uploadPageEnterModelDescription"></textarea>
      <p class="uploadPageImportModelDetail" id="uploadPageModelType">模型类型</p>
      <select v-model="modelType" id="uploadPageEnterModelType" value="pmml">
        <option value="pmml">PMML</option>
        <option value="onnx">ONNX</option>
        <option value="pkl">PKL</option>
        <option value="pth">PTH</option>
      </select>
      <p class="uploadPageImportModelDetail" id="uploadPageModelFile">模型文件</p>
      <input id="uploadPageEnterModelFile" @mouseover="dialogUploadFileType" type="file" :accept="'.' + this.modelType">
      <button @click="uploadNewModel" @mouseover="dialogClickToUpload" id="uploadPageUploadButton">
        <img id="uploadPageUploadIcon" src="../assets/uploadIcon.png" class="uploadIcon" alt="Icon">
        上传
      </button>
      <button @click="goToModelPage" @mouseover="dialogClickToModelPage" id="goToModelPageButton"
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

function changeTableSize() {
  const cont = document.getElementById('uploadPageImportModel');
  if (window.innerWidth <= 800) {
    cont.style.width = `${window.innerWidth * 0.9}px`;
  } else {
    cont.style.width = '720px';
  }
}

export default {
  data() {
    return {
      // 从表单获得的信息（此处不包含模型文件信息）
      modelName: '',
      modelDescription: '',
      modelType: 'pmml',
    };
  },
  methods: {
    uploadNewModel(event) {
      // Model upload
      const path = '/model';
      const f = document.getElementById('uploadPageEnterModelFile').files[0];
      const postRequest = new FormData();
      postRequest.append('name', this.modelName);
      postRequest.append('type', this.modelType);
      postRequest.append('des', this.modelDescription);
      postRequest.append('file', f);
      axios.post(getBackUrl(path), postRequest, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
        .then((res) => {
          if (res.data.status === 'success') {
            this.$router.push({
              name: 'model',
            });
          } else {
            const mes = `创建新模型失败：${res.data.reason}`;
            alert(mes);
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    goToModelPage(event) {
      this.$router.push({
        name: 'model',
        params: {
        },
      });
    },
    dialogClickToModelPage(event) {
      setDialog('点击返回模型列表页ʕ•̀ o •́ʔ', 1500);
    },
    dialogClickToUpload(event) {
      setDialog('(◍>o<◍)✩记得要填完所有选项才点击提交哟！', 1500);
    },
    dialogUploadFileType(event) {
      setDialog('记得上传和上边模型类型相同的文件哟~(=´ω`=)', 1500);
    },
  },
  mounted() {
    changeAllImgUrl();
    changeTableSize();
    window.onresize = changeTableSize;
    setTimeout(() => { setDialog('', 0); }, 100);
  },
};

</script>

<style>
#uploadPageBox {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#uploadPageImportModel {
  padding: 20px;
  display: grid;
  grid-template-columns: 25% 75%;
  grid-template-rows: 45px 110px 45px 45px 85px;
  grid-template-areas: 'name enterName'
    'des enterDes'
    'type enterType'
    'file enterFile'
    'button button';
  justify-items: center;
  align-items: center;
}

#uploadPageModelName {
  grid-area: name;
}

#uploadPageEnterModelName {
  grid-area: enterName;
}

#uploadPageModelDescription {
  grid-area: des;
}

#uploadPageEnterModelDescription {
  grid-area: enterDes;
  width: 90%;
  height: 85px;
  resize: none;
}

#uploadPageModelType {
  grid-area: type;
}

#uploadPageEnterModelType {
  grid-area: enterType;
  width: 91%;
  height: 32px;
}

#uploadPageModelFile {
  grid-area: file;
}

#uploadPageEnterModelFile {
  grid-area: enterFile;
}

#uploadPageUploadButton {
  margin-top: 30px;
  grid-area: button;
  display: flex;
  align-items: center;
}

#uploadPageUploadIcon {
  width: 30px;
  margin-left: 35px;
  margin-right: 5px;
}

.uploadPageImportModelDetail {
  font-weight: bolder;
}
</style>
