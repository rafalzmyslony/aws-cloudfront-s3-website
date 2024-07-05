from flask import Flask, request, abort, jsonify

app = Flask(__name__)

'''
status code 401 + response.headers['Www-Authenticate']   creates prompt to type login and password
'''

@app.route("/test")
def unauthorized():
  """Returns a 401 Unauthorized response for the /test endpoint."""
#   return abort(401)  # Raise abort with status code 401
  return 'test', 401  # Raise abort with status code 401


@app.route("/test2")
def with_custom_header():
  """Returns a response with a custom header."""
  response = jsonify({"message": "This is a test response"})
  response.headers['Www-Authenticate'] = 'Basic realm="Enter credentials for this super secure site'
  return response, 401

@app.route("/basic")
def with_custom_header2():
  # test:test  --> dGVzdDp0ZXN0   (base64) !!!! Cg==
  """Returns a response with a custom header."""
  print(request.headers)
  if 'Authorization' in request.headers and request.headers['Authorization'] == 'Basic dGVzdDp0ZXN0':
    return 'success', 200
  response = jsonify({"message": "This is a test response"})
  response.headers['Www-Authenticate'] = 'Basic realm="Enter credentials for this super secure site'

  return response, 401

if __name__ == "__main__":
  app.run(debug=True)
