<template>
  <div id="mainPageDivBox">
    <div id="mainPageContentBox">
      <div id="mainPageInfoBox">
        <p id="mainPageSlogan">Machine Learning Everywhere</p>
        <p id="mainPageDes">机器学习在线部署系统，提供多种机器学习的部署方案！实现机器学习自由！</p>
        <p class="projectTitle" id="mainPageProjectName">by TeAM</p>
      </div>
      <img name="mainPagePic1.png" class="themeImage" alt="robotPic" id="mainPageRobotPic">
    </div>
    <button @click="changePageToModel" id="mainPageToModelPageButton">
      开始
    </button>
    <div id="blockRobotPic"></div>
  </div>
</template>

<script>
import axios from 'axios';
import changeAllImgUrl from '@/getThemeImg';

function changeMainPageDivBoxSize() {
  const cont = document.getElementById('mainPageDivBox');
  const cont2 = document.getElementById('mainPageSlogan');
  const des = document.getElementById('mainPageDes');
  if (window.innerWidth <= 800) {
    cont.style.width = `${window.innerWidth * 0.95}px`;
    cont2.style.fontSize = '35px';
    des.style.fontSize = '15px';
  } else if (window.innerWidth <= 1100) {
    cont.style.width = `${window.innerWidth * 0.90}px`;
    cont2.style.fontSize = '45px';
    des.style.fontSize = '18px';
  } else if (window.innerWidth <= 1300) {
    cont.style.width = `${window.innerWidth * 0.85}px`;
    cont2.style.fontSize = '55px';
    des.style.fontSize = '20px';
  } else {
    cont.style.width = `${window.innerWidth * 0.80}px`;
    cont2.style.fontSize = '70px';
    des.style.fontSize = '25px';
  }
}

export default {
  data() {
    return {
    };
  },
  methods: {
    changePageToModel(event) {
      this.$router.push({
        name: 'model',
      });
    },
  },
  mounted() {
    changeMainPageDivBoxSize();
    window.onresize = changeMainPageDivBoxSize;
    changeAllImgUrl();
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
  margin-top: 35px;
}

#mainPageRobotPic {
  width: 65%;
}

#mainPageContentBox {
  display: flex;
  align-items: center;
  text-align: left;
  justify-content: space-between;
}

#mainPageInfoBox {
  width: 25%;
  display: flex;
  flex-direction: column;
}

#mainPageSlogan {
  font-family: 'Courier New', Courier, monospace;
  font-weight: bolder;
  margin: 0;
}

#mainPageProjectName {
  font-size: 30px;
  font-weight: bolder;
  text-align: right;
  margin: 0;
}

#mainPageDes {
  color: var(--mainPageNotImportantTextColor);
}

#mainPageToModelPageButton {
  margin-top: 25px;
  width: 205px;
  height: 75px;
  font-size: 23px;
}
</style>
