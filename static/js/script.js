
// logedIn = document. ;

// if loged in is false logg off schouln'd be visible
if (logedIn) { document.getElementById("logg_off").style.display("none"); }

// corrupt questions toggle
const switch1 = document.querySelector('#switch-1');
const switch2 = document.querySelector('#switch-2');
const switch3 = document.querySelector('#switch-3');

const sysCodes = document.getElementById('system-code-aanpas');
const leerdoel = document.getElementById('leerdoel-aanpas');
const authors = document.getElementById('author-aanpas');

leerdoel.style.display = '';
sysCodes.style.display = 'none';
authors.style.display = 'none';

switch1.addEventListener('click', () => {
    sysCodes.style.display = '';
    authors.style.display = 'none';
    leerdoel.style.display = 'none';
});
switch2.addEventListener('click', () => {
    leerdoel.style.display = '';
    sysCodes.style.display = 'none';
    authors.style.display = 'none';
});
switch3.addEventListener('click', () => {
    authors.style.display = '';
    leerdoel.style.display = 'none';
    sysCodes.style.display = 'none';
});