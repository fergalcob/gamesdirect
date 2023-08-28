
let item = '';

    $('body').on("mouseenter",'.wishlist',function(){
        item = $(this).attr("id");
        $('#' + item).addClass('fa-solid').removeClass('fa-regular').css('cursor', 'pointer');;
    });

    $("body").on("mouseleave",'.wishlist',function(){
        item = $(this).attr("id");
        $('#' + item).addClass('fa-regular').removeClass('fa-solid');
    });
    $('body').on("mouseenter",'.wishlist-login',function(){
        item = $(this).attr("id");
        $('#' + item).addClass('fa-solid').removeClass('fa-regular').css('cursor', 'pointer');;
    });

    $("body").on("mouseleave",'.wishlist-login',function(){
        item = $(this).attr("id");
        $('#' + item).addClass('fa-regular').removeClass('fa-solid');
    });

    $("body").on("click",'.wishlist',function(){
        const csrftoken = Cookies.get('csrftoken');
        id = $(this).attr("id");
        item = $(this).attr("data-game-id");
        platform = $(this).attr("data-platform");
        $('#' + id).addClass('remove-wishlist fa-solid fa-heart-circle-xmark').removeClass('wishlist fa-regular fa-heart');
        $.ajax({
            url: 'add_to_wishlist',
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            data: {
                'item_id': item,
                'platform_id' : platform
            }    
    });
});
$("body").on("click",'.remove-wishlist',function(){
    const csrftoken = Cookies.get('csrftoken');
    id = $(this).attr("id");
    item = $(this).attr("data-game-id");
    platform = $(this).attr("data-platform");
    $('#' + id).addClass('wishlist fa-regular fa-heart').removeClass('remove-wishlist fa-solid fa-heart-circle-xmark');
    $.ajax({
        url: 'remove_from_wishlist',
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: {
            'item_id': item,
            'platform_id' : platform
        },
        success: function (response) {
            $("#wishlist_item_" + id ).fadeOut(300, function() {
                $( "#wishlist_item_" + id ).remove();
            });
        },  
});
});
$("body").on("mouseenter",'.wishlist-login',function(){
    item = $(this).attr("id");
        $('#' + item).addClass('fa-solid').removeClass('fa-regular').css('cursor', 'pointer');
    });
    $("body").on("mouseleave",'.wishlist-login',function(){
        item = $(this).attr("id");
        $('#' + item).addClass('fa-regular').removeClass('fa-solid').css('cursor', 'pointer');
    });

