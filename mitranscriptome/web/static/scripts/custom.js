function toggle_visibility(id) {
   var e = document.getElementById(id);
 if(e.style.display == 'block')
    e.style.display = 'none';
 else
    e.style.display = 'block';
}

function toggle_off(id) {
   var e = document.getElementById(id);
       e.style.display = 'none';
}

function toggle_on(id) {
   var e = document.getElementById(id);
       e.style.display = 'block';
}