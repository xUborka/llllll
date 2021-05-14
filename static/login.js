// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
var firebaseConfig = {
    apiKey: "AIzaSyDPp4HNa7z2McPRualRwH8Zj-qtOGZc1Mg",
    authDomain: "llllll-project.firebaseapp.com",
    projectId: "llllll-project",
    storageBucket: "llllll-project.appspot.com",
    messagingSenderId: "401553182035",
    appId: "1:401553182035:web:0dbf6f271372664fa5a5a6",
    measurementId: "G-LZFGW1FB4G"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();

$(document).ready(function(){
    $('#Logout').click(function(){
        firebase.auth().signOut().then(() => {
            window.location.assign('/logout');
          });
    });

    $('#Anon').click(function(){
        console.log("Anon Clicked");
        firebase.auth().signInAnonymously().then(user => {
            return user.user.getIdToken().then(idToken => {
                return $.ajax('/create_anon_user', {data: {"idToken": idToken}, type: "POST"});
            }).then(() => {
                window.location.assign('/auth_needed');
            });
              
        });
    });

    $('#Login').click(function(){
        var user = $("#exampleInputEmail1").val();
        var pw = $("#exampleInputPassword1").val();
        firebase.auth().signInWithEmailAndPassword(user, pw).then(user => {
            console.log(user);
            return user.user.getIdToken().then(idToken => {
                return $.ajax('/create_anon_user', {data: {"idToken": idToken}, type: "POST"});
            }).then(() => {
                window.location.assign('/auth_needed');
            });
              
        });
    });

});