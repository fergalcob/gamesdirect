$(document).on("click","#increment-quantity",function(){let t=Cookies.get("csrftoken"),a=$(this).prev(),e=parseInt(a.attr("data-quantity"))+1,i=a.attr("data-product-id");console.log(e),$.ajax({url:"update_cart",method:"POST",headers:{"X-CSRFToken":t},mode:"same-origin",data:{cart_item_id:i,item_quantity:e},success:function(t){$("#side-cart-dynamic").load(location.href+" #side-cart-dynamic")}})}),$(document).on("click","#decrement-quantity",function(){let t=Cookies.get("csrftoken"),a=$(this).next(),e=parseInt(a.attr("data-quantity"))-1,i=a.attr("data-product-id");console.log(e),$.ajax({url:"update_cart",method:"POST",headers:{"X-CSRFToken":t},mode:"same-origin",data:{cart_item_id:i,item_quantity:e},success:function(t){$("#side-cart-dynamic").load(location.href+" #side-cart-dynamic")}})});