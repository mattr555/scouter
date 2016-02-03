$(function(){
  $('#notes_form').ajaxForm({
    success: function(){
      $('#notes_sub').prop('disabled', true);
      $('#notes_status').text('ok');
    }
  });

  $('#notes_area').keydown(function(){
    $('#notes_sub').prop('disabled', false);
    $('#notes_status').text('');
  });

  function updateTagList(resp){
    $('#tags').html(resp);
    $('#tag_inp').val('');
    reselectForms();
  }

  function reselectForms(){
    $('.tag_del').ajaxForm({
      success: updateTagList
    });

    $('#tag_add').ajaxForm({
      success: updateTagList
    })
  }

  reselectForms();
})
