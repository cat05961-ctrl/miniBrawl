const firebaseConfig = {
  apiKey: "AIzaSyDY_GF8Adf1WyTyX91dVSGXRisxvxDyEWc",
  authDomain: "minibrawl-478a3.firebaseapp.com",
  databaseURL: "https://minibrawl-478a3-default-rtdb.firebaseio.com/",
  projectId: "minibrawl-478a3",
  storageBucket: "minibrawl-478a3.appspot.com"
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();
const db = firebase.database();
const storage = firebase.storage();

// регистрация
function register() {
    auth.createUserWithEmailAndPassword(get("email"), get("pass"))
    .then(() => location.href = "app.html")
    .catch(e => alert(e.message));
}

// вход
function login() {
    auth.signInWithEmailAndPassword(get("email"), get("pass"))
    .then(() => location.href = "app.html")
    .catch(e => alert(e.message));
}

// загрузка APK
function uploadGame() {
    let name = get("gameName");
    let file = document.getElementById("file").files[0];

    if (!file) return alert("Выбери файл");

    let ref = storage.ref("games/" + file.name);

    ref.put(file).then(() => {
        ref.getDownloadURL().then(url => {

            db.ref("games").push({
                name: name,
                file: url
            });

            alert("Игра загружена 🚀");
        });
    });
}

// вывод игр
if (document.getElementById("list")) {
    db.ref("games").on("child_added", snap => {
        let game = snap.val();

        let div = document.createElement("div");
        div.className = "msg";

        div.innerHTML = `
            <b>${game.name}</b><br>
            <a href="${game.file}" target="_blank">📥 Скачать</a>
        `;

        list.appendChild(div);
    });
}

// чат
function sendMsg() {
    let msg = get("msg");
    db.ref("chat").push({ msg });
}

if (document.getElementById("chat")) {
    db.ref("chat").on("child_added", snap => {
        let div = document.createElement("div");
        div.className = "msg";
        div.innerText = snap.val().msg;
        chat.appendChild(div);
    });
}

// профиль
function saveProfile() {
    let user = auth.currentUser;
    db.ref("users/" + user.uid).set({
        name: get("name")
    });
}

// выход
function logout() {
    auth.signOut().then(() => location.href = "index.html");
}

function get(id) {
    return document.getElementById(id).value;
}