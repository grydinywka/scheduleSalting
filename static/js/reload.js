function reloadPage() {
    window.setTimeout(function(){ document.location.reload(true); }, 60000);
}

$(document).ready(function(){
    reloadPage();
});
