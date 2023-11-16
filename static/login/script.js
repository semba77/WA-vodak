function switch_function() {
    var x = document.getElementById("password_input");
    var text = document.getElementById("switch_paragraph")
    if (x.type === "password") {
      x.type = "text";
      text.textContent="   skrýt heslo";
    } else {
      x.type = "password";
      text.textContent="zobrazit heslo";
    }
  }

function close_button(){
  document.getElementById("error_div").remove();
}