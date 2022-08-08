function getThemeImgUrl(str) {
  const doc = document.getElementsByTagName('html')[0];
  const curTheme = doc.getAttribute('data-theme');
  return require(`./assets/theme/${curTheme}/${str}`);
}

export default function changeAllImgUrl() {
  const allPic = document.getElementsByTagName('img');
  for (let i = 0; i < allPic.length; i += 1) {
    if (allPic[i].classList.contains('themeImage')) {
      const picName = allPic[i].getAttribute('name');
      allPic[i].src = getThemeImgUrl(picName);
    }
  }
}
