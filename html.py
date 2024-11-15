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

                console.log(await streamToString(response.body))
                location.reload()
            });
            document.getElementById('return').addEventListener('click', async function(event) {
                const response = await fetch(window.location.href, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                });

                console.log(await streamToString(response.body))
                location.reload()
            });"""
mainPage = """<html data-theme="light"><head><title>Digital hall pass</title><link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.red.min.css"
        >
    </head>
    <body>
        <nav>
            <ul>
                <li><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbspFSMS Digital Hallpass</strong></li>
            </ul>
        </nav>
        <hr/>
        <br/>
        <div className="body">
        {cards}
        </div>
        <footer><center>
            <hr/>
            Teacher: <b>Mr. Miller</b>!<br/>
            Primarily made by: <b>Aarav Sethi</b><br/>
            Help given by: Bertulan, Nam Hoang, Joseph McKeon
        </center></footer>
    </body>
</html>"""
card = "<article><strong>{teacher}</strong>'s Class<br/><br/><a href=\"{url}\">Here</a></article>"
html = """<html data-theme="light"><head><title>Digital hall pass</title><link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.red.min.css"
        >
    </head>
    <body>
        <nav>
            <ul>
                <li><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbspFSMS Digital Hallpass</strong></li>
            
                <li>Class: {current_class}</li>
            </ul>
        </nav>
        <hr/>
        <div style= "padding: 20px; text-align: center;">
            <div style="display: flex; justify-content: center; align-items: center;">
                <div className="body leaveForm" style="border: 1px solid #C9C9C9; border-radius: 10px; padding: 20px; margin-right: 20px; border-radius: 10px; width: 300px;">
                    <h3>New entry</h3>
                    <input required id="name" {disabled} placeholder="Your Name"/>
                    <input required id="reason" {disabled} placeholder="Reasoning"/>
                    <button data-tooltip="Click this to add an entry" data-placement="bottom" id="sumbit" {disabled}>Leave</button>
                </div>
                <br/>
                <div style="border: 1px solid #C9C9C9; border-radius: 10px; padding: 20px; border-radius: 10px; width: 300px;">
                    <h3>{currentlyOut} is currently out</h3>
                    <button id="return" data-tooltip="Click this when you return." data-placement="bottom" {notDisabled}>Return</button>
                </div>
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
        <footer><center>
            <hr/>
            Teacher: <b>Mr. Miller</b>!<br/>
            Primarily made by: <b>Aarav Sethi</b><br/>
            Help given by: Bertulan, Nam Hoang, Joseph McKeon
        </center></footer></body>
        <script>
            {js}
        </script></html>"""