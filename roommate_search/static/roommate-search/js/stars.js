$(document).ready(function () {
    var box = $(".box");

    function getOrCreateBox () {
        if (box.length < 1) {
            box = $("<div class='box'><ul/></div>").prependTo("div#content");
        }
        return box;
    }

    function toggleLinks (el) {
        el.parent().find("a.profile-star").toggle();
    }

    $("a.profile-star").click(function (event) {
        event.preventDefault();

        var el = $(this),
        id = el.attr("id").replace("profile-star-", "");

        function postHandler(data) {
            if (data.message !== "Success") {
                getOrCreateBox().find("ul").append(
                    '<li class="error">The server is having some issues, try again soon.</li>'
                );
            }
        }

        $.post(el.attr("href"), {}, postHandler);
        toggleLinks(el);
    });
});
