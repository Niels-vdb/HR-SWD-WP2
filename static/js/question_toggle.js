const switch1 = document.querySelector("#switch-1");
const switch2 = document.querySelector("#switch-2");
const switch3 = document.querySelector("#switch-3");

const sysCodes = document.getElementById("edit-sys-code-screen");
const leerdoel = document.getElementById("edit-leerdoel-screen");
const authors = document.getElementById("edit-author-screen");

switch1.addEventListener("click", () => {
sysCodes.style.display = "";
authors.style.display = "none";
leerdoel.style.display = "none";
});
switch2.addEventListener("click", () => {
leerdoel.style.display = "";
sysCodes.style.display = "none";
authors.style.display = "none";
});
switch3.addEventListener("click", () => {
authors.style.display = "";
leerdoel.style.display = "none";
sysCodes.style.display = "none";
});