var a = document.getElementsByClassName('_51mw _51m- vMid');
var i=0;
var x = setInterval(function(){
	if(i>=a.length){
		clearInterval(x)
	}
	else{
		a[i].click();
		i++;
	}

}, 100);