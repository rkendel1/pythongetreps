import requests
import geocoder
import json
# Detect latitude and longitude
g = geocoder.ip('me')
latitude = g.latlng[0]
longitude = g.latlng[1]

url = f"https://v3.openstates.org/people.geo?lat={latitude}&lng={longitude}&include=other_identifiers"

payload = {}
headers = {
    'X-API-Key': 'fa4ad3d1-031f-4e40-8cb0-4cf1a5344052'
}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()  # Assuming the response is in JSON format

# Parse the JSON response
data = json.loads(response.text)

# Extract values for "id" and "biodguide"
for entry in data.get("results", []):
    person_id = entry.get("id")
    biodguide = next((id_entry["identifier"] for id_entry in entry.get("other_identifiers", []) if id_entry["scheme"] == "bioguide"), None)

    # Save the values to the user profile in the database
    user_profile = UserProfile(person_id=person_id, biodguide=biodguide)
    session.add(user_profile)
    session.commit()

    # Print or use the values as needed
    print(f"Person ID: {person_id}")
    print(f"Biodguide: {biodguide}")

