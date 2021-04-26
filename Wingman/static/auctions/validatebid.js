function validate_bid(bid_value, initial) {
         //document.getElementById("demo").innerHTML = "Welcome " + bid_value ;
         //alert("bid_value");
   var new_value = document.forms["form_bid"]["new_bid"].value;
   if( initial ){
        if( new_value < bid_value  ){
            alert("not lower than RMB "+ bid_value);
                return false;
            }
   }
   else {
        if( new_value <= bid_value  ){
            alert("not lower than RMB "+ bid_value);
                return false;
            }
   }
   
   return true;

 }