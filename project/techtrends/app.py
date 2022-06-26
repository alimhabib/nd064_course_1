from http.client import OK
import logging 
import sqlite3 

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort


numberOfConnections = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global numberOfConnections 
    numberOfConnections = numberOfConnections + 1
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):    
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post
#Get total Count of posts    
def get_number_of_posts( ):    
    connection = get_db_connection()
    numberOFPosts = connection.execute('SELECT count(*) FROM posts').fetchone()
    connection.close()
    return numberOFPosts[0]

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():    
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info( f'this post not found -> {post_id}'  )
      return render_template('404.html'), 404
    else:
      app.logger.info('this post is retrieved '+ post['title'])
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('about page has been acceessed' )
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info('a new article is successfuly created with title'+ title)
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the healthz
@app.route('/healthz', methods=['GET'])
def health():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

@app.route('/metrics', methods=['GET'])
def metrics(): 
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"post_count":get_number_of_posts(),"db_connection_count":numberOfConnections}}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Metrics request successfull')
    return response
    
# start the application on port 3111
if __name__ == "__main__": 
   ## stream logs to a file
   logging.basicConfig(
    format='%(levelname)-8s : %(asctime)s  %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
   app.run(host='0.0.0.0', port='3111')
