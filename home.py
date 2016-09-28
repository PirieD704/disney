from flask import Flask, render_template, request, redirect, session
from flaskext.mysql import MySQL

app = Flask(__name__)
#create an instance of the mysql class
mysql = MySQL()
#add to the app (Flask object) some config data for our connection
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
#The name of the database we want to connect to at the DB server
app.config['MYSQL_DATABASE_DB'] = 'disney'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
# user the mysql object's method "init_app" and pass it the flask object
mysql.init_app(app)

app.secret_key = "HAOEA2342352LKT3049203ytO4htr130JSasdKLF239"

@app.route('/')
def index():
	#set up a cursor object which is what the sql object uses to connect and run queries
	cursor = mysql.connect().cursor()
	#execute our query
	cursor.execute("SELECT content FROM page_content WHERE page='home' AND location='header' AND status='1'")
	header_text = cursor.fetchall()
	print header_text
	cursor2 = mysql.connect().cursor()
	#execute our query
	cursor2.execute("SELECT content, header_text, image_link FROM page_content WHERE page='home' AND location='body' AND status='1'")
	body_stuff = cursor2.fetchall()
	print header_text
	return render_template('index.html',
		header_text = header_text, data = body_stuff)



# Make a new route called admin
@app.route('/admin')
# define the method for the new route admin
def admin():
	# return render_template('admin.html')
	# get the variable "message" out of the query string if it exists...
	if request.args.get('message'):
		# return the template 
		return render_template('admin.html',
	 	message = "Login Failed")
	else:
		return render_template('admin.html')

# Make a new route called admin_submit. Add method POST so that the form can get here.
@app.route('/admin_submit', methods=['GET', 'POST'])
# define new route for the admin_submit
def admin_submit():
	print request.form
	# return request.form['username'] + ' ---- ' + request.form['password']
	if request.form['username'] == 'admin' and request.form['password'] == 'admin':
		#You may proceed
		#But before you do.. let me give you a ticket!
		session['username'] = request.form['username']
		return redirect('/admin_portal')
	else:
		return redirect('/admin?message=login_failed')

@app.route('/admin_portal')
def admin_portal():
	#session variable 'username' exists... proceed
	if 'username' in session:
		return render_template('admin_portal.html')
	# you have no ticket. no soup for you
	else:
		return redirect('/admin?message=You_Must_Log_In')

@app.route('/admin_update', methods=['POST'])
def admin_update():
	# First, do you belong here?
	if 'username' in session:
		# ok, they are logged in. i will insert your stuff...
		body = request.form['body_text']
		header = request.form['header']
		image = request.form['image']
		cursor = mysql.connect().cursor()
		query = "INSERT INTO page_content VALUES (DEFAULT, 'home', '"+body+"',1,1,'left_block', NULL, '"+header+"', '"+image+"')"
		print query
		cursor.execute(query)
		return redirect('/admin_portal?success=Added')

	# you have no ticket. no soup for you
	else:
		return redirect('/admin?message=You_Must_Log_In')


if __name__ == "__main__":
	app.run(debug=True)












