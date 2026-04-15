import { auth, db } from "./firebase.js";
import {
createUserWithEmailAndPassword,
signInWithEmailAndPassword
} from "https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js";

import {
ref,
set
} from "https://www.gstatic.com/firebasejs/9.22.2/firebase-database.js";

window.register = async function () {
    let email = emailInput();
    let pass = passInput();
    let nick = document.getElementById("nick").value;

    let user = await createUserWithEmailAndPassword(auth, email, pass);

    await set(ref(db, "users/" + user.user.uid), {
        nickname: nick
    });

    location.href = "chat.html";
};

window.login = async function () {
    let email = emailInput();
    let pass = passInput();

    await signInWithEmailAndPassword(auth, email, pass);

    location.href = "chat.html";
};

function emailInput(){return document.getElementById("email").value;}
function passInput(){return document.getElementById("pass").value;}