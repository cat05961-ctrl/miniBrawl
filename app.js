const firebaseConfig = {
  apiKey: "AIzaSyDY_GF8Adf1WyTyX91dVSGXRisxvxDyEWc",
  authDomain: "minibrawl-478a3.firebaseapp.com",
  databaseURL: "https://minibrawl-478a3-default-rtdb.firebaseio.com/",
  projectId: "minibrawl-478a3"
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();
const db = firebase.database();

// регистрация
function register() {
    let email = document.getElementById("email").value;
    let pass = document.getElementById("pass").value;

    auth.createUserWithEmailAndPassword(email, pass)
    .then(() => alert("Регистрация ок"))
    .catch(e => alert(e.message));
}

// вход
function login() {
    let email = document.getElementById("email").value;
    let pass = document.getElementById("pass").value;

    auth.signInWithEmailAndPassword(email, pass)
    .then(() => window.location.href = "app.html")
    .catch(e => alert(e.message));
}

// добавить игру
function addGame() {
    let name = document.getElementById("gameName").value;

    if(name === "") return alert("Введите название");

    db.ref("games").push({
        name: name
    });
}

// загрузка игр
if (document.getElementById("list")) {
    db.ref("games").on("child_added", function(snapshot){
        let game = snapshot.val();

        let div = document.createElement("div");
        div.className = "game";
        div.innerText = game.name;

        document.getElementById("list").appendChild(div);
    });
}