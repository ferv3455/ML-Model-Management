<template>
  <div id="appBox">
    <nav>
      <img id="logoImg" src="./assets/s02big.png" alt="logo">
      <p id="navTeamName" class="projectTitle">TeAM</p>
      <router-link class="toOtherPageNav" to="/">
        <img id="homeIcon" class="themeImage" name="homeIcon.png" alt="homeIcon">
        <p>主页</p>
      </router-link>
      <router-link class="toOtherPageNav" to="/model">
        <img id="listIcon" class="themeImage" name="listIcon.png" alt="listIcon">
        <p>模型列表</p>
      </router-link>
      <div class="toOtherPageNav">
        <img id="changeThemeIcon" class="themeImage" name="changeThemeIcon.png" alt="changeThemeIcon">
        <select id="themeChoice" @change="changeTheme" v-model="nextTheme">
          <option value="default">默认主题</option>
          <option value="monotone">黑白主题</option>
        </select>
      </div>
    </nav>
    <div id="underNav">
    </div>
    <div id="appRouterView">
      <router-view />
    </div>
    <footer class="default">
      <div id="footerBox">
        <p id="footerWords"> 本网站仅为大作业使用，并无任何商业用途！ </p>
        <div class="footerInfo">
          <img id="emailIcon" name="emailIcon.png" class="themeImage" alt="emailIcon">
          <p> 电子邮箱: yczddgj@126.com </p>
          <img id="phoneIcon" name="phoneIcon.png" class="themeImage" alt="phoneIcon">
          <p> 联络电话: +86-15611462910</p>
          <img id="linkIcon" name="linkIcon.png" class="themeImage" alt="linkIcon">
          <p> 友情链接: <a href="http://www.yczddgj.com">韵城之都网站</a> </p>
          <img id="teamIcon" name="teamIcon.png" class="themeImage" alt="teamIcon">
          <div id="teamAvatarBox">
            <p> 团队成员:</p>
            <img class="teamAvatar" src="./assets/avatar/gxy.png" title="郭心源" alt="avatar">
            <img class="teamAvatar" src="./assets/avatar/xyy.jpg" title="谢苑瑜" alt="avatar">
            <img class="teamAvatar" src="./assets/avatar/xrf.jpg" title="幸若凡" alt="avatar">
            <img class="teamAvatar" src="./assets/avatar/fjj.jpg" title="范骏捷" alt="avatar">
            <img class="teamAvatar" src="./assets/avatar/gyc.jpg" title="顾洋丞" alt="avatar">
            <img class="teamAvatar" src="./assets/avatar/wqj.jpg" title="王麒杰" alt="avatar">
          </div>
        </div>
        <a href="https://git.tsinghua.edu.cn/xy-guo20/ml-model-manage-system">
          <img id="gitIcon" src="./assets/gitIcon.png" alt="gitIcon">
        </a>
      </div>
    </footer>
    <img v-bind:src="require('./assets/theme/' + this.curTheme + '/robotPic.png')" alt="" id="backGroundRobotPic">
  </div>
</template>

<script>
import changeAllImgUrl from '@/getThemeImg';

export default {
  data() {
    return {
      curTheme: 'default',
      nextTheme: '',
    };
  },
  methods: {
    changeTheme(event) {
      const doc = document.getElementsByTagName('html')[0];
      doc.setAttribute('data-theme', this.nextTheme);
      this.curTheme = this.nextTheme;
      if (this.$cookies.isKey('theme')) {
        this.$cookies.remove('theme');
      }
      this.$cookies.config('1m');
      this.$cookies.set('theme', this.curTheme);
      this.changeFooterpic();
      this.$router.go(0);
    },
    changeFooterpic() {
      const myFooter = document.getElementsByTagName('footer')[0];
      myFooter.classList = [this.curTheme];
    },
  },
  mounted() {
    if (this.$cookies.isKey('theme')) {
      this.curTheme = this.$cookies.get('theme');
      this.nextTheme = this.curTheme;
      const doc = document.getElementsByTagName('html')[0];
      doc.setAttribute('data-theme', this.nextTheme);
      this.changeFooterpic();
    }
    changeAllImgUrl();
  },
};
</script>

<style>
#backGroundRobotPic {
  position: fixed;
  z-index: -50;
  opacity: 0.1;
  top: 100px;
  right: 10px;
  width: 60%;
}

#logoImg {
  height: 75%;
  margin-left: 10px;
}

nav {
  height: 65px;
  display: flex;
  align-items: center;
  position: fixed;
  width: 100%;
  left: 0;
  top: 0;
  z-index: 5201314;
}

#underNav {
  display: block;
  height: 65px;
}

#navTeamName {
  font-size: 30px;
  margin-left: 15px;
  font-weight: bolder;
  flex-grow: 1;
}

#homeIcon {
  height: 30px;
  margin-right: 5px;
}

#listIcon {
  margin-top: 2px;
  height: 27px;
  margin-right: 6px;
}

#changeThemeIcon {
  margin-top: 2px;
  height: 26px;
  margin-right: 8px;
}

#themeChoice {
  width: 110px;
  height: 25px;
  font-size: 18px;
  margin-top: 2px;
}

.toOtherPageNav {
  display: flex;
  align-items: center;
  color: var(--navTextColor);
  margin-right: 25px;
  text-decoration: none;
}

footer {
  width: 100%;
  height: 350px;
  text-align: center;
  position: relative;
}

footer.default {
  background: url('./assets/theme/default/footer.png');
}

footer.monotone {
  background: url('./assets/theme/monotone/footer.png');
}

#appRouterView {
  flex: 1;
}

#appBox {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

#footerBox {
  margin-top: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 16px;
}

#app {
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
}

.footerInfo {
  display: grid;
  align-items: center;
  grid-template-columns: 50px 380px;
  grid-template-rows: 40px 40px 40px 40px;
}

.footerInfo p {
  margin-left: 20px;
  text-align: left;
}

#emailIcon {
  width: 28px;
}

#phoneIcon {
  width: 28px;
}

#teamIcon {
  width: 33px;
}

#linkIcon {
  width: 30px;
}

#footerWords {
  font-weight: bolder;
}

.teamAvatar {
  width: 35px;
  border-radius: 7px;
  margin: 5px;
}

#teamAvatarBox {
  display: flex;
  align-items: center;
}

#gitIcon {
  width: 30px;
  position: absolute;
  bottom: 15px;
  right: 15px;
}
</style>
