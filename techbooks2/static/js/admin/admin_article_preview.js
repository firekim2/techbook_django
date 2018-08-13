previewer_loader = (content, category, title, i) => {
  let categories = ['테크토크', '테크피플', '못보던 프로토타입']

  get_question_template = (mark, content) => {
	// javascript template literal
	// https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Template_literals
  	return `<div class="content_preview question_answer">
  			<div class="qna_mark">${mark}.</div>
  			<div class="qna_content">${content}</div>
  		</div>`;
  }


  block_template = (item) => {
  	// line-break 하면 될 것 같아여
  	var content = item.content.replace(/(?:\r\n|\r|\n)/g, '<br />');
  	switch (item.label) {
  		case 'title':
  			return `<div class="content_preview title"><h3> ${content} </h3></div>`;
      case 'description':
        return `<div class="content_preview description"><p> ${content} </p></div>`;
      case 'movie_a':
        return `<div class="content_preview movie_a">
                  <video src="${content}" controls>video_error</video>
                  <p class="copyright_preview">${item.copyright}</p>
                </div>`;
      case 'movie_b':
        return `<div class="content_preview movie_b">
                  <video src="${content}" controls>video_error</video>
                  <p class="copyright_preview">${item.copyright}</p>
                </div>`;
      case 'image':
      case 'gif':
        return `<div class="content_preview image">
                  <img src="${content}">
                  <p class="copyright_preview">${item.copyright}</p>
                </div>`;
      case 'notice':
        return `<div class="content_preview notice">
                  <p> ${content} </p>
                </div>`;
      case 'section':
        return `<div class="content_preview section">
                  <h3> ${content} </h3>
                </div>`;
      case 'answer' :
      case 'question' :
        return get_question_template(item.label === "question" ? "Q" : "A", content);
      case 'comment':
        return `<div class="content_preview comment">
                  <p>${item.name}</p>
                  <p>${content}</p>
                </div>`;
      case 'profile':
        return `<div class="content_preview comment">
                  <p>${item.name} (${item.job})</p>
                  <p>${content}</p>
                </div>`;
      case 'button':
        return `<div class="content_preview button">
                  <a href="${item.link}">${item.content}</a>
                </div>`
      case 'image_button':
        return `<div class="content_preview image_button">
                  <a href="${item.link}"><img src="${item.content}"></a>
                </div>`
  		default:
  			return "";
  	}
  }


  var pages = (content || []).map((page) => {
  	var page_template = page.map((item) => {
  		return block_template(item);
  	}).join("");
  	return `<div class='page_preview'>${page_template}</div>`;
  }).join("");


  top_category_valid_checker = (valid, item) => {
    return `<div class="top-category ${valid}"> ${item} </div>`
  }


  top_nav = () => {
    var top_category = categories.map((item, index) => {
      return top_category_valid_checker(category === index ? "valid" : "", item)
    }).join("");
    return `<nav class="top" id="top">
              ${top_category}
              <div class="top-title"><h3>${title}</h3></div>
            </nav>`
  }

  var template = top_nav() + `<div class="previewer height100 scroll_y"> ${pages} </div>`;
	$("#preview_box"+i).html(template);
}
