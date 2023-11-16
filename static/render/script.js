function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  function fetchUser(user_id){
    return fetch(
        '/api/user/'+user_id+'/',
        {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                "user-id": user_id
            },
        }

    )
    .then(response => {
        if (response.status === 200) { // Kontrola, zda je status 201 Created
            return response.json();
        }
        throw new Error('Network response was not ok');
    })
    .then(data => {
        return data
    })
}

function fetchUsername(user_id, input){
  fetch("/api/user/", {
    method: 'GET',
    headers: {
        "Content-Type": "application/json",
        "user-id": user_id
    }
})
.then(response => {
    if (response.status === 200) { // Kontrola, zda je status 201 Created
        return response.json();
    }
    alert('Network response was not ok');
    throw new Error('Network response was not ok');
})
.then(data => {
    // Zpracování odpovědi od serveru
    input.value = data["username"];
    console.log(data["username"]);
})
.catch(error => {
    // Zpracování chyby
    console.error('Chyba: ' + error);
});
}
  

function sendForm(data) {
    fetch("/api/register/", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "user-id": getCookie("user_id")
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.status === 201) { // Kontrola, zda je status 201 Created
            return response.json();
        }
        alert('Network response was not ok');
        throw new Error('Network response was not ok');
    })
    .then(data => {
        // Zpracování odpovědi od serveru
        console.log(data);
        alert('Proběhlo v pořádku');
    })
    .catch(error => {
        // Zpracování chyby
        console.error('Chyba: ' + error);
    });
}

function fetchAllFinishedRegistrations(){
    return fetch("/api/register/allFinished/", {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            "user-id": getCookie("user_id")
        }
    })
    .then(response => {
        if (response.status === 200) { // Kontrola, zda je status 201 Created
            return response.json();
        }
        alert('Network response was not ok');
        throw new Error('Network response was not ok');
    })
}