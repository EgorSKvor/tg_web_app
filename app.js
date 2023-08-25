let tg = window.Telegram.WebApp;

tg.expand();

let order = document.getElementById("order");

order.addEventListener("click", function () {
  let fio = document.getElementById("fio").value;
  let city = document.getElementById("city").value;
  let time = document.getElementById("time").value;
  let data = {
    fio: fio,
    city: city,
    time: time,
  };
  tg.sendData(JSON.stringify(data));
  tg.close();
});
