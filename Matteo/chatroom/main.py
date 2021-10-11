from flask import Flask, render_template, abort, request, redirect
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

msgs = []

def getRoom(room):
    result = False
    for x in db.collection('rooms').stream():
        if(list(x.to_dict().values())[0] == room):
            result = True
            room_ref = db.collection('rooms').document(room)
            messages_ref = room_ref.collection('messages').limit(30).stream()
            for msg in messages_ref:
                msgs.append(msg.to_dict())
    return result

#list(x.to_dict().values())[0]

@app.route('/<roomid>')
def chatroomPage(roomid):
    msgs.clear()
    if getRoom(roomid) == True:
        return render_template('chat.html', room=roomid, listmsg=msgs)
    else:
        abort(404)


@app.route('/form')
def manageForm():
    argss = list(request.args.values())
    print(argss)
    db.collection('rooms').document(argss[0]).set({'name':argss[0]})
    if not argss[1]:
        db.collection('rooms').document(argss[0]).collection('messages').document().set({'from':'anonimo','msg':argss[2]})
    else:
        db.collection('rooms').document(argss[0]).collection('messages').document().set({'from':argss[1],'msg':argss[2]})
    return chatroomPage(argss[0])


if __name__ == '__main__':
    #uso porta 8910
    app.run(host='127.0.0.1', port=8910, debug=True)