from flask import Flask, request, jsonify
import jwt
import argparse

app = Flask(__name__)

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="JWT Server")
parser.add_argument("--check-signature", action="store_true", help="Enable JWT signature checks")
parser.add_argument("--secret-key", default="YOUR_SECRET_KEY", help="Secret key for signing and verifying JWTs")
args = parser.parse_args()

# Set the secret key from the command-line argument
SECRET_KEY = args.secret_key

@app.route("/generate-jwt", methods=["POST"])
def generate_jwt():
    data = request.get_json()
    payload = {
        "username": data["username"],
        "email": data["email"],
    }
    # Generate a JWT and encode it using the HS256 algorithm.
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"jwt_token": jwt_token})

@app.route("/handle-jwt", methods=["POST"])
def handle_jwt():
    data = request.get_json()
    jwt_token = data["jwt_token"]
    # Decode the JWT without verifying its signature.
    payload = jwt.decode(jwt_token, SECRET_KEY, verify=False)
    # Process the JWT payload.
    # ...
    return jsonify({"success": True})

@app.route("/check-jwt", methods=["POST"])
def check_jwt():
    # Check if the request contains a JWT in the Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header:
        # Extract the JWT from the Authorization header
        jwt_token = auth_header.split(" ")[1]
        try:
            if args.check_signature:
                # Decode the JWT and verify its signature
                payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
            else:
                # Decode the JWT without verifying its signature
                payload = jwt.decode(jwt_token, options={"verify_signature": False})
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
        return jsonify({"success": False, "error": "Missing JWT"}), 400

if __name__ == "__main__":
    app.run(debug=True)
