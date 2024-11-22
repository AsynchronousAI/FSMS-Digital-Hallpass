import datetime, re, json
import requests, os, base64

file_path = "data.json"
url = f"https://api.github.com/repos/AsynchronousAI/FSMS-Digital-Hallpass/contents/{file_path}"
headers = {
    "Authorization": "token " + os.environ["GITHUB_TOKEN"],
}

timezone = datetime.timezone(datetime.timedelta(hours=-6))


# Custom function for serializing datetime objects
def datetime_converter(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()  # Convert datetime to ISO 8601 string
    raise TypeError("Type not serializable")


# Custom function for deserializing datetime strings
def datetime_parser(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                # Attempt to parse datetime strings in ISO format
                dct[key] = datetime.datetime.fromisoformat(value).replace(
                    tzinfo=timezone
                )
            except ValueError:
                pass  # If it can't be parsed, leave it as a string
    return dct


def fromCSV(csvfile):
    lines = open(csvfile, "r").readlines()
    lines.reverse()
    allData = []
    for line in lines:
        fields = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
        allData.append(
            {
                "name": fields[0].replace('"', ""),
                "count": fields[1].replace("#", ""),
                "reason": fields[2],
                "exit_time": fields[3] + ", " + fields[4],
                "datetime": datetime.datetime.now(),  # This data is not in the CSV file, so sadly lost to time
                "return_time": fields[5],
            }
        )

    return allData


def toStorage(data, sha):
    encoded = json.dumps(data, default=datetime_converter)

    data = {
        "message": "Automated update by app",
        "content": base64.b64encode(encoded.encode("utf-8")).decode("utf-8"),
        "branch": "main",
        "sha": sha,
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code != 200 and response.status_code != 201:
        print("ERROR: ", response.text)


def fromStorage():
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("ERROR: ", response.text)

    response_data = response.json()
    json_content = base64.b64decode(response_data["content"]).decode("utf-8")
    content = json.loads(json_content, object_hook=datetime_parser)

    return content, response_data["sha"]
