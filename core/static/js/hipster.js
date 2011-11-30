Hipster = {
  
  init: function () {
    Hipster.load_object()

    $('.vote').live('click', function () {
      $.ajax({
        type: "POST",
        url: "/vote/",
        data: {
          'id': $(this).parent().attr("id"),
          'rating': $(this).html()
        },
        dataType: "json",
        success: function (data) {
          if (error_check(data) == true) {
            load_object()
          } else {
            alert(data['error'])
          }
        }
      })
    })
  }

  load_object: function () {
    $.ajax({
      type: "GET",
      url: "/random/",
      dataType: "json",
      success: function (data) {
        if (Music.error_check(data) == true) {
          $.each(data['data'], function (key, val) {
            html = '<table><tr><td>ID</td><td>Name</td><td>Description</td><td>Score</td></tr>'
            html += '<tr><td>' + val['id'] + '</td><td>' + val['name'] + '</td><td>' + val['description'] + '</td><td>' + val['score'] + '</td></tr>'
            html += '<tr><img src="' + val['image'] + '"></tr></table>'
            html += '<ul id=' + val['id'] + '>\
                       <li class="link vote">1</li>\
                       <li class="link vote">2</li>\
                       <li class="link vote">3</li>\
                       <li class="link vote">4</li>\
                       <li class="link vote">5</li>\
                       <li class="link vote">6</li>\
                       <li class="link vote">7</li>\
                       <li class="link vote">8</li>\
                       <li class="link vote">9</li>\
                       <li class="link vote">10</li>\
                     </ul>'
            $('#document').html(html)
          })
        } else {
          alert(data['error'])
        }
      }
    })
  }

  error_check: function (data) {
    var result
    if ('error' in data) {
      result = 'error'
    } else {
      result = true
    }
    return result
  }

}

$(document).ready(function() {
  Hipster.init()
})