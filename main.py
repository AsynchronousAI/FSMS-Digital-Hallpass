# Imports
import os
from flask import Flask, send_file, request
import datetime
from typing import List
from . import html as htmls

# App
app = Flask(__name__)

# Globals
all_entries = {}
current = {}
classes = {
    "Mr. Miller": 'miller'
}

timezone = datetime.timezone(datetime.timedelta(hours=-6))
# Functions
def count_entries(current_class, name) -> int:
    """
        Count how many enties exist in the list with the same name.
    """
    
    count = 1

    for entry in all_entries[current_class]:
        if entry['name'] == name:
            count += 1

    return count

@app.route('/') # Main Menu
def error():
    global classes
    allCards = ""
    for current, value in classes.items():
        allCards += htmls.card.format(
            teacher=current,
            url=value
        )
    return htmls.mainPage.format(
        cards = allCards
    )

@app.route('/<current_class>', methods=['POST', 'GET', 'PUT']) # 
def index(current_class):
    global current
    if current_class not in list(classes.values()):
        return "Class does not exist"
    if current_class not in all_entries:
        all_entries[current_class] = []
    if current_class not in current:
        current[current_class] = {}
    if request.method == 'POST':
        try:
            # Collect information
            if "name" in request.json:
                name = request.json['name'] or ""
            if "reason" in request.json:
                reason = request.json['reason'] or ""
            exit_time = datetime.datetime.now(timezone).strftime('%I:%M %p')

            # Append to list
            return_time = datetime.datetime.now(timezone).strftime("%I:%M %p")
            count = count_entries(current_class, name)
            current[current_class] = {
                'name': name,
                'count': count,
                'reason': reason,
                'exit_time': exit_time,
                'return_time': return_time
            }

            return "success"
        except Exception as e:
            return str(e)
    elif request.method == 'PUT':
        all_entries[current_class].append(current[current_class])
        current[current_class]={}
        return "success"

    elif request.method == 'GET':
        table = ""
        for entry in reversed(all_entries[current_class]):
            table += f"""<tr>
                <td>{entry['name']}</td>
                <td>#{entry['count']}</td>
                <td>{entry['reason']}</td>
                <td>{entry['exit_time']}</td>
                <td>{entry['return_time']}</td>
            </tr>
            """
        return htmls.html.format(
            disabled=(current[current_class] == {} and " " or "disabled"),
            currentlyOut=(current[current_class] == {} and "No one" or current[current_class]['name']),
            notDisabled=(current[current_class] == {} and "disabled" or " "),
            table=table,
            current_class=list(classes.keys())[list(classes.values()).index(current_class)],
            js=htmls.js
        )
def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
