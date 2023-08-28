$(document).on("click", "#remove-from-cart", function() {
        const csrftoken = Cookies.get('csrftoken');
        let cart_item = $(this).attr("data-product-id");
        console.log(cart_item)
        $.ajax({
            url: 'remove_from_cart',
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            data: {
                'cart_item_id': cart_item,
            },
            success: function (response) {
                $('#side-cart-dynamic').load(location.href + " #side-cart-dynamic");
            },
        });
    });
