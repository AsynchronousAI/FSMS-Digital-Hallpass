# Imports
import os
from flask import Flask, send_file, request
import datetime
from typing import List
import htmls

# App
app = Flask(__name__)

# Globals
all_entries = {}
current = {}
classes = {"Mr. Miller": "miller"}

timezone = datetime.timezone(datetime.timedelta(hours=-6))


# Functions
def count_entries(current_class, name) -> int:
    """
    Count how many enties exist in the list with the same name.
    """

    count = 1

    for entry in all_entries[current_class]:
        if entry["name"] == name:
            count += 1

    return count


def get_day_with_ordinal(day):
    if 10 <= day <= 20:  # Special case for 11th to 20th, which all end in 'th'
        suffix = "th"
    else:
        # Get the last digit of the day
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    return f"{day}{suffix}"


@app.route("/")  # Main Menu
def error():
    global classes
    allCards = ""
    for current, value in classes.items():
        allCards += htmls.card.format(teacher=current, url=value)
    return htmls.mainPage.format(cards=allCards, searchJs=htmls.searchJs)


@app.route("/<current_class>", methods=["POST", "GET", "PUT"])  #
def index(current_class):
    global current

    try:
        if current_class not in list(classes.values()):
            return "Class does not exist"
        if current_class not in all_entries:
            all_entries[current_class] = []
        if current_class not in current:
            current[current_class] = {}
        if request.method == "POST":
            # Collect information
            ## Check for name
            if "name" in request.json and request.json["name"] != "":
                name = request.json["name"]
            else:
                return "Name required!"

            ## Check for last name
            if len(name.split(" ")) != 2:
                return "Please include your first and last name seperated by a space."

            ## Check for reason
            if "reason" in request.json and request.json["reason"] != "":
                reason = request.json["reason"]
            else:
                return "Reason required!"

            now = datetime.datetime.now(timezone)
            day_with_ordinal = get_day_with_ordinal(now.day)
            exit_time = f"{now.strftime('%B')} {day_with_ordinal}, {now.strftime('%I:%M %p')}"  # November 18th, 3:51 PM

            # Append to list
            count = count_entries(current_class, name)
            current[current_class] = {
                "name": name,
                "count": count,
                "reason": reason,
                "exit_time": exit_time,
            }

            return "success"
        elif request.method == "PUT":
            current[current_class] = {
                "name": current[current_class]["name"],
                "count": current[current_class]["count"],
                "reason": current[current_class]["reason"],
                "return_time": datetime.datetime.now(timezone).strftime("%I:%M %p"),
                "exit_time": current[current_class]["exit_time"],
            }

            all_entries[current_class].append(current[current_class])
            current[current_class] = {}
            return "success"

        elif request.method == "GET":
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
                currentlyOut=(
                    current[current_class] == {}
                    and "No one"
                    or current[current_class]["name"]
                ),
                notDisabled=(current[current_class] == {} and "disabled" or " "),
                table=table,
                current_class=list(classes.keys())[
                    list(classes.values()).index(current_class)
                ],
                js=htmls.js,
            )
    except Exception as e:
        return str(e)


def main():
    app.run(port=int(os.environ.get("PORT", 80)))


if __name__ == "__main__":
    main()
