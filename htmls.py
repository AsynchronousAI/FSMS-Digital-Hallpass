js = """async function streamToString(stream) {
                const reader = stream.getReader();
                const decoder = new TextDecoder('utf-8');
                let result = '';
                let done, value;

                // Read the stream until it's done
                while ({ done, value } = await reader.read(), !done) {
                    result += decoder.decode(value, { stream: true });
                }

                // Decode any remaining data
                result += decoder.decode(); // Flush remaining data

                return result;
            }

            document.getElementById('sumbit').addEventListener('click', async function(event) {
                const name = document.getElementById('name').value;
                const reason = document.getElementById('reason').value;

                const data = { 
                    'name': name, 
                    'reason': reason 
                };

                const response = await fetch(window.location.href, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const error = await streamToString(response.body)
                if (error !== "success") {
                    document.getElementById('sumbit').setCustomValidity(error);
                    document.getElementById('sumbit').reportValidity();
                    console.error(error);
                } else {
                    location.reload();
                }
            });
            document.getElementById('return').addEventListener('click', async function(event) {
                const response = await fetch(window.location.href, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                });

                const error = await streamToString(response.body)
                if (error !== "success") {
                    document.getElementById('return').setCustomValidity(error);
                    document.getElementById('return').reportValidity();
                    console.error(error);
                } else {
                    location.reload();
                }
            });"""
searchJs = """document.getElementById('search').addEventListener('input', function(event) {
                const search = event.target.value.toLowerCase();
                const articles = document.querySelectorAll('article');
                articles.forEach(article => {
                    const teacher = article.querySelector('strong').innerText.toLowerCase();
                    if (teacher.includes(search)) {
                        article.style.display = 'block';
                    } else {
                        article.style.display = 'none';
                    }
                });
            });"""
nav = """
        <nav style="margin-left: 20px;">
            <ul>
                <li><strong>FSMS Digital Hallpass</strong></li>
                <li>
                   <input id="search" type="search" placeholder="Search teachers"/>
                </li>
            </ul>
        </nav>
"""
currentClassNav = """
        <nav style="margin-left: 20px;">
            <ul>
                <li><strong><a href="/">FSMS Digital Hallpass</a></strong></li>
                <li>Teacher: {current_class}</li>
                <li><a href="/{class_url}/download">Download Class Data</a></li>
            </ul>
        </nav>
"""
head = """<title>Digital Hall Pass</title><link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.red.min.css"
        /><style>
.error {{
    border: 1px solid red;
}}       
        </style>"""
footer = """<footer><center>
            <hr/>
            <b>Teacher:</b> Mr. Miller!<br/>
            <b>Made by:</b> Aarav Sethi<br/>
            <b>Help given by:</b> Bertulan, Nam Hoang, Joseph McKeon
        </center></footer>"""
mainPage = (
    """<html data-theme="light"><head>"""
    + head
    + """
    </head>
    <body>"""
    + nav
    + """
        <hr/>
        <br/>
        <div style="margin-left: 20px; margin-right: 20px;">
        {cards}
        </div>
        """
    + footer
    + """
    </body><script>
            {searchJs}
        </script>
</html>"""
)
card = '<article><strong>{teacher}</strong>\'s Class<br/><br/><a href="{url}">Start Here</a></article>'
html = (
    """<html data-theme="light"><head>"""
    + head
    + """</head>
    <body>"""
    + currentClassNav
    + """
        <hr/>
        <div style= "padding: 20px; text-align: center;">
            <div style="display: flex; justify-content: center; align-items: center;">
                <article id="new" style="border: 1px solid #C9C9C9; border-radius: 10px; padding: 20px; margin-right: 20px; border-radius: 10px; width: 800px;">
                    <h4>New Entry</h4>
                    <fieldset role="group">
                        <input required id="name" {disabled} placeholder="First & Last Name"/>
                        <input required id="reason" {disabled} placeholder="Reasoning"/>
                        <button data-tooltip="Click this to add an entry" data-placement="bottom" id="sumbit" {disabled}>Leave</button>
                    </fieldset>
                </article>
                <br/>
                <article id="return" style="border: 1px solid #C9C9C9; border-radius: 10px; padding: 20px; border-radius: 10px; width: 300px;">
                    <h4><b>{currentlyOut}</b> is currently out</h4>
                    <button id="return" data-tooltip="Click this when you return." data-placement="bottom" {notDisabled}>Return</button>
                </article>
            </div>
            <br/>
            <hr/>
            <br/>
            <table>
                <tr> 
                    <td>Name</td>
                    <td>Leave #</td>
                    <td>Reason</td>
                    <td>Exit Time</td>
                    <td>Return Time</td>
                </tr>
{table}
    </table></div>
        """
    + footer
    + """</body>
        <script>
            {js}
        </script></html>"""
)
