from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
from string import ascii_uppercase
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
socketio = SocketIO(app)

# Constants
ROOM_CODE_LENGTH = 4
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 20
MIN_PASSWORD_LENGTH = 6
MAX_MESSAGE_LENGTH = 500

rooms = {}
users = {}
PROFILE_PICS = [
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#4A90E2"/></svg>',
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#50C878"/></svg>',
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#FF6B6B"/></svg>',
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#9B59B6"/></svg>',
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#F39C12"/></svg>',
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#1ABC9C"/></svg>',
]

# Helper Functions
def validate_username(username):
    """Validate username meets requirements"""
    if not username:
        return False, "Username is required."
    if len(username) < MIN_USERNAME_LENGTH:
        return False, f"Username must be at least {MIN_USERNAME_LENGTH} characters."
    if len(username) > MAX_USERNAME_LENGTH:
        return False, f"Username must be less than {MAX_USERNAME_LENGTH} characters."
    if not username.replace("_", "").replace("-", "").isalnum():
        return False, "Username can only contain letters, numbers, hyphens, and underscores."
    return True, None

def validate_password(password):
    """Validate password meets requirements"""
    if not password:
        return False, "Password is required."
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    return True, None

def validate_message(message):
    """Validate message meets requirements"""
    if not message or not message.strip():
        return False, "Message cannot be empty."
    if len(message) > MAX_MESSAGE_LENGTH:
        return False, f"Message must be less than {MAX_MESSAGE_LENGTH} characters."
    return True, None

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

def cleanup_empty_room(room_code):
    """Delete room if empty after a delay"""
    socketio.sleep(5)
    if room_code in rooms and rooms[room_code]["members"] <= 0:
        print(f"Deleting empty room {room_code} after delay.")
        del rooms[room_code]

@app.route("/", methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")

        if not name or not password:
            return render_template("login.html", error="Please enter a username and password.", name=name)

        if name not in users:
            return render_template("login.html", error="Invalid username or password.", name=name)
        
        if not check_password_hash(users[name]["password"], password):
            return render_template("login.html", error="Invalid username or password.", name=name)

        session["name"] = name
        return redirect(url_for("lounge"))

    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")

        # Validate username
        valid_username, username_error = validate_username(name)
        if not valid_username:
            return render_template("signup.html", error=username_error, name=name)

        # Validate password
        valid_password, password_error = validate_password(password)
        if not valid_password:
            return render_template("signup.html", error=password_error, name=name)

        if name in users:
            return render_template("signup.html", error="Username already taken.", name=name)

        # Hash password before storing
        hashed_password = generate_password_hash(password)
        users[name] = {"password": hashed_password, "profile_pic": random.choice(PROFILE_PICS)}
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/lounge", methods=["POST", "GET"])
def lounge():
    name = session.get("name")
    if not name:
        return redirect(url_for("login"))

    if request.method == "POST":
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if join != False and not code:
            return render_template("lounge.html", error="Please enter a room code.", user=users.get(name))

        room = code
        if create != False:
            room = generate_unique_code(ROOM_CODE_LENGTH)
            rooms[room] = {"members": 0, "messages": [], "names": set()}
        elif code not in rooms:
            return render_template("lounge.html", error="Room does not exist.", user=users.get(name))

        session["room"] = room
        return redirect(url_for("room"))

    return render_template("lounge.html", user=users.get(name))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/account", methods=["GET", "POST"])
def account():
    if "name" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = session["name"]
        pic_index = int(request.form.get("profile_pic"))
        if 0 <= pic_index < len(PROFILE_PICS):
            users[name]["profile_pic"] = PROFILE_PICS[pic_index]
        return redirect(url_for("account"))

    return render_template("account.html", users=users, profile_pics=PROFILE_PICS)

@app.route("/room")
def room():
    if "name" not in session or "room" not in session or session["room"] not in rooms:
        return redirect(url_for("lounge"))

    room_code = session.get("room")
    return render_template("room.html", code=room_code, messages=rooms[room_code]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    name = session.get("name")
    if room not in rooms or name not in users:
        return
    
    msg_content = data.get("data", "")
    
    # Validate message
    valid_msg, msg_error = validate_message(msg_content)
    if not valid_msg:
        send({"error": msg_error}, to=request.sid)
        return

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    content = {
        "name": name,
        "message": msg_content,
        "time": current_time,
        "profile_pic": users[name]["profile_pic"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {msg_content}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name or name not in users:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    if name in rooms[room]["names"]:
        return False

    join_room(room)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    send({"name": name, "message": "has entered the room", "time": current_time, "profile_pic": users[name]["profile_pic"]}, to=room)
    rooms[room]["members"] += 1
    rooms[room]["names"].add(name)
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")

    if not room or not name or name not in users:
        return

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        rooms[room]["names"].discard(name)
        if rooms[room]["members"] <= 0:
            socketio.start_background_task(cleanup_empty_room, room)
    
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    send({"name": name, "message": "has left the room", "time": current_time, "profile_pic": users[name]["profile_pic"]}, to=room)
    print(f"{name} has left the room {room}")


@socketio.on("leave")
def leave(data):
    room = session.get("room")
    name = session.get("name")

    if not room or not name or name not in users:
        session.clear()
        return

    leave_room(room)
    profile_pic = users[name]["profile_pic"] # Get pic before clearing session

    if room in rooms:
        rooms[room]["members"] -= 1
        rooms[room]["names"].discard(name)
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    send({"name": name, "message": "has left the room", "time": current_time, "profile_pic": profile_pic}, to=room)
    print(f"{name} has left the room {room}")
    session.clear()

if __name__ == "__main__":
    socketio.run(app, debug=True)
