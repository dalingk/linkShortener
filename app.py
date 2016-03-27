import bottle, datetime, random, string, re, mysql.connector, dateutil.parser, bcrypt, os, hmac

secret_file = "secret"
if not os.path.isfile(secret_file):
    f = open(secret_file, "wb")
    f.write(os.urandom(16))
    f.close()
f = open(secret_file, "rb")
cookie_secret = f.read()
f.close()
app = application = bottle.Bottle(catchall=True)

def getLinks():
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT name, url, tiny FROM links WHERE name != '' AND private=false ORDER BY createdTime desc;")
    l = c.fetchall()
    c.close()
    cnx.close()
    return l
def emailNotExists(email):
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT 1 FROM users WHERE email LIKE %s LIMIT 1;", (email,))
    c.fetchall()
    count = c.rowcount
    c.close()
    cnx.close()
    return count == 0
def createUser(email, password):
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    pwhash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    c.execute("INSERT INTO users (email, pwhash) VALUES (%s,%s)", (email, pwhash))
    cnx.commit()
    c.close()
    cnx.close()
def validLogon(email, password):
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT email, pwhash FROM users WHERE email=%s LIMIT 1;", (email,))
    user = c.fetchall()
    c.close()
    cnx.close()
    if len(user) == 1:
        pwtest = bcrypt.hashpw(password.encode("utf-8"), user[0][1].decode("utf-8").encode("utf-8")) == user[0][1].decode("utf-8").encode("utf-8")
        return pwtest
    else:
        return False
def loginUser(email):
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT PID FROM users WHERE email=%s;", (email,))
    pid = c.fetchone()[0]
    session = os.urandom(16)
    existing = True
    while existing:
        c.execute("SELECT SESSION FROM sessions WHERE SESSION=%s;", (session, ))
        c.fetchall()
        if c.rowcount == 0:
            existing = False
        else:
            session = os.urandom(16)
    c.execute("INSERT INTO sessions (PID, session) VALUES (%s,%s);", (pid, session))
    cnx.commit()
    c.close()
    cnx.close()
    bottle.response.set_cookie("session", session, secret=cookie_secret, max_age=15552000) #180 days
def logoutUser(pid, session):
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("DELETE FROM sessions WHERE PID=%s and session=%s", (pid, session))
    cnx.commit()
    c.close()
    cnx.close()
    bottle.response.set_cookie("session", "")

# Returns the user's pid or false if the user is not logged in
def getUserBySession():
    session = bottle.request.get_cookie("session", secret=cookie_secret)
    if session:
        cnx = mysql.connector.connect(option_files="mysql.cnf")
        c = cnx.cursor()
        c.execute("SELECT PID FROM sessions WHERE session=%s;", (session,));
        u = c.fetchall()
        if len(u) == 1:
            c.close()
            cnx.close()
            return u[0][0]
        c.close()
        cnx.close()
        bottle.response.set_cookie("session", "")
    return False
def getLinksByPID(PID):
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT name, url, tiny, private FROM links WHERE userid=%s ORDER BY createdTime desc;",(PID,))
    links = c.fetchall()
    c.close()
    cnx.close()
    return links
def getEmail(PID):
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT email FROM users WHERE PID=%s;",(PID,))
    emails = c.fetchall()
    c.close()
    cnx.close()
    return emails[0][0]
def genTiny():
    tinyLength = 6;
    tiny = "".join(random.SystemRandom().choice(string.ascii_letters + string.digits) for x in range(tinyLength))
    cnx = mysql.connector.connect(option_fles="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT tiny FROM links WHERE tiny = %s COLLATE utf8_bin;", (tiny,))
    rows = c.fetchall()
    c.close()
    cnx.close()
    if len(rows) > 0:
        tiny = genTiny()
    return tiny
def stats(l):
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT v.viewTime, v.viewIP FROM links l, views v WHERE l.tiny = v.tiny AND l.tiny = %s COLLATE utf8_bin ORDER BY v.viewTime DESC LIMIT 1;", (l[0][2],))
    s = c.fetchall()
    c.execute('SELECT count(tiny) FROM views WHERE tiny = %s COLLATE utf8_bin', (l[0][2],))
    numViews = c.fetchall()[0][0]
    c.close()
    cnx.close()
    stats = {
        'name': l[0][0],
        'url': l[0][1],
        'tiny': l[0][2],
        'numViews': numViews
    }
    PID = getUserBySession()
    if PID:
        stats['createdBy'] = l[0][3]
        stats['createdTime'] = timeFormat(dateutil.parser.parse(l[0][4]))
        stats['createdIP'] = l[0][5]
        stats['private'] = l[0][6]
    if numViews > 0:
        stats['lastView'] = timeFormat(dateutil.parser.parse(s[0][0]))
        stats['lastViewIP'] = s[0][1]
    return stats;

def timeFormat(t):
    delta = datetime.datetime.now() - t
    days = "{0}{1}".format(delta.days, " day" if delta.days == 1 else " days") if delta.days > 0 else ""
    hours = " {0}{1}".format(delta.seconds // 3600, " hour" if delta.seconds // 3600 == 1 else " hours") if delta.seconds // 3600 > 0 else ""
    minutes = " {0}{1}".format(delta.seconds % 3600 // 60, " minute" if delta.seconds % 3600 // 60 == 1 else " minutes") if delta.seconds % 3600 // 60 > 0 else ""
    seconds = " {0}{1}".format(delta.seconds % 60, " second" if delta.seconds % 60 == 1 else " seconds") if delta.seconds % 60 else ""
    return "{0}{1}{2}{3}".format(days, hours, minutes, seconds)

@app.route("/")
def index():
    links = getLinks()
    return bottle.template('links', title = "All Links", links=links)
@app.route("/l/<tiny>")
def index(tiny):
    pid = getUserBySession()
    if not pid:
        pid = 0
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT name, url, tiny, createdTime, createdIP FROM links WHERE tiny=%s COLLATE utf8_bin;", (tiny,))
    l = c.fetchall()
    if len(l) > 0:
        c.execute('INSERT INTO views (viewTime, viewIP, tiny, pid) VALUES (%s,%s,%s,%s);', (datetime.datetime.now().isoformat(),bottle.request.remote_addr, l[0][2], pid))
        cnx.commit()
        c.close()
        cnx.close()
        bottle.response.status = 302
        bottle.response.set_header("Location", l[0][1])
        return bottle.template("links", title="Links", links=l)
    c.close()
    cnx.close()
    return bottle.templates('links', title="Not Found", error="That links was not found.")

@app.route("/stats/<tiny>")
def index(tiny):
    cnx = mysql.connector.connect(option_files="mysql.cnf")
    c = cnx.cursor()
    c.execute("SELECT name, url, tiny, users.email, createdTime, createdIP, private, userid FROM links, users WHERE tiny=%s COLLATE utf8_bin AND userid = users.PID;", (tiny,))
    l = c.fetchall()
    c.close()
    cnx.close()
    if len(l) > 0:
        if l[0][6] == 0 or l[0][7] == getUserBySession():
            return bottle.template('links', title="Stats for {}".format(tiny), stats=stats(l))
        else:
            return bottle.template('links', title="Private link", error="This link is private.")
    else:
        return bottle.template('links', title="Unknown link", error="That link wasn't found.")


@app.get("/new")
def new():
    PID = getUserBySession()
    if PID:
        return bottle.template('new', title = "New Link", custom = bottle.request.query.get("custom"))
    else:
        bottle.redirect("/login")
        return "Please login before submitting a link"
@app.post("/new")
def add():
    PID = getUserBySession()
    if PID:
        email = getEmail(PID)
        url_re = re.compile('^(http[s]*(?::\/\/))')
        url = bottle.request.forms.get('url')
        url = ('' if url_re.match(url) else 'http://') + url
        userIP = bottle.request.remote_addr
        name = bottle.request.forms.get('name')
        tiny = genTiny()
        private = 1 if bottle.request.forms.get('private') else 0
        cnx = mysql.connector.connect(option_files="mysql.cnf")
        c = cnx.cursor()
        c.execute('INSERT INTO links (url, createdTime, createdIP, tiny, name, userid, private) VALUES (%s,%s,%s,%s,%s,%s,%s);', (url, datetime.datetime.now().isoformat(), userIP, tiny, name, PID, private))
        cnx.commit()
        bottle.TEMPLATES.clear()
        c.close()
        cnx.close()
        bottle.redirect("/stats/{}".format(tiny))
        return "url: %s, user %s, tiny %s" % (url, user, tiny)
    else:
        bottle.redirect("/login")
        return "Please login before submitting a link"

@app.get("/register")
def showRegisterPage():
    if getUserBySession():
        bottle.redirect("/user")
    return bottle.template('register', title = "Register")
@app.post("/register")
def register():
    email = bottle.request.forms.get("email") or ""
    password = bottle.request.forms.get("password")
    confirm = bottle.request.forms.get("confirm")
    if email and len(email) > 5 and len(email) < 256:
        if emailNotExists(email):
            if len(password) > 5 and password == confirm:
                createUser(email, password);
                loginUser(email)
                return bottle.template('register', title="Registration Complete", email = email)
            else:
                error = "Please verify your password contains 6 characters and was typed correctly."
        else:
            error = "Please choose a different email address."
    else:
        email = ""
        error = "Your email was not long enough."
    return bottle.template('register', title = "Registration Error", email = email, error=error)

@app.get("/login")
def showLoginPage():
    if getUserBySession():
        bottle.redirect("/user")
    return bottle.template('login', title = "Login")
@app.post("/login")
def login():
    if getUserBySession():
        bottle.redirect("/user")
        return
    email = bottle.request.forms.get("email")
    password = bottle.request.forms.get("password")
    if email and password and validLogon(email, password):
        loginUser(email)
        bottle.redirect("/user")
    else:
        bcrypt.hashpw("abcdefghijklmnopqrstuvwxyz".encode("utf-8"), bcrypt.gensalt())
        return bottle.template('login', title="Login", error="Incorrect email or password.")
    return "Submitting login request"
@app.route("/logout")
def logout():
    userpid = getUserBySession()
    session = bottle.request.get_cookie("session", secret=cookie_secret)
    if userpid and session:
        logoutUser(userpid, session)
    bottle.redirect("/")

@app.get("/user")
def user():
    userpid = getUserBySession()
    if userpid:
        email = getEmail(userpid)
        links = getLinksByPID(userpid)
        return bottle.template("links", title = "Links for {}".format(email), links = links)
    else:
        bottle.redirect("/login")
    return bottle.template("links", title="Not logged in", error="You must be logged in to view links you have submitted.")

if __name__ == "__main__":
    @app.route("/<filename>")
    def static(filename):
        return bottle.static_file(filename, root="/home/kyle/repos/links")
    bottle.run(app, host='0.0.0.0', port=8080, debug=True, reloader=True)
