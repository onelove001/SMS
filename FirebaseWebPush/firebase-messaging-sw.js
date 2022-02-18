importScrpts("http://www.gstatic.com/firebasejs/7.14.6/firebase-app.js")
importScrpts("http://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js")


const firebaseConfig = {
    apiKey: "AIzaSyAhgb230zeWwq77fHdWBKfuYoHbSkBznJg",
    authDomain: "studentmanagementsystem234.firebaseapp.com",
    projectId: "studentmanagementsystem234",
    storageBucket: "studentmanagementsystem234.appspot.com",
    messagingSenderId: "391301702726",
    appId: "1:391301702726:web:56d1b13d6fc0cb923ad647",
    measurementId: "G-RPND0CW791"
};
firebase.initializeApp(firebaseConfig)

const messaging = firebase.messaging()

messaging.setBackgroundMessageHandler(function(payload){
	console.log(payload)
})