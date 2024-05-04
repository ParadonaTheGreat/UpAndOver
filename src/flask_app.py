from flask import Flask, request,render_template, redirect, url_for
import time
app = Flask(__name__)

roomStates = {}

@app.route('/', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("loginscreen.html")
    if request.method == 'POST':
        roomStates[request.form['code'] + "left"] = False
        if request.form['code']+"numPeople" in roomStates.keys() and roomStates[request.form['code']+"numPeople"] == roomStates[request.form['code']+"maxPpl"] :
            return redirect(url_for('login'))
        if request.form['code']+"numPeople" not in roomStates.keys():
            roomStates[request.form['code']+"numPeople"] = 1
        else:
            roomStates[request.form['code']+"numPeople"] +=1
        if roomStates[request.form['code']+"numPeople"] > 1:
            return redirect(url_for('game', maxNum = roomStates[request.form['code']+"maxNum"], maxPpl = roomStates[request.form['code']+"maxPpl"], code = request.form['code'], user = request.form['userid']))
        else:
            return redirect(url_for('settings', code = request.form['code'], user = request.form['userid']))

@app.route('/<code>/<user>/settings', methods = ['GET','POST'])
def settings(code, user):
    if request.method == 'GET':
        return render_template("settings.html", code = code, user = user)
    if request.method == 'POST':
        roomStates[code+"maxNum"] = request.form['maxNum']
        roomStates[code+"maxPpl"] = request.form['maxPpl']
        return redirect(url_for('game', maxNum = roomStates[code+"maxNum"], maxPpl = roomStates[code+"maxPpl"], code = code, user = user))


@app.route('/<maxNum>/<maxPpl>/<code>/<user>', methods = ['GET','POST'])
def game(maxNum, maxPpl, code, user):
    try:
        if code+"gamenumber" not in roomStates.keys():
            roomStates[code+"gamenumber"] = 0
            roomStates[code+"turn"] = 0

        if roomStates[code+"numPeople"] == 1:
            roomStates[code+"player" + user] = user
            roomStates[code+"players"] = [user]

        if roomStates[code+"numPeople"] >= 2 and user not in roomStates[code+"players"]:
            roomStates[code+"player" + user] = user
            roomStates[code+"players"].append(user)

        if request.method == 'GET':
            if roomStates[code + "left"] == True:
                return redirect(url_for('gameover',code=code))
            if roomStates[code+"gamenumber"] >= int(maxNum):
                return redirect(url_for('gameover',code=code))
            if roomStates[code+"numPeople"] > 1 and roomStates[code+"players"][roomStates[code+"turn"]] != user:
                return render_template("buttonsDisabled.html", maxNum = maxNum, maxPpl = maxPpl, turn=roomStates[code+"players"][roomStates[code+"turn"]], gamenumber=roomStates[code+"gamenumber"], user = user, code = code, dicto = roomStates)
            return render_template("countto30template.html", maxNum = maxNum, maxPpl = maxPpl, turn=roomStates[code+"players"][roomStates[code+"turn"]], gamenumber=roomStates[code+"gamenumber"], user = user, code = code, dicto = roomStates)

        if request.method == 'POST':
            if request.form['button'] == "leaveButton":
                roomStates[code + "left"] = True
                roomStates[code+"players"][roomStates[code+"turn"]] = "Nobody"
                time.sleep(5.1)
                return redirect(url_for('gameover',code=code))

            if int(roomStates[code+"numPeople"])<int(maxPpl):
                return redirect(url_for('game', maxNum = maxNum, maxPpl = maxPpl, code = code, user = user))

            else:
                if request.form['button'] == "submitButton":
                    if roomStates[code+"gamenumber"] <int(maxNum):
                        num_choice = request.form['number_choice']
                        roomStates[code+"gamenumber"] = roomStates[code+"gamenumber"]+int(num_choice)
                    if roomStates[code+"gamenumber"] >= int(maxNum):
                        return redirect(url_for('gameover',code=code))
                    if roomStates[code+"turn"] != int(maxPpl)-1:
                        roomStates[code+"turn"] +=1
                    else:
                        roomStates[code+"turn"] = 0

                    if roomStates[code+"gamenumber"] >= int(maxNum):
                        return redirect(url_for('gameover',code=code))

                    if roomStates[code+"numPeople"] > 1 and roomStates[code+"players"][roomStates[code+"turn"]] != user:
                        return render_template("buttonsDisabled.html", maxNum = maxNum, maxPpl = maxPpl, turn=roomStates[code+"players"][roomStates[code+"turn"]], gamenumber=roomStates[code+"gamenumber"], user = user, code = code, dicto = roomStates)
                    return render_template("countto30template.html", maxNum = maxNum, maxPpl = maxPpl, turn=roomStates[code+"players"][roomStates[code+"turn"]], gamenumber=roomStates[code+"gamenumber"], user = user, code = code, dicto = roomStates)
    except Exception as e:
        return redirect(url_for('login'))
        #return str(e) + roomStates + "hello world"

@app.route('/<code>/end', methods = ['GET','POST'])
def gameover(code):
    if request.method == 'GET':
        return render_template("game_over.html",code = code, loser = roomStates[code+"players"][roomStates[code+"turn"]])
    if request.method == 'POST':
        try:
            for i in range (len(list(roomStates.keys()))-1,-1,-1):
                if code in list(roomStates.keys())[i]:
                    roomStates.pop(list(roomStates.keys())[i])
        except Exception as e:
            return redirect(url_for('login'))
        finally:
            return redirect(url_for('login'))


if __name__ == '__main__':
  app.run(debug = True)
