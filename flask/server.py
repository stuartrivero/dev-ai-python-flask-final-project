# Import the Flask class from the flask module
# Import the Flask class from the flask module
from flask import Flask, make_response, request

data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]


# Create an instance of the Flask class, passing in the name of the current module
app = Flask(__name__)


@app.errorhandler(400)
def handle_400(error):
    return {"message": f"{error}"}, 400

@app.errorhandler(Exception)
def handle_exception(e):
    return {"message": str(e)}, 500

@app.route("/test500")
def test500():
    raise Exception("Forced exception for testing")

@app.route("/count")
def count():
    return f"{len(data)}", 200


@app.route("/name_search")
def name_search():
    name= request.args.get("q")
    # Check if the query parameter is present but invalid (e.g., empty or numeric)
    if name.strip() == "" or name.isdigit():
        return {"message": "Invalid input parameter"}, 422
    if not name:
        return {"message":"Invalid input parameter"},400


    user = next((u for u in data if u["first_name"] == name), None)

    if not user:
        return {"message":"Person not found"},404

    return user, 200

@app.route("/person/<uid>")
def get_person(uid):
    user = next((u for u in data if u["id"] == uid), None)
    if not user:
        return  {"message":"Person not found"},404
    return user, 200


@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_person(id):
    for person in data:
        if person["id"] == str(id):
            # Remove the person from the data list
            data.remove(person)
            # Return a JSON response with a message and HTTP status code 200 (OK)
            return {"message": "Person with ID deleted"}, 200
    # If no person with the given ID is found, return a JSON response with a message and HTTP status code 404 (Not Found)
    return {"message": "Person not found"}, 404

@app.route("/person", methods=['POST'])
def create_person():
    # Get the JSON data from the incoming request
    new_person = request.get_json()

    # Check if the JSON data is empty or None
    if not new_person:
        # Return a JSON response indicating that the request data is invalid
        # with a status code of 422 (Unprocessable Entity)
        return {"message": "Invalid input, no data provided"}, 422

    # Proceed with further processing of 'new_person', such as adding it to a database
    # or validating its contents before saving it

    # Assuming the processing is successful, return a success message with status code 200 (Created)
    return {"message": "Person created successfully"}, 200

@app.route("/data")
def get_data():
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return {"message": f"Data of length {len(data)} found"}
        else:
            # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404

# Define a route for the root URL ("/")
@app.route("/")
def index():
    # Function that handles requests to the root URL
    # Return a plain text response
    return "hello world"

@app.route("/no_content")
def no_content():
    return ({"message":"No content found"}),204

@app.route("/exp")
def index_explicit():
    return make_response({}, 200)

#curl -X GET -i localhost:5000/person/not-a-valid-uuid
# curl -X DELETE -i localhost:5000/person/66c09925-589a-43b6-9a5d-d1601cf53287

# curl -X POST -i -w '\n' \
#                    --url http://localhost:5000/person \
#                                           --header 'Content-Type: application/json' \
#                                                    --data '{
# "id": "4e1e61b4-8a27-11ed-a1eb-0242ac120002",
# "first_name": "John",
# "last_name": "Horne",
# "graduation_year": 2001,
# "address": "1 hill drive",
# "city": "Atlanta",
# "zip": "30339",
# "country": "United States",
# "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff"
# }'