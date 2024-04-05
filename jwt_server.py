from flask import Flask, request, jsonify
import jwt
import argparse

app = Flask(__name__)

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="JWT Server")
parser.add_argument("--check-signature", action="store_true", help="Enable JWT signature checks")
parser.add_argument("--secret-key", default="YOUR_SECRET_KEY", help="Secret key for signing and verifying JWTs")
parser.add_argument("--port", type=int, default=5000, help="Port on which to run the Flask server")

args = parser.parse_args()

# Set the secret key from the command-line argument
SECRET_KEY = args.secret_key


@app.route("/generate-jwt", methods=["POST"])
def generate_jwt():
    data = request.get_json()
    payload = {}
    for key, value in data.items():
        payload[key] = value
    # Generate a JWT and encode it using the HS256 algorithm.
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"jwt_token": jwt_token})

# @app.route("/handle-jwt", methods=["POST"])
# def handle_jwt():
#     data = request.get_json()
#     jwt_token = data["jwt_token"]
#     # Decode the JWT and verify its signature.
#     try:
#         payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
#         # Process the JWT payload.
#         # ...
#         return jsonify({"success": True})
#     except jwt.InvalidTokenError:
#         return jsonify({"success": False, "message": "Invalid token"}), 401

@app.route("/check-jwt", methods=["POST"])
def check_jwt():
    # Check if the request contains a JWT in the Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header:
        parts = auth_header.split(" ")
        # Ensure the Authorization header is properly formatted with the "Bearer" keyword followed by the token
        if len(parts) == 2 and parts[0].lower() == "bearer":
            jwt_token = parts[1]
            try:
                if args.check_signature:
                    # Decode the JWT and verify its signature
                    payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
                else:
                    # Decode the JWT without verifying its signature
                    payload = jwt.decode(jwt_token, None, options={"verify_signature": False})
                # Process the JWT payload
                # ...
                return jsonify({"success": True, "payload": payload})
            except jwt.InvalidTokenError:
                return jsonify({"success": False, "error": "Invalid JWT"}), 400
            except jwt.ExpiredSignatureError:
                return jsonify({"success": False, "error": "Expired JWT"}), 400
            except jwt.InvalidSignatureError:
                return jsonify({"success": False, "error": "Invalid JWT signature"}), 400
        else:
            # Authorization header is not in the expected format
            return jsonify({"success": False, "error": "Malformed Authorization header"}), 400
    else:
        return jsonify({"success": False, "error": "Missing JWT"}), 400

@app.route("/handle-jwt", methods=["POST"])
def handle_jwt():
    # Check if the request contains a JWT in the Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header:
        parts = auth_header.split(" ")
        # Ensure the Authorization header is properly formatted with the "Bearer" keyword followed by the token
        if len(parts) == 2 and parts[0].lower() == "bearer":
            jwt_token = parts[1]
            try:
                # header = jwt.get_unverified_header(jwt_token)
                # alg = header['alg']
                if args.check_signature:
                    # This also makes the application vulnerable by using the algorithm specified in the JWT without validation.
                    payload = jwt.decode(jwt_token, SECRET_KEY)
                else:
                    # Simulate accepting 'none' as a valid algorithm, making it vulnerable.
                    payload = jwt.decode(jwt_token, None, options={"verify_signature": False})
                return jsonify({"success": True, "payload": payload})
            except jwt.InvalidTokenError:
                return jsonify({"success": False, "error": "Invalid JWT"}), 400
            except jwt.ExpiredSignatureError:
                return jsonify({"success": False, "error": "Expired JWT"}), 400
            except jwt.InvalidSignatureError:
                return jsonify({"success": False, "error": "Invalid JWT signature"}), 400
        else:
            # Authorization header is not in the expected format
            return jsonify({"success": False, "error": "Malformed Authorization header"}), 400
    else:
        return jsonify({"success": False, "error": "Missing JWT why"}), 400

def print_example_curl_commands():
    # Bold White for the descriptions
    bold_white = "\033[1;37m"
    # Yellow for the commands
    yellow = "\033[0;33m"
    # Reset to default terminal color
    reset = "\033[0m"

    print(f'{bold_white}\nExample curl commands:{reset}')
    print(f'{bold_white}Generate JWT:{reset}')
    print(f'{yellow}\tcurl -X POST -H "Content-Type: application/json" -d \'{{"username": "sho_luv", "website": "sholuv.net"}}\' http://localhost:{args.port}/generate-jwt{reset}')
    print(f'{bold_white}Handle JWT:{reset}')
    print(f'{yellow}\tcurl -X POST -H "Content-Type: application/json" -d \'{{"jwt_token": "YOUR_JWT_TOKEN"}}\' http://localhost:{args.port}/handle-jwt{reset}')
    print(f'{bold_white}Check JWT:{reset}')
    print(f'{yellow}\tcurl -X POST -H "Authorization: Bearer YOUR_JWT_TOKEN" -H "Content-Type: application/json" http://localhost:{args.port}/check-jwt{reset}\n')


if __name__ == "__main__":
    
    print_example_curl_commands()

    app.run(debug=False, port=args.port)