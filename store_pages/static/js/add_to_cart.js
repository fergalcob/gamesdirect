$(document).on("click", "#cart-button", function(ev) {
        ev.preventDefault();
        const csrftoken = Cookies.get('csrftoken');
        let item = $(this).attr("data-product-id");
        let platform = $(this).attr("data-product-platform");
        let quantity = 1;

        $.ajax({
            url: 'add_to_cart',
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            data: {
                'item_id': item,
                'platform': platform,
                'quantity': 1,
            },
            success: function (response) {
                $('#side-cart-dynamic').load(location.href + " #side-cart-dynamic");
            },
    });
    ev.preventDefault();
});

