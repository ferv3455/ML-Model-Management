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
        <p> info info info </p>
        <p> email: xxxxxxx </p>
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
  margin-top: 200px;
}

#app {
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
}
</style>
