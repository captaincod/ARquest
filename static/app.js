$(function () { // Short way for document ready.
    var counter = 1;
    $("#addButton").on("click", function () {
        if ($(".lat").length > 10) { // Number of boxes.
            alert("Максимум 10 точек в квесте");
            return false;
        }
        var newType = $(".lat").last().clone().addClass("newAdded"+counter); // Clone the group and add a new class.
        var newName = $(".lon").last().clone().addClass("newAdded"+counter);
        var newFile = $(".file").last().clone().addClass("newAdded"+counter);
        newType.appendTo("#fieldset"); // Append the new group.
        newName.appendTo("#fieldset");
        newFile.appendTo("#fieldset");

        document.getElementsByClassName("newAdded"+counter)[0].setAttribute("id","lat"+counter);
        document.getElementById("lat"+counter).getElementsByClassName("form-control")[0].setAttribute("name","lat"+counter);
        document.getElementsByClassName("newAdded"+counter)[1].setAttribute("id","lon"+counter);
        document.getElementById("lon"+counter).getElementsByClassName("form-control")[0].setAttribute("name","lon"+counter);
        document.getElementsByClassName("newAdded"+counter)[2].setAttribute("id","file"+counter);
        document.getElementById("file"+counter).getElementsByClassName("form-control-file")[0].setAttribute("name","file"+counter);

        counter = counter + 1;
    });

    $("#removeButton").on("click", function () {
        if ($(".lat").length == 1) { // Number of boxes.
            alert("Нет точек для удаления");
            return false;
        }
        $(".lat").last().remove(); // Remove the last group.
        $(".lon").last().remove();
        $(".file").last().remove();

        counter = counter - 1;
    });
});

function get_quest() {
    $.ajax({
        type: "POST",
        url: "/get_quest",
        data: $('form').serialize(),
        success: function(response) {
            var json = jQuery.parseJSON(response);
            var errors = json.errors;
            if (errors.length >= 1) {
                console.log(errors);
            };
        },
        error: function(error) {
            console.log(error);
        }
    });
}