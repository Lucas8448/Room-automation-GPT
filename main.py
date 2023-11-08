from openai import OpenAI
import requests
from time import sleep
import json

api_key = ""
client = OpenAI(api_key=api_key)

thread = client.beta.threads.create()


def get_data(location):
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={location['lat']}&lon={location['lon']}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['properties']['timeseries'][0]['data']
    else:
        return "Failed to retrieve data"


location = {
    'lat': 59.9139,
    'lon': 10.7522
}


def send_data(data):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_me9gABGjqEXjX6840RzWZBuZ",
        instructions=str(data)
    )
    return run


def toggle_bed_lightstrip(state):
    if state not in ["on", "off"]:
        raise ValueError("Invalid state. Must be 'on' or 'off'.")
    # Implement the action to toggle the bed lightstrip
    print(f"Bed lightstrip toggled {state}.")


def set_bed_lightstrip_color(color):
    # Implement the action to set the color of the bed lightstrip
    print(f"Bed lightstrip color set to {color}.")


def toggle_desk_lamp(state):
    if state not in ["on", "off"]:
        raise ValueError("Invalid state. Must be 'on' or 'off'.")
    # Implement the action to toggle the desk lamp
    print(f"Desk lamp toggled {state}.")


def adjust_dimmer_lucas(level):
    if not 0 <= level <= 100:
        raise ValueError("Invalid level. Must be between 0 and 100.")
    # Implement the action to adjust the dimmer
    print(f"Dimmer adjusted to level {level}.")


def toggle_roof_lightstrip(state):
    if state not in ["on", "off"]:
        raise ValueError("Invalid state. Must be 'on' or 'off'.")
    # Implement the action to toggle the roof lightstrip
    print(f"Roof lightstrip toggled {state}.")


def set_roof_lightstrip_color(color):
    # Implement the action to set the color of the roof lightstrip
    print(f"Roof lightstrip color set to {color}.")


def control_floor_heating_lucas(temp):
    # Implement the action to control the floor heating
    print(f"Floor heating set to {temp}.")


def control_somfy_blinds(position):
    if position not in ["open", "close", "halfway"]:
        raise ValueError(
            "Invalid position. Must be 'open', 'close', or 'halfway'.")
    # Implement the action to control the Somfy blinds
    print(f"Somfy blinds moved to {position}.")


def toggle_wardrobe_lightstrip(state):
    if state not in ["on", "off"]:
        raise ValueError("Invalid state. Must be 'on' or 'off'.")
    # Implement the action to toggle the wardrobe lightstrip
    print(f"Wardrobe lightstrip toggled {state}.")


def set_wardrobe_lightstrip_color(color):
    # Implement the action to set the color of the wardrobe lightstrip
    print(f"Wardrobe lightstrip color set to {color}.")


function_dispatch = {
    'toggle_bed_lightstrip': toggle_bed_lightstrip,
    'set_bed_lightstrip_color': set_bed_lightstrip_color,
    'toggle_desk_lamp': toggle_desk_lamp,
    'adjust_dimmer_lucas': adjust_dimmer_lucas,
    'toggle_roof_lightstrip': toggle_roof_lightstrip,
    'set_roof_lightstrip_color': set_roof_lightstrip_color,
    'control_floor_heating_lucas': control_floor_heating_lucas,
    'control_somfy_blinds': control_somfy_blinds,
    'toggle_wardrobe_lightstrip': toggle_wardrobe_lightstrip,
    'set_wardrobe_lightstrip_color': set_wardrobe_lightstrip_color,
}


def call_action_function(function_name, arguments):
    # Convert the argument string to a dictionary (assuming arguments are in JSON format)
    arguments_dict = json.loads(arguments)
    # Call the corresponding function from the dispatch table
    function_dispatch[function_name](**arguments_dict)


def main():
    while True:
        data = get_data(location)
        run = send_data(data)

        waiting = True
        while waiting:
            run_return = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(run_return.status)
            if run_return.status in ["requires_action", "completed"]:
                waiting = False
                if run_return.status == "requires_action":
                    print("Requires action")
                    calls = run_return.required_action.submit_tool_outputs.tool_calls
                    for call in calls:
                        function_name = call.function.name
                        function_arguments = call.function.arguments
                        call_action_function(function_name, function_arguments)
                elif run_return.status == "completed":
                    print("Run completed")
        sleep(400)


if __name__ == "__main__":
    main()
