// 🔥 Firebase подключение (РАБОТАЕТ НА САЙТЕ)

import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";

import { getAuth } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js";

import { getDatabase } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-database.js";

import { getStorage } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-storage.js";

const firebaseConfig = {
  apiKey: "AIzaSyDY_GF8Adf1WyTyX91dVSGXRisxvxDyEWc",
  authDomain: "minibrawl-478a3.firebaseapp.com",
  databaseURL: "https://minibrawl-478a3-default-rtdb.firebaseio.com/",
  projectId: "minibrawl-478a3",
  storageBucket: "minibrawl-478a3.appspot.com",
  messagingSenderId: "690621895511",
  appId: "1:690621895511:web:843a615bb87e1e22226412"
};

const app = initializeApp(firebaseConfig);

// экспорт
export const auth = getAuth(app);
export const db = getDatabase(app);
export const storage = getStorage(app);