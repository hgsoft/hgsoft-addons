function addQtyList() {
    var value = document.getElementById("product_id").value;

    var inputs_qty = $(".add_qty_list");
    
    var full_list = "";
    
    var final_value;
    
    for(var i = 0; i < inputs_qty.length; i++){
        full_list += "#" + $(inputs_qty[i]).val();
    }
    
    final_value = value + "|" + full_list;
    
    document.getElementById("product_id").value = final_value;

    alert("Valor final: " + final_value)
}