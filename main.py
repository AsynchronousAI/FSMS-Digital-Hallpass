# Imports
from flask import Flask, send_file, request
import io, os, datetime, htmls, database

# App
app = Flask(__name__)

# Globals
all_entries, sha = database.fromStorage()
current = {}
classes = {"Mr. Miller": "miller"}

timezone = database.timezone


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


@app.route("/<current_class>", methods=["POST", "GET", "PUT"])  # Class Page
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
                "datetime": now,
                "return_time": "Out",
            }

            return "success"
        elif request.method == "PUT":
            current[current_class] = {
                "name": current[current_class]["name"],
                "count": current[current_class]["count"],
                "reason": current[current_class]["reason"],
                "return_time": datetime.datetime.now(timezone).strftime("%I:%M %p"),
                "exit_time": current[current_class]["exit_time"],
                "datetime": current[current_class]["datetime"],
            }

            all_entries[current_class].append(current[current_class])

            database.toStorage(all_entries, sha)

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
                class_url=current_class,
                current_class=list(classes.keys())[
                    list(classes.values()).index(current_class)
                ],
                js=htmls.js,
            )
    except Exception as e:
        return str(e)


@app.route("/<current_class>/download", methods=["GET"])  # Download one class
def download(current_class):
    if current_class not in list(classes.values()):
        return "Class does not exist"
    if current_class not in all_entries:
        all_entries[current_class] = []
    if current_class not in current:
        current[current_class] = {}

    data = all_entries[current_class]
    data.reverse()

    # Convert to CSV in BytesIO
    csv = "Name,Leave #,Reason,Date,Exit Time,Return Time\n"
    for entry in data:
        csv += f"\"{entry['name']}\",{entry['count']},{entry['reason']},{entry['exit_time']},{entry['return_time']}\n"

    output = io.BytesIO()
    output.write(csv.encode("utf-8"))
    output.seek(0)

    # Return the file as a downloadable response
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="FSMSDigitalHallpass-" + current_class + ".csv",
    )


@app.route("/download", methods=["GET"])  # Download all classes
def downloadAll():
    data = []
    for class_name, entries in all_entries.items():
        for entry in entries:
            data.append(
                {
                    "name": entry["name"],
                    "count": entry["count"],
                    "reason": entry["reason"],
                    "exit_time": entry["exit_time"],
                    "return_time": entry.get("return_time", ""),
                    "class": class_name,
                    "datetime": entry["datetime"],
                }
            )
    data = sorted(data, key=lambda x: x["datetime"])
    data.reverse()

    # Convert to CSV in BytesIO
    csv = "Name,Leave #,Reason,Date,Exit Time,Return Time,Class\n"
    for entry in data:
        csv += f"\"{entry['name']}\",{entry['count']},{entry['reason']},{entry['exit_time']},{entry['return_time']},{entry['class']}\n"

    output = io.BytesIO()
    output.write(csv.encode("utf-8"))
    output.seek(0)

    # Return the file as a downloadable response
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="FSMSDigitalHallpass-allData.csv",
    )


def main():
    app.run(port=int(os.environ.get("PORT", 80)), debug=True)


if __name__ == "__main__":
    main()
