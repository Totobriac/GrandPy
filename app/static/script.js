divx = document.getElementById("#chatbox");

$(document).ajaxStart(function () {
    $("#waitScreen").fadeIn('slow');
    $(".big").addClass("rotate");
    $(".medium").addClass("rotate");
    $(".small").addClass("reverseRotate");
    $(".huge").addClass("reverseRotate");    
});

$(document).ready(function() {
    $('form').on('submit', function(event) {
           
      $.ajax({
         data : {
            question : $('#question').val(),            
                },
            type : 'POST',
            url : '/process'
           })
    
    .done(function(data) {
        var loaded = 0;                  
        $("#chatbox").append( "<p class = display_question>"+data['user_question']+"</p>" );                            
        $("#user_form")[0].reset();
        $("#chatbox").append("<div class = pictures> </div>");       
        $(".pictures").last().append($('<img id = wiki_img>').attr('src', data['wiki_pic']));
        $(".pictures").last().append($('<img id = img>').attr('src', data['response']));
        $("img").on('load', function(){
            loaded ++;
            if(loaded == 2) {
            $(".big").removeClass("rotate");
            $(".medium").removeClass("rotate");
            $(".small").removeClass("reverseRotate");
            $(".huge").removeClass("reverseRotate");
            $("#waitScreen").fadeOut('slow');
            console.log("loaded!!")}
        });
        $("#chatbox").append( "<p class = wikidata>"+data['wiki_data']+"</p>" );                  
        $("#chatbox").animate({ scrollTop: 100000 }, "slow");                                  
     });
     event.preventDefault();
     });     
});