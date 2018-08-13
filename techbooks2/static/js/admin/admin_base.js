var open_menu = function(obj){
  let target = obj.parentElement.classList
  if(target.contains("open")){
    target.remove("open")
  }
  else{
    target.add("open");
  }
}
