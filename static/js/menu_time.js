const today = new Date();
const time = today.getHours();
const greeting = document.getElementById("greeting").innerHTML;

console.log(time);
if (time > 6 && time < 12) {
document
    .getElementById("greeting")
    .insertAdjacentHTML("afterbegin", "Goedemorgen ");
}
if (time >= 12 && time < 18) {
document
    .getElementById("greeting")
    .insertAdjacentHTML("afterbegin", "Goedemiddag ");
}
if (time >= 18 && time < 24) {
document
    .getElementById("greeting")
    .insertAdjacentHTML("afterbegin", "Goedenavond ");
}