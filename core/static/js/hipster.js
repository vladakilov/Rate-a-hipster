Hipster = {

  init: function () {
    Hipster.load_object();
    
    $('.vote').live('click', function () {
      $.ajax({
        type: "POST",
        url: "/api/vote/",
        data: {
          'id': $(this).parent().attr("id"),
          'rating': $(this).html()
        },
        dataType: "json",
        success: function (data) {
          if (Hipster.error_check(data) == true) {
            Hipster.load_object();
          } else {
            alert(data['error']);
          }
        }
      })
    })
  },

  load_object: function () {
    $.ajax({
      type: "GET",
      url: "/api/random/",
      dataType: "json",
      success: function (data) {
        if (Hipster.error_check(data) == true) {
          $.each(data['data'], function (key, val) {
            html = '<table><tr><td>ID</td><td>Name</td><td>Description</td><td>Score</td></tr>'
            html += '<tr><td>' + val['id'] + '</td><td>' + val['name'] + '</td><td>' + val['description'] + '</td><td>' + val['score'] + '</td></tr>'
            html += '<tr><img src="'+val['image']+'" onload="Hipster.resize(&quot;resize_500&quot;)" class="resize_500"></tr></table>'
            html += '<ul id=' + val['id'] + ' class="rate">\
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
                     </ul>';
            $('#document').html(html);
          })
        } else {
          alert(data['error']);
        }
      }
    })
  },

  load_page: function (page) {
    Hipster.clear_div();
    var html = '';
    $.ajax({
      type: "GET",
      data: {
        'page': page
      },
      url: "/api/doc/",
      dataType: "json",
      success: function (data) {
        if (Hipster.error_check(data) == true) {
	      // Display all image
          html += '<ul id="doc_items">';
          $.each(data['data'], function (key, val) {
            if (key % 2 == 0) {
              html += '<li class="even"><a href="/doc/' + data['data'][key]['id'] + '"><img src="' + data['data'][key]['image'] + '" onload="Hipster.resize(&quot;resize_200&quot;)" class="resize_200"></a></li>';
            } else {
              html += '<li class="odd"><a href="/doc/' + data['data'][key]['id'] + '"><img src="' + data['data'][key]['image'] + '" onload="Hipster.resize(&quot;resize_200&quot;)" class="resize_200"></a></li>';
            }
          });
          html += '</ul><div id="pagination"><ul>';
          // Pagination
          if (data['paging']) {
	        if (data['paging']['previous_page']) {
              html += '<li class="paginate" onclick="Hipster.load_page(' + data["paging"]["previous_page"] + ')">Previous Page</li>';
            }
            $.each(data['paging']['page_list'], function (key, val) {
              html += '<li class="paginate" onclick="Hipster.load_page(' + val + ')">'+val+'</li>';
	        })
	        if (data['paging']['next_page']) {
              html += '<li class="paginate" onclick="Hipster.load_page(' + data["paging"]["next_page"] + ')">Next Page</li>';
            }
          }
          html += '</ul></div>'
          $('#doc_list').html(html);

        } else {
          alert(data['error']);
        }
      }
    })
  },

  error_check: function (data) {
    var result;
    if ('error' in data) {
      result = 'error';
    } else {
      result = true;
    }
    return result;
  },

  clear_div: function () {
    $('#document').html('')
  },

  resize: function (type) {
    var size = type.slice(-3)
    $('.'+type).each(function () {
      var maxWidth = size;
      var maxHeight = size;
      var ratio = 0;
      var width = $(this).width();
      var height = $(this).height();

      if (width > maxWidth) {
        ratio = maxWidth / width;
        $(this).css("width", maxWidth);
        $(this).css("height", height * ratio);
        height = height * ratio;
        width = width * ratio;
      }

      if (height > maxHeight) {
        ratio = maxHeight / height;
        $(this).css("height", maxHeight);
        $(this).css("width", width * ratio);
        width = width * ratio;
      }
    })
  }

}