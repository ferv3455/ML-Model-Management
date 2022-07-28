export default function getBackUrl(str) {
  let IP = 'http://localhost:5000';
  console.log(window.location.host);
  if (window.location.host !== 'localhost:8080') {
    IP = 'http://59.110.25.36:5000';
  }
  return IP + str;
}
