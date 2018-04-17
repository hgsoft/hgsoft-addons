function addQtyList() {
    var p_name = $(".p_name");
    
    p_name_list = "";
    
    for(var i = 0; i < p_name.length; i++){
        p_name_list += "#" + $(p_name[i]).val();
    }
    
    var p_qty = $(".p_qty");
    
    p_qty_list = "";
    
    for(var i = 0; i < p_qty.length; i++){
        p_qty_list += "#" + $(p_qty[i]).val();
    }
    
    var value = document.getElementById("product_id").value;

    var inputs_color = $(".color").length;
    
    var inputs_size = $(".size").length;
    
    var inputs_qty = $(".add_qty_list");
    
    var full_list = "";
    
    var final_value;
    
    for(var i = 0; i < inputs_qty.length; i++){
        full_list += "#" + $(inputs_qty[i]).val();
    }
    
    //final_value = value + "|" + full_list;
 
    final_value = p_name_list + "|" + p_qty_list;
 
    document.getElementById("product_id").value = final_value + "|" + inputs_color + "|" + inputs_size;

}