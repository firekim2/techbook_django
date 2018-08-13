$(document).ready(() => {
  let articles = $(".article");
  articles.each((index) => {
    let article = JSON.parse($("#article"+index).html());
    let category = article.category;
    let category_no = article.category_no;
    let title = article.title;
    let content = article.content;
    previewer_loader(content, category_no, title, index);
    $("#btn-article-editor-" + index).on("click",function(){
      location.href='/techbook/admin/article/' + article.edition + '_' + article.category_no;
    })
  })
});
