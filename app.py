from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt, datetime

SECRET_KEY = 'mayIwinthisInternship'

app = Flask(__name__)
CORS(app)

users = [
    {
        "userName": "prtyksh",
        "passwd": "1234"
    },
    {
        "userName": "prtyksh2",
        "passwd": "1234"
    }
]

slots = [
    {"timings": "10:00 AM - 11:00 AM", "booked": None},
    {"timings": "11:00 AM - 12:00 PM", "booked": None},
    {"timings": "12:00 PM - 01:00 PM", "booked": None},
    {"timings": "01:00 PM - 02:00 PM", "booked": None},
    {"timings": "02:00 PM - 03:00 PM", "booked": None},
    {"timings": "03:00 PM - 04:00 PM", "booked": None},
    {"timings": "04:00 PM - 05:00 PM", "booked": None},
    {"timings": "05:00 PM - 06:00 PM", "booked": None}
]


def verify_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, 'Missing token'

    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded['userName'], None
    except jwt.ExpiredSignatureError:
        return None, 'Token expired'
    except jwt.InvalidTokenError:
        return None, 'Invalid token'



@app.route('/slots')
def slotsFunc():
    return jsonify(slots)

@app.route("/book", methods=['POST'] )
def bookFunc():
    userName, error = verify_token(request)
    if error:
        return jsonify([500])
    
    data = request.get_json()
    slot = data.get("timeSlot")

    for oneSlot in slots:
        if oneSlot['timings'] == slot:
            oneSlot['booked'] = userName
            break
    
    return jsonify([200])

@app.route("/cancel", methods=['POST'] )
def cancelFunc():
    userName, error = verify_token(request)
    if error:
        return jsonify([500])
    
    data = request.get_json()
    slot = data.get("timeSlot")

    for oneSlot in slots:
        if oneSlot['timings'] == slot:
            if oneSlot['booked'] == userName:
                oneSlot['booked'] = None
                break
            else:
               return jsonify([401])
        
    
    return jsonify([200])


@app.route("/login", methods=['POST'] )
def loginFunc():
    data = request.get_json()
    userName = data.get("userName")
    passwd = data.get("passwd")


    for user in users:
        if (user['userName'] == userName):
            found = True
            if(user['passwd'] == passwd):
                token = jwt.encode({
                    'userName': userName,
                    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
                }, SECRET_KEY, algorithm='HS256')
                return jsonify({"token": token})
            else:
                return jsonify([500])
            
    
    users.append({
        "userName": userName,
        "passwd": passwd
    })
    token = jwt.encode({
        'userName': userName,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')
    return jsonify({"token": token})

 

if __name__ == '__main__':
    app.run(debug=True)
