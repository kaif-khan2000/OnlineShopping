function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function signIn(){
    var token = getCookie('csrftoken');
   
    email = document.getElementById("loginEmail").value;
    password = document.getElementById("loginPassword").value;
    message = document.getElementById('message');
    if(email == "" || password == "") {
        message.innerHTML = "Fill credentials Properly!"
        return;
    }
    $.ajax({
        headers:{'X-CSRFToken':token},
        type:"POST",
        url:"/login",
        data:{
            'email':email,
            'password':password
        },
        success:function(response){
            if(response.status == 'success'){
                location.reload();
            }
            else{
               
                message.innerHTML = "Invalid Credentials!";
                password.value = "";
            }
        },
    })
}

function logout(){
    $.ajax({
        type:"GET",
        url:"/logout",
        data:{},
        success:function(response){
            location.reload();
        }
    })
}

function register(){
    var token = getCookie('csrftoken');
    username = document.getElementById('username').value
    email = document.getElementById('email').value
    address = document.getElementById('address').value
    password = document.getElementById('password').value
    confirmPassword = document.getElementById('confirmPassword').value
    message = document.getElementById('message')
    if(username == "" || email == "" || address=="" || password=="" || confirmPassword==""){
        message.innerHTML = "Looks like some fields are empty!";
        return;
    }
    if (!(/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(email)))
    {
        message.innerHTML = "email not in correct format"
        return;
    }
    if(password.length < 5){
        message.innerHTML = "Sorry! Your password is too short to be considered"
        return;
    }
    if (password != confirmPassword){
        message.innerHTML = "passwords do not match";
        return;
    }
    
    $.ajax({
        headers:{'X-CSRFToken':token},
        type:"POST",
        url: '/register',
        data: {
            'email':email,
            'username':username,
            'password':password,
            'address':address,
        },
        success:function(response){
            smessage = document.getElementById('smessage');
            smessage.innerHTML = "Registerd successfully. Please login"
        }
    })
}

var suggestions = document.getElementById("suggestions") 
  $('#searchbar').on('input paste',function(e){
    console.log($('#searchbar').value);
    e.preventDefault();
    $.ajax({
      type:"GET",
      url:"/searchRecommendations",
      data:{
        "search" : $('#searchbar').val(),
      },
      success: function(response){
        suggestions.innerHTML = "";
        for(i=0;i<response.length;i++){
          console.log(response[0])
          if(response[i].fields.name!="")
            suggestions.innerHTML += "<option><h2>"+response[i].fields.brand+"("+response[i].fields.name+")</h2><option>";
        }
      }
    });
  });