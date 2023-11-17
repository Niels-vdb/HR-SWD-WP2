const switch4 = document.querySelector("#switch-4");
const switch5 = document.querySelector("#switch-5");

const employee = document.getElementById("employee-screen");
const birthYear = document.getElementById("birth-year-screen");

switch4.addEventListener("click", () => {
  birthYear.style.display = "";
  employee.style.display = "none";
});
switch5.addEventListener("click", () => {
  birthYear.style.display = "none";
  employee.style.display = "";
});