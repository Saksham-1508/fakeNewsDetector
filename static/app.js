var news = document.querySelectorAll(".news");


fetch('https://gnews.io/api/v4/top-headlines?country=in&lang=en&token=9210044dd1ed359b2b51029d1b14b577')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        console.log(data.articles[0]);
        news.forEach((element, index) => {
            var article = data.articles[index]
            element.innerHTML += "<img style='float:left;height:275px;padding:0 3px;' src=" + article.image + "><div style='display:flex;flex-direction:column;margin:0 5px;padding:3px;'><h1>" + article.title + "</h1><p>" + article.description + "</p><a href='" + article.url + "'style='float:bottom;' target='_blank' class='article-link'>Go To Article</a></div>";
        })

    });