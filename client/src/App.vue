<template>
  <div id="appBox">
    <nav>
      <img id="logoImg" src="./assets/s02big.png" alt="logo">
      <p id="navTeamName">TeAM</p>
      <router-link id="toHomeNav" to="/">
        <img id="homeIcon" src="./assets/homeIcon.png" alt="homeIcon">
        <p>主页</p>
      </router-link>
    </nav>
    <div id="underNav">
    </div>
    <div id="appRouterView">
      <router-view />
    </div>
    <footer>
      <div id="footerBox">
        <p id="footerWords"> 本网站仅为大作业使用，并无任何商业用途！ </p>
        <div class="footerInfo">
          <img id="emailIcon" src="./assets/emailIcon.png" alt="emailIcon">
          <p> 电子邮箱: yczddgj@126.com </p>
          <img id="phoneIcon" src="./assets/phoneIcon.png" alt="phoneIcon">
          <p> 联络电话: +86-15611462910</p>
          <img id="teamIcon" src="./assets/teamIcon.png" alt="teamIcon">
          <div id="teamAvatarBox">
            <p> 团队成员:</p>
            <img class="teamAvatar" src="./assets/avatar/gxy.png" alt="avatar">
            <img class="teamAvatar" src="./assets/avatar/xyy.jpg" alt="avatar">
          </div>
          <img id="linkIcon" src="./assets/linkIcon.png" alt="linkIcon">
          <p> 友情链接: <a href="http://www.yczddgj.com">韵城之都网站</a> </p>
        </div>
        <a href="https://git.tsinghua.edu.cn/xy-guo20/ml-model-manage-system">
          <img id="gitIcon" src="./assets/gitIcon.png" alt="gitIcon">
        </a>
      </div>
    </footer>
  </div>
</template>

<style>
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
  font-family: 'Courier New', Courier, monospace;
}

#homeIcon {
  height: 30px;
  margin-right: 5px;
}

#toHomeNav {
  display: flex;
  align-items: center;
  color: var(--navTextColor);
  margin-right: 20px;
  text-decoration: none;
}

footer {
  width: 100%;
  height: 350px;
  background: url('./assets/footer.png');
  text-align: center;
  position: relative;
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
  grid-template-columns: 50px 300px;
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
  width: 40px;
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
