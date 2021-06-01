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
    var line_nuber = 1;
    $('#Logout').click(function(){
        firebase.auth().signOut().then(() => {
            window.location.assign('/logout');
        });
    });

    function returnData(param) {
        console.log(param);
        var res = '';
        if (param['rc'] == 0){
            res = "<p class=\"text-white\"><b> > " + line_nuber.toString() + " : </b>" + param['stdout'].replace(/\n/g, '<br>') + '</p>';
        } else {
            res = "<p class=\"text-danger\"><b> > " + line_nuber.toString() + " : </b>" + param['stderr'] + '</p>';
        }
        var value = res.concat($('#console').html())
        $('#console').html(value);
        line_nuber += 1;
    }

    $('#SubmitButton').click(function(){
        document.getElementById("SubmitButton").disabled = true;
        document.getElementById("SubmitLoading").hidden = false;
        document.getElementById("SubmitText").hidden = true;
        setTimeout(function(){
            document.getElementById("SubmitButton").disabled = false;
            document.getElementById("SubmitLoading").hidden = true;
            document.getElementById("SubmitText").hidden = false;
        },2000);
        var editor_ref = ace.edit("editor");
        return $.post('/submit', {"code": editor_ref.getValue()}, function(data){
            data = JSON.parse(data);
            console.log(data);
            returnData(data);
        });
    });

    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/dracula");
    editor.session.setMode("ace/mode/python");
    document.getElementById('editor').style.fontSize='16px';
});