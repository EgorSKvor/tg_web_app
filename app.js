let tg = window.Telegram.WebApp;

tg.expand();

let order = document.getElementById("order");

order.addEventListener("click", function () {
  let fio = document.getElementById("fio").value;
  let napr = document.getElementById("napr").value;
  let whyYou = document.getElementById("whyYou").value;
  let age = document.getElementById("age").value;
  let data = {
    fio: fio,
    napr: napr,
    whyYou: whyYou,
    age: age,
  };
  tg.sendData(JSON.stringify(data));
  tg.close();
});
