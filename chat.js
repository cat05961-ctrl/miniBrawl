import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import { getDatabase, ref, push, onValue } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-database.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js";

// 🔥 ТВОЙ CONFIG (НЕ МЕНЯЙ)
const firebaseConfig = {
  apiKey: "AIzaSyDY_GF8Adf1WyTyX91dVSGXRisxvxDyEWc",
  authDomain: "minibrawl-478a3.firebaseapp.com",
  databaseURL: "https://minibrawl-478a3-default-rtdb.firebaseio.com/",
  projectId: "minibrawl-478a3",
  storageBucket: "minibrawl-478a3.firebasestorage.app",
  messagingSenderId: "690621895511",
  appId: "1:690621895511:web:843a615bb87e1e22226412"
};

// 🔥 INIT
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const auth = getAuth(app);

let username = "Без имени";

// 🔥 получаем пользователя
onAuthStateChanged(auth, (user) => {
  if (user) {
    username = user.email; // можно потом заменить на ник
  }
});

// 🔥 отправка
window.send = function () {
  const input = document.getElementById("msg");
  const text = input.value;

  if (text === "") return;

  push(ref(db, "chat"), {
    user: username,
    msg: text
  });

  input.value = "";
};

// 🔥 загрузка сообщений
onValue(ref(db, "chat"), (snapshot) => {
  const chat = document.getElementById("chat");
  chat.innerHTML = "";

  snapshot.forEach((child) => {
    const data = child.val();

    chat.innerHTML += `
      <div class="msg">
        <b>${data.user || "Без имени"}</b><br>
        ${data.msg || "..."}
      </div>
    `;
  });
});