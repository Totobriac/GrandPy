divx = document.getElementById("#chatbox");

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
        $("#chatbox").append( "<p class = display_question>"+data['user_question']+"</p>" );                            
        $("#user_form")[0].reset();
        $("#chatbox").append("<div class = pictures> </div>");       
        $(".pictures").last().append($('<img id = wiki_img>').attr('src', data['wiki_pic']));
        $(".pictures").last().append($('<img id = img>').attr('src', data['response']));        
        $("#chatbox").append( "<p class = wikidata>"+data['wiki_data']+"</p>" );                  
        $("#chatbox").animate({ scrollTop: 100000 }, "slow");  
                           
     });
     event.preventDefault();
     });     
});


