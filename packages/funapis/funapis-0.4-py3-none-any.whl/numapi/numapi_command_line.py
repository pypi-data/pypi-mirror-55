import numapi

import sys, os, requests

argumentList = sys.argv

script_dir = os.path.dirname(__file__)
token_file_path = os.path.join(script_dir, "token.txt")

headers = {
    'x-rapidapi-host': "numbersapi.p.rapidapi.com",
    # 'x-rapidapi-key': "7e04752b81msh7b9ecaaba88e7b3p1f0a1fjsnd3ac29e67955"
}

with open(token_file_path, 'r') as file:
    headers["x-rapidapi-key"] = str(file.read())

def test_token(token):
    headers["x-rapidapi-key"] = token
    url = "https://numbersapi.p.rapidapi.com/random/trivia"
    querystring = {"max":"20","fragment":"true","min":"10","json":"true"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.ok

def update_token(token):
    if not test_token(token):
        return False

    with open(token_file_path, 'w') as file:
        file.write(token)
        file.close()

    return True

def main():
    """
    Get fact about number passed from command line
    """

    if "-t" in argumentList:
        if not update_token(argumentList[argumentList.index("-t") + 1]):
            sys.stdout.write("Unable to update token, it may be invalid or file may not be written properly.\nCheck token validity again!\n")
            sys.stdout.flush()
            return
        headers["x-rapidapi-key"] = argumentList[argumentList.index("-t") + 1]
        argumentList.pop(argumentList.index("-t"))
        argumentList.pop(argumentList.index(headers["x-rapidapi-key"]))


    if len(argumentList) > 2:
        if argumentList[1] == "-f":
            querystring = {"fragment":"true","json":"true"}
            url = f"https://numbersapi.p.rapidapi.com/{argumentList[2]}/math"
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.json()

            sys.stdout.write(f"{str(data['text'])}\n")
        elif argumentList[1] == "-ft":
            querystring = {"fragment":"true","notfound":"floor","json":"true"}
            url = f"https://numbersapi.p.rapidapi.com/{argumentList[2]}/trivia"
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.json()

            sys.stdout.write(f"{str(data['text'])}\n")
        elif argumentList[1] == "-fy":
            querystring = {"fragment":"true","json":"true"}
            url = f"https://numbersapi.p.rapidapi.com/{argumentList[2]}/year"
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.json()

            if "date" in data:
                sys.stdout.write(f"{str(data['date'])}, {str(data['number'])} - {str(data['text'])}\n")
            else:
                sys.stdout.write(f"{str(data['number'])} - {str(data['text'])}\n")
        elif argumentList[1] == "-fd":
            if "/" not in str(argumentList[2]):
                sys.stdout.write("Please provide date in the form of - mm/dd")
                sys.flush()
                return
            querystring = {"fragment":"true","json":"true"}
            url = f"https://numbersapi.p.rapidapi.com/{argumentList[2]}/date"
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.json()

            sys.stdout.write(f"{str(data['year'])} - {str(data['text'])}\n")
        else:
            sys.stdout.write("Please provide options in - '-f', '-ft', '-fy' or '-fd'")
    elif len(argumentList) > 1:
        if argumentList[1] == "-h":
            sys.stdout.write("Command line options - \n")
            options = [(
                "<none>", "get trivia fact about random number"),
                ("-f", "get math fact about a number. Ex. -f 29"),
                ("-ft", "get trivia fact about a number. Ex. -ft 7"),
                ("-fy", "get fact about year. Ex. -fy 2003"),
                ("-fd", "get fact about date. Ex. -fd 5/23")
            ]
            for pair in options:
                sys.stdout.write(f"\t{pair[0]}\t{pair[1]}\n")
            sys.stdout.flush()
            return

        querystring = {"fragment":"true","json":"true"}
        url = f"https://numbersapi.p.rapidapi.com/{argumentList[1]}/math"
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()

        sys.stdout.write(f"{str(data['text'])}\n")
    else:
        url = "https://numbersapi.p.rapidapi.com/random/trivia"
        querystring = {"max":"20","fragment":"true","min":"10","json":"true"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()

        sys.stdout.write(f"{str(data['number'])} - {str(data['text'])}\n")

    sys.stdout.flush()
    return
