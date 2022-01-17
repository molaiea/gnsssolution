let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

$(document).ready(function(){
    $(".rinexfile").change(function(){
        console.log("test");
        console.log($(".rinexfile").get(0).files[0].value);
    })
    $(".submit").click(function(e){

        var f_obj = $(".rinexfile").get(0).files[0];
        console.log("File object:",f_obj.value);
        //console.log("The file name is:",f_obj.name);
        //console.log("The file size is:",f_obj.size);

        // var data = new FormData();                                      //Create formdata objects to facilitate file transfer to the back end
        // data.append("file",f_obj)

        $.ajax({
            type: "POST",
            url: "/sendData",
            data: {'data':f_obj.value},
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            dataType: "json",
            success: function (data) {
                // any process in data
                alert("successfull")
            },
            failure: function () {
                alert("failure");
            }
        });
    })
})