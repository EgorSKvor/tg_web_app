let tg = window.Telegram.WebApp;

tg.expand();

let order = document.getElementById("order");

order.addEventListener("click", function () {
  let fio = document.getElementById("fio").value;
  let napr = document.getElementById("napr").value;
  let time = document.getElementById("time").value;
  let age = document.getElementById("age").value;
  let data = {
    fio: fio,
    napr: napr,
    time: time,
    age: age,
  };
  tg.sendData(JSON.stringify(data));
  tg.close();
});
