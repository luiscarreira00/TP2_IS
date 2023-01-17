import sys

from flask import Flask
import json

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

import xmlrpc.client
print("connecting to server...")
string = "Cristiano Ronaldo"
with xmlrpc.client.ServerProxy("http://rpc-server:9000/") as proxy:
    print("teste dentro do cliente")
    print("3 is even: %s" % str(proxy.is_even(3)))
    print("100 is even: %s" % str(proxy.is_even(100)))



#@app.route('/api/selectplayer', methods=['GET'])
#def select_player():
#    x=server.selectPlayer(string)
#    y=json.load(x)
#    return [{
#        "Name": y["Name"],
#        "Age": y["Age"],
#        "Overall": y["Overall"],
#        "Nationality": y["Nationality"]

        #"id": "7674fe6a-6c8d-47b3-9a1f-18637771e23b",
        #"name": "Ronaldo",
        #"country": "Portugal",
        #"position": "Striker",
        #"imgUrl": "https://cdn-icons-png.flaticon.com/512/805/805401.png",
        #"number": 7
 #   }]


#if __name__ == '__main__':
#    app.run(host="0.0.0.0", port=PORT)
