function _post(api) {
  var form = document.createElement("form");
  var input = document.createElement("input");

  document.body.appendChild(form);

  input.setAttribute("type", "submit");
  form.appendChild(input);
  form.setAttribute("action", "/api/" + api);
  form.setAttribute("method", "post");
  form.setAttribute("onsubmit", "return false;");
  form.submit();
}

function post(api) {
  $.post('/api/' + api, {}, function(serverResponse){console.log(serverResponse)}, "json")
}

function pushPowerButton(range) {
  var msg = "";
  var api = "";

  if (range == "long") {
    msg += "Forcely";
    api = "fcpwoff";
  } else {
    msg += "Normaly";
    api = "pwoff";
  }
  msg += " power off.",

  swal({
    title:msg,
    type:"warning",
    text:"Are you OK？",
    confirmButtonText:"Yes, of course.",
    cancelButtonText:"No!",
    showConfirmButton:true,
    showCancelButton:true,
    closeOnConfirm:false,
    closeOnCancel:false
  },
  function(isConfirm){
    if(isConfirm){
      post(api)
      swal("Done!", "Check the status of power.", "success");
    }else{
      swal("Do nothing.", "See you!", "error");
    }
  });
}
