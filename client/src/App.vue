<template>
  <nav>
    <img id="logoImg" src="./assets/s02big.png" alt="logo">
    <p id="navTeamName">TeAM</p>
    <router-link id="toHomeNav" to="/">
      <img id="homeIcon" src="./assets/homeIcon.png" alt="homeIcon">
      <p>主页</p>
    </router-link>
  </nav>
  <router-view />
</template>

<style>
#logoImg {
  height: 75%;

  margin-left: 10px;
}

nav {
  margin: -10px;
  height: 65px;
  display: flex;
  align-items: center;
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
}

#toHomeNav {
  display: flex;
  align-items: center;
  color: var(--navTextColor);
  margin-right: 20px;
}
</style>
