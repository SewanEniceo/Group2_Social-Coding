import urllib.parse
import requests

def get_user_input():
    orig = input("Starting Location: ")
    dest = input("Destination: ")
    return orig, dest

def make_api_request(orig, dest):
    main_api = "https://www.mapquestapi.com/directions/v2/route?" 
    key = "7UcV7QoQ7grGFJB2w4QYHmaSJmMYqoj2"
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    return requests.get(url).json()

def print_route_info(json_data):
    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print("Directions from {} to {}".format(orig, dest))
        print("Trip Duration:   {}".format(json_data["route"]["formattedTime"]))
        print("Kilometers:      {:.2f}".format((json_data["route"]["distance"]) * 1.61))
        print("=============================================")
        for i, each in enumerate(json_data["route"]["legs"][0]["maneuvers"], start=1):
            print("{}. {} ({:.2f} km)".format(i, each["narrative"], (each["distance"]) * 1.61))
            print("=============================================\n")
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: {}; Invalid user inputs for one or both locations.".format(json_status))
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: {}; Missing an entry for one or both locations.".format(json_status))
        print("**********************************************\n")
    else:
        print("************************************************************************")
        print("For Status Code: {}; Refer to:".format(json_status))
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")

def save_history(orig, dest, json_data):
    with open("route_history.txt", "a") as file:
        file.write("From: {}\nTo: {}\n".format(orig, dest))
        file.write("Duration: {}\n".format(json_data["route"]["formattedTime"]))
        file.write("Distance: {:.2f} km\n".format((json_data["route"]["distance"]) * 1.61))
        file.write("=" * 50 + "\n")

if __name__ == "__main__":
    while True:
        orig, dest = get_user_input()
        if orig.lower() == "quit" or dest.lower() == "quit" or orig.lower() == "q" or dest.lower() == "q":
            break
        json_data = make_api_request(orig, dest)
        print_route_info(json_data)
        save_history(orig, dest, json_data)
