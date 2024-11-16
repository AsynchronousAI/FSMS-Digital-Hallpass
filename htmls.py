js = open("main.js", 'r').read()
mainPage = open("main.html", 'r').read()
card = "<article><strong>{teacher}</strong>'s Class<br/><br/><a href=\"{url}\">Here</a></article>"
html = open("class.html", 'r').read()