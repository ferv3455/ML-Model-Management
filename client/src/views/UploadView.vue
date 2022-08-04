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
      </select>
      <p class="uploadPageImportModelDetail" id="uploadPageModelFile">模型文件</p>
      <input id="uploadPageEnterModelFile" type="file" :accept="'.' + this.modelType">
      <button @click="uploadNewModel" id="uploadPageUploadButton">
        <img id="uploadPageUploadIcon" name="uploadIcon.png" class="themeImage" alt="Icon">
        上传
      </button>
      <button @click="goToModelPage" id="goToModelPageButton" class="roundButton returnButton">
        <img class="returnIcon themeImage" name="returnIcon.png" alt="return">
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import changeAllImgUrl from '@/getThemeImg';
import getBackUrl from '../getIP';

function changeTableSize() {
  const cont = document.getElementById('uploadPageImportModel');
  if (window.innerWidth <= 800) {
    cont.style.width = `${window.innerWidth * 0.8}px`;
  } else {
    cont.style.width = '700px';
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
      axios.post(getBackUrl(path), {
        name: this.modelName,
        type: this.modelType,
        des: this.modelDescription,
        file: f,
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
  },
  mounted() {
    changeAllImgUrl();
    changeTableSize();
    window.onresize = changeTableSize;
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
</style>
