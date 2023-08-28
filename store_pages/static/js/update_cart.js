$(document).on("click", "#increment-quantity", function() {
    const csrftoken = Cookies.get('csrftoken');
    let cart_item = $(this).prev();
    let item_quantity = parseInt(cart_item.attr('data-quantity')) + 1;
    let item_id = cart_item.attr('data-product-id')
    console.log(item_quantity);
    $.ajax({
        url: 'update_cart',
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: {
            'cart_item_id': item_id,
            'item_quantity': item_quantity,
        },
        success: function (response) {
            $('#side-cart-dynamic').load(location.href + " #side-cart-dynamic");
        },
    });
});

$(document).on("click", "#decrement-quantity", function() {
    const csrftoken = Cookies.get('csrftoken');
    let cart_item = $(this).next();
    let item_quantity = parseInt(cart_item.attr('data-quantity')) - 1;
    let item_id = cart_item.attr('data-product-id')
    console.log(item_quantity);
    $.ajax({
        url: 'update_cart',
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: {
            'cart_item_id': item_id,
            'item_quantity': item_quantity,
        },
        success: function (response) {
            $('#side-cart-dynamic').load(location.href + " #side-cart-dynamic");
        },
    });
});