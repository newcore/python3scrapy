try{
  window.onerror = function(){return true;}
}
catch(err){}
function is_mobile() {
    var userAgentInfo = navigator.userAgent;
    var Agents = ["Android", "iPhone",
                "SymbianOS", "Windows Phone",
                "iPad", "iPod"];
    var flag = false;
    for (var v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) > 0) {
            flag = true;
            break;
        }
    }
    return flag;
}
function gotomurl(url) {
	if(is_mobile()){
		window.location.href=url;
	}
}

$(document).ready(function(){
  var winW = $(window).width();
 
  if(winW<1000){
	 
  }else if(winW<1100){

  }

});

function subck(){
	var q = document.getElementById("kw").value;
	if(q=='' || q==''){return false;}else{return true;}
}

$(document).ready(function() {
	var WinH = $(window).height();
    var offset = $('#footer').offset(); 
	if(WinH>offset.top+$('#footer').height()){
		var MH = WinH-offset.top-$('#footer').height()+20;
		$('#footer').css("margin-top",MH.toString()+"px");
	
	}
    $('#footer').css("visibility","visible");
});

function toptab(obj,id){
	$(".hothead a").removeClass("current");
	$("#tab"+id).addClass("current");
    $(".hotsearch ul").hide();
	$("#toplist"+id).show();
}