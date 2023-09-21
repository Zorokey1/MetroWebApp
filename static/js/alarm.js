xhr = new XMLHttpRequest();
xhr.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
        window.location.replace("http://127.0.0.1:8000/finished/");
    }
};

xhr.open("GET", "http://127.0.0.1:8000/alarm/json");
xhr.send();