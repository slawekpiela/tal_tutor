import requests
import streamlit as st


def get_a_joke():
    url = "https://icanhazdadjoke.com/"

    # Custom headers including the desired User-Agent
    headers = {
        "User-Agent": "My Library (https://github.com/username/repo)",
        "Accept": "application/json"  # Ask the server to return JSON
    }

    # Perform the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data['joke'])
    else:
        print("Failed to retrieve joke. Status code:", response.status_code)

    return data["joke"]


def main():
    click = st.button("Get a joke")
    if click:
        response = get_a_joke()

        st.write(response)


main()
