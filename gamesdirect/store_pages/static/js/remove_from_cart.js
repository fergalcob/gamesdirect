$(document).on("click","#remove-from-cart",function(){let e=Cookies.get("csrftoken"),t=$(this).attr("data-product-id"),d=$(this).attr("data-product-platform");console.log(t),$.ajax({url:"remove_from_cart",method:"POST",headers:{"X-CSRFToken":e},mode:"same-origin",data:{item_id:t,platform:d},success:function(e){$("#side-cart-dynamic").load(location.href+" #side-cart-dynamic")}})});