var API_URL = 'https://api.demoblaze.com';
var HLS_URL = '';
var token = '';
$(document).ready(function () {
  $.getJSON("config.json", function (data) {
    if (data.API_URL) API_URL = data.API_URL
    if (data.HLS_URL) HLS_URL = data.HLS_URL

    var token = getCookie("tokenp_");
    if (token.length > 0) {
      $.ajax({
        type: 'POST',
        url: API_URL + '/check',
        data: JSON.stringify({ "token": token }),
        contentType: "application/json",
        success: function (data) {
          if (data.errorMessage == "Token has expired") {
            alert("Your token has expired, please login again.");
          } else if (data.errorMessage == "Bad parameter, token malformed.") {
            alert("Bad parameter, token malformed.");
          } else if (data.errorMessage == "Bad parameter, flag is incorrect.") {
            alert("Bad parameter, flag is incorrect.");
          } else {
            document.getElementById("signin2").style.display = 'none';
            document.getElementById("login2").style.display = 'none';
            document.getElementById("nameofuser").text = "Welcome " + data.Item.username;
            document.getElementById('nameofuser').style.display = 'block';
            document.getElementById('logout2').style.display = 'block';
          }
        }
      });
    } else {
      document.getElementById("signin2").style.display = 'block';
      document.getElementById("login2").style.display = 'block';
    }

    var loc = document.location.href;
    var getString = loc.split('?')[1];
    var GET = getString.split('&');
    var get = {};

    for (var i = 0, l = GET.length; i < l; i++) {
      var tmp = GET[i].split('p_=');
      get[tmp[0]] = unescape(decodeURI(tmp[1]));
    }
    var idp = get['id'];
    idp = idp.replace(/#/g, '');
    $.ajax({
      type: 'POST',
      url: API_URL + '/view',
      data: JSON.stringify({ "id": idp }),
      contentType: "application/json",

      success: function (data) {
        // $('#tbodyid').empty();
        var valew = JSON.parse(JSON.stringify(data));
        $('#tbodyid').append('<h2 class="name">' + valew["title"] + '</h2>' + '<hr>' + '<h3 class="price-container">' + '$' + valew['price'] + '<small>' + ' *includes tax' + '</small>' + '</h3>' + '<hr>' + '<div class="description description-tabs">' + '<ul id="myTab" class="nav nav-pills">' + '<li class="active">' + '</li>' + '</ul>' + '<div id="myTabContent" class="tab-content">' + '<div class="tab-pane fade active in" id="more-information">' + '<br>' + '<strong>' + 'Product description' + '</strong>' + '<p>' + valew['desc'] + '</div>' + '</div>' + '</div>' + '<hr>' + '<div class="row">' + '<div class="col-sm-12 col-md-6 col-lg-6">' + '<a href="#" onclick="addToCart(' + valew['id'] + ')" class="btn btn-success btn-lg">' + 'Add to cart' + '</a>' + '</div>' + '</div>');
        $('#imgp').append('<div class="item active">' + '<img width=400 height=280 src="' + valew['img'] + '" alt="">' + '</div>');
      }
    });
    var player = window.player = videojs('example-video');
    var url = HLS_URL + "/index.m3u8";
    player.src({
      src: url,
      type: 'application/x-mpegURL'
    });
    $('#videoModal').on('hidden.bs.modal', function (e) {
      var player = window.player = videojs('example-video');
      player.pause();
    });
  })
});

function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') c = c.substring(1);
    if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
  }
  return "";
}

function showcart() {
  // location.href= 'prod.html?id=' + eid;
  // window.open('cart.html?tokenp_=' + token,'_blank');
}

function send() {
  document.getElementById("recipient-email").value = "";
  document.getElementById("recipient-name").value = "";
  document.getElementById("message-text").value = "";
  alert('Thanks for the message!!');
  $('#exampleModal').modal('hide');
  location.reload();
}

function logIn() {
  var pass = b64EncodeUnicode(document.getElementById("loginpassword").value);
  var username = document.getElementById("loginusername").value;
  if (pass == "" || username == "") {
    alert("Please fill out Username and Password.");
  } else {
    $.ajax({
      type: 'POST',
      url: API_URL + '/login',
      data: JSON.stringify({ "username": username, "password": pass }),
      contentType: "application/json",

      success: function (data) {
        if (data.errorMessage == "Wrong password.") {
          alert("Wrong password.");
        } else if (data.errorMessage == "User does not exist.") {
          alert("User does not exist.");
        } else {
          $('#logInModal').modal('hide');
          $('.modal-backdrop').hide();
          token = data.replace("Auth_token: ", "");
          document.cookie = "tokenp_=" + token;
          location.reload();
        }
      }
    });
  }
}

function logOut() {
  document.cookie = 'tokenp_' + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
  location.href = 'index.html';
}

function b64EncodeUnicode(str) {
  return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function (match, p1) {
    return String.fromCharCode('0x' + p1);
  }));
}

function register() {
  var pass = b64EncodeUnicode(document.getElementById("sign-password").value);
  var username = document.getElementById("sign-username").value;
  if (pass == "" || username == "") {
    alert("Please fill out Username and Password.");
  } else {
    $.ajax({
      type: 'POST',
      url: API_URL + '/signup',
      data: JSON.stringify({ "username": username, "password": pass }),
      contentType: "application/json",

      success: function (data) {
        if (data.errorMessage == "This user already exist.") {
          alert("This user already exist.");
        } else {
          $('#signInModal').modal('hide');
          $('.modal-backdrop').hide();
          alert("Sign up successful.");
        }
      }
    });
  }
}

function addToCart(idp) {
  var token = getCookie("tokenp_");
  if (token.length > 0) {
    $.ajax({
      type: 'POST',
      url: API_URL + '/addtocart',
      data: JSON.stringify({ "id": guid(), "cookie": token, "prod_id": idp, "flag": true }),
      contentType: "application/json",

      success: function (data) {
        if (data.errorMessage == "Token has expired") {
          alert("Your token has expired, please login again.");
        } else if (data.errorMessage == "Bad parameter, token malformed.") {
          alert("Bad parameter, token malformed.");
        } else if (data.errorMessage == "Bad parameter, flag is incorrect.") {
          alert("Bad parameter, flag is incorrect.");
        } else {
          alert("Product added.");
        }
      }
    });
  } else {
    $.ajax({
      type: 'POST',
      url: API_URL + '/addtocart',
      data: JSON.stringify({ "id": guid(), "cookie": document.cookie, "prod_id": idp, "flag": false }),
      contentType: "application/json",
      success: function (data) {
        alert("Product added");
      }
    });
  }
  return false;
}