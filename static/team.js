$(function(){
  $('#notes_form').ajaxForm({
    success: function(){
      $('#notes_sub').prop('disabled', true);
      $('#notes_status').css('display', 'inline');
    }
  });

  $('#notes_area').keydown(function(){
    $('#notes_sub').prop('disabled', false);
    $('#notes_status').css('display', 'none');
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

  $('#pit_save').click(function(){
    var $inputs = $('#pit_form :input');
    var tags = '';
    $inputs.each(function(){
      var val = $(this).val();
      if (val){
        if ($(this).prop('type') == 'radio' && !$(this).prop('checked')) return;
        tags += val + ',';
      }
    });

    $.post('/ajax/tag', {'do': 'add', 'license': $('#license_input').val(), 'name': tags.slice(0, -1)}, updateTagList);
    $('#pitModal').modal('hide');
  });
})
