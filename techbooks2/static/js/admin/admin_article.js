<!--

	var num_of_page = 0;

	function Page(){
    var page_name;
    this.page_name = "page" + num_of_page;
		num_of_page ++;
		var div = document.createElement('div');
		div.innerHTML = document.getElementById('preset_page').innerHTML;
		div.id = this.page_name;
		div.className = "webeditor_page row";
		document.getElementById('field').appendChild(div);
	}

	Page.prototype.addContent = function(){
		var div = document.createElement('div');
		div.innerHTML = document.getElementById('preset_content').innerHTML;
		div.className = "webeditor_content row";
		document.getElementById(this.page_name).appendChild(div);
	}

	Page.prototype.removePage = function(){
    var page = $("#" + this.page_name);
    page.fadeOut(200, function(){
      $(this).remove();
			sorting_handle();
    });
		console.log(this.page_name + " is removed.");
	}

	function add_page(){
		var page_name = "page" + num_of_page;
		window[page_name] = new Page;
		console.log(page_name + " is added.");
		sorting_handle();
	}

	var label_option = {};
	label_option['title'] = ['content'];
	label_option['section'] = ['content'];
	label_option['question'] = ['content'];
	label_option['answer'] = ['content'];
	label_option['description'] = ['content'];
	label_option['notice'] = ['content'];
	label_option['movie_a'] = ['content', 'thumbnail', 'copyright'];
	label_option['movie_b'] = ['content', 'copyright'];
	label_option['image'] = ['content', 'copyright'];
	label_option['gif'] = ['content', 'copyright'];
	label_option['button'] = ['content', 'link'];
	label_option['image_button'] = ['content', 'link'];
	label_option['comment'] = ['name', 'content'];
	label_option['profile'] = ['name', 'job', 'content', 'image'];


  function change_labels(element){
    var selOption = element.val();
		var options = label_option[selOption];
		var parent = element.parent();
		if (options){
			var i;
			var div = document.createElement('div');
			for (i = 0; i < options.length; i++) {
				var p = document.createElement('p');
				p.innerHTML ='<label>' + options[i] + '</label>\
				<textarea rows="3"></textarea>';
				p.className = options[i] + " content_holder";
				div.appendChild(p);
			}
			$("div", parent).remove(".content_data")
      div.className = "content_data";
			parent.append(div);
			if (selOption == 'image' || selOption == 'gif' || selOption == 'image_button' || selOption == 'movie_a' || selOption == 'movie_b'){
				//parent_target = $("textarea",$(".content", $(parent)));
				$('<input />',{
		      type: "button",
		      value: "파일 업로드",
					class: "btn btn-default",
					onclick: 'var image_upload_window = window.open("/techbook/admin/article/image_upload/", "파일 업로드", "width=600, height=400, toolbar=no, menubar=no, scrollbars=no, resizable=yes");\
												image_upload_window.parent_target = $("textarea",$(".content", $(this).parent()));\
												image_upload_window.target_label = $(".labels",$(this).parents().eq(1)).val();'
		    }).appendTo($(".content_data",$(parent)));
				if (selOption == 'movie_a'){
					$('<input />',{
			      type: "button",
			      value: "썸네일 업로드",
						class: "btn btn-default",
						style: "margin-left:10px",
						onclick: 'var image_upload_window = window.open("/techbook/admin/article/image_upload/", "썸네일 업로드", "width=600, height=400, toolbar=no, menubar=no, scrollbars=no, resizable=yes");\
													image_upload_window.parent_target = $("textarea",$(".thumbnail", $(this).parent()));\
													image_upload_window.target_label = $(".labels",$(this).parents().eq(1)).val();\
													image_upload_window.is_thumbnail = true'
			    }).appendTo($(".content_data",$(parent)));
				}
			}
		}
  };

	$(document).on("change",".labels",function(){
    change_labels($(this));
	});

	function to_json() {
		var _contents = []
		$('.webeditor_page').each(function(i){
			_contents.push([]);
			$(".labels", this).each(function(index, item){
				var selectedLabel = item[item.selectedIndex].value;
				var _content = {};
				_content['label'] = selectedLabel;
				$(".content_holder",$(this).parent()).each(function(){
					_content[$("label", $(this)).html()] = $("textarea", $(this)).val();
				})
				_contents[i].push(_content);
			});
		})
		var json_string = JSON.stringify(_contents);
	  $("#id_content").html(json_string);
		let category = $("#id_category").val();
		let title = $("#id_title").val();
		previewer_loader(_contents, category, title, "");
	}

	$(function(){
		$('#field').sortable({
	      items: ".webeditor_page > .webeditor_content",
	      placeholder: 'ui-state-highlight',
				distance:30,
				axis: "y",
	      over: function(event, ui) {
	      		var cl = ui.item.attr('class');
	      		$('.ui-state-highlight').addClass(cl);
	  		}
	  });
	});

	$(window).resize(function(){
		$("#preview_box").css('left',($(".article-container")[0].offsetLeft + 465)/2 + 'px');
	})


	$(document).ready(function() {
	  label_loader();
	  let content = JSON.parse($("#id_content").html());
		let category = $("#id_category").val();
		let title = $("#id_title").val();
		previewer_loader(content, category, title, "");
	  for (var i = 0; i < content.length ; i++){
	    add_page();
	    for (var j = 0; j < content[i].length ; j++){
	      window[$(".webeditor_page").last().attr('id')].addContent();
	      var last_content = $(".webeditor_content").last();
	      var label;
	      $(".labels", last_content).each(function(){
	        label = content[i][j]['label'];
	        $(this).val(label);
	        change_labels($(this));
	        var content_data = $(this).next();
	        $("p", content_data).each(function(){
	          $("textarea", $(this)).html(content[i][j][$("label", $(this)).html()]);
	        })
	      });
	    }
	  }
		$("#preview_box").css('left',($(".article-container")[0].offsetLeft + 465)/2 + 'px');
	});

	function sorting_handle(){
		$(".sorting-handle").remove();
		let div = $('<div/>',{
			class: 'sorting-handle',
			html: '<i class="fas fa-sort"></i>'
		});
		$(".webeditor_page:not(:last)").after(div);
		$(".sorting-handle").on("click",function(e){
			let prev = $(this).prev().detach();
			let next = $(this).next().detach();
			$(this).after(prev);
			$(this).before(next);
		})
	}

	function label_loader(){
	  var labels = $(".labels");
	  var labels_key = Object.keys(label_option);
	  $('<option />',{
	    value: "",
	    html: "라벨 선택"
	  }).appendTo(labels);
	  for (var i = 0; i < labels_key.length; i++) {
	    $('<option />',{
	      value: labels_key[i],
	      html: labels_key[i]
	    }).appendTo(labels);
	  }
	}
//-->
