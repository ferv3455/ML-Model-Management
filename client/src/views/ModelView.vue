<template>
  <div id="mainPageDivBox">
    <h1 id="mainPageTitle">
      模型列表页面
    </h1>
    <table id="mainPageUploadTable">
      <tr>
        <th>模型名称</th>
        <th>描述</th>
        <th>类型</th>
        <th>算法</th>
        <th>上传时间</th>
      </tr>
      <tr v-for="model in models" :key="model" onmouseover="this.style.backgroundColor='var(--buttonTransColor)';"
        onmouseout="this.style.backgroundColor='var(--backgroundColor)'">
        <td @mouseover="dialogCheckModelDetail">
          <router-link :to="{ name: 'modelID', params: { modelID: model.id } }">
            {{ model.name }}
          </router-link>
        </td>
        <td>{{ model.des }}</td>
        <td>{{ model.type }}</td>
        <td>{{ model.algo }}</td>
        <td>{{ formatDate(model.time) }}</td>
      </tr>
    </table>
    <button @click="changePageToUpload" id="mainPageUploadButton" @mouseover="dialogClickToUploadModel">
      <img id="mainPageUploadIcon" class="themeImage" name="uploadIcon.png" alt="Icon">
      上传模型
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import setDialog from '@/live2dSetDialog';
import changeAllImgUrl from '@/getThemeImg';
import getBackUrl from '../getIP';

function changeMainPageDivBoxSize() {
  const cont = document.getElementById('mainPageDivBox');
  if (window.innerWidth <= 800) {
    cont.style.width = `${window.innerWidth * 0.95}px`;
  } else {
    cont.style.width = `${window.innerWidth * 0.80}px`;
  }
}

export default {
  data() {
    return {
      models: [{
        id: 1,
        name: 'testModel1',
        des: 'This is a test model',
        type: 'pmml',
        algo: 'SVC',
        time: Date.now() / 1000,
      }, {
        id: 2,
        name: 'testModel2',
        des: 'This is another test model',
        type: 'onnx',
        algo: 'CNN',
        time: Date.now() / 1000,
      },
      ],
    };
  },
  methods: {
    changePageToUpload(event) {
      this.$router.push({
        name: 'upload',
      });
    },
    formatDate(value) {
      const date = new Date(value * 1000);
      return date.toLocaleString();
    },
    dialogCheckModelDetail(event) {
      setDialog('*⸜( •ᴗ• )⸝*点击这里可以查看此模型的详情', 1500);
    },
    dialogClickToUploadModel(event) {
      setDialog('点击这里可以上传新模型哟๐•ᴗ•๐', 1500);
    },
  },
  mounted() {
    changeMainPageDivBoxSize();
    window.onresize = changeMainPageDivBoxSize;
    changeAllImgUrl();
    setTimeout(() => { setDialog('', 0); }, 100);

    axios.get(getBackUrl('/model'), {
      params: {},
    }).then((res) => {
      this.models = res.data.models;
    }).catch((error) => {
      console.log(error);
    });
  },
};

</script>

<style>
#mainPageDivBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: auto;
  margin-right: auto;
}

#mainPageUploadTable {
  min-width: 100%;
  text-align: center;
  border-style: solid;
  border-color: var(--textColor);
  border-radius: 10px;
  border-width: 3px;
}

#mainPageUploadTable th {
  border-bottom-style: solid;
  border-color: var(--textColor);
  border-collapse: collapse;
  border-width: 2px;
  padding: 7px;
}

#mainPageUploadTable td {
  padding: 7px;
}

#mainPageUploadButton {
  margin-top: 25px;
  display: flex;
  align-items: center;
}

#mainPageUploadIcon {
  width: 30px;
  margin-left: 15px;
  margin-right: 5px;
}
</style>
