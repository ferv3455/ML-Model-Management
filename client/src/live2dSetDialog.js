let previousSetTimeout = -1;

export default function setDialog(str, time) {
  if (previousSetTimeout !== -1) {
    clearTimeout(previousSetTimeout);
  }

  const target = document.getElementsByClassName('live2d-widget-dialog')[0];
  target.innerHTML = str;

  previousSetTimeout = setTimeout(() => {
    target.innerHTML = '';
    previousSetTimeout = -1;
  }, time);
}
