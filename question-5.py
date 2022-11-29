from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from countries import ISO3166
import hashlib

LOGIN_DATABASE = "login.txt"
PASSWORD_DATABASE = "passwords.txt"
country_dict = {v.lower(): k for k, v in ISO3166.items()}

class Handler(BaseHTTPRequestHandler):
    def authenticate(self,login,password,location):
        print("authenticate called")
        login = login.lower()
        location = location.lower()
        # 1. Check login if login has correct ID with country code
        code = country_dict[location]
        if not (login[0:2] == code.lower() or login[0:2] == code.upper() or login[0:2] == code):
            self.send_response(400)
            self.send_header('content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes('bad request, country code error', "utf-8"))
            return
        # 2. Check login if login already exists
        with open(LOGIN_DATABASE) as f:
            login_data = f.read().splitlines()
        if login not in login_data:
            self.send_response(403)
            self.send_header('content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes('Not found, user doesnt exist', "utf-8"))
            return
        # 3. Check if passwords exist
        salt = '5gz'
        db_password = password + salt
        hashed_code = hashlib.md5(db_password.encode())
        hashed_pw = hashed_code.hexdigest()
        with open(PASSWORD_DATABASE) as f:
            pw_data = f.read().splitlines()
        if hashed_pw not in pw_data:
            self.send_response(403)
            self.send_header('content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes('Not found, user doesnt exists', "utf-8"))
            return
        self.send_response(200)
        self.send_header('content-type','application/json')
        self.end_headers()
        self.wfile.write(bytes('Successful login!', "utf-8"))
        return

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        self.wfile.write('Welcome to authentication!'.encode())

    def do_POST(self):
        # Getting the content
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        data = json.loads(post_data.decode('utf-8'))
        self.authenticate(data['login'],data['password'],data['location'])


def main():
    PORT = 8080
    server = HTTPServer(('', PORT), Handler)
    print('Server running on port', PORT)
    server.serve_forever()
    server.server_close()

if __name__ == "__main__":
    main()