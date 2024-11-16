async function streamToString(stream) {
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
});