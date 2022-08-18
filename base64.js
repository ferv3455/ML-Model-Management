function getBase64(file) {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
        console.log(reader.result);
    };
    reader.onerror = function (error) {
        console.log('Error: ', error);
    };
    return reader.result;
}

function func() {
    var file = document.getElementById('file').files[0];   // <input type='file'>
    var a = getBase64(file);
    console.log(a);
}