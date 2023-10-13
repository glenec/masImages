
from flask import Flask, flash, session, jsonify, request, render_template,send_from_directory,redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_bcrypt import Bcrypt
import config


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.database_uri
app.secret_key = config.secret_key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    user = User()
    user.id = user_id
    return user

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = 'admin'
        password = request.form["password"]
        next_url = request.form["next"]
        if username == config.USERNAME and bcrypt.check_password_hash(config.PASSWORD, password):
            user = User()
            user.id = username
            login_user(user)
            session.permanent = True
            if next_url:
                return redirect(next_url)
            return redirect(url_for("index"))
        else:
            flash("Incorrect username or password!")
    return render_template("login.html")

@app.route('/')
@login_required
def index():
    return redirect(url_for("costco"))

@app.route('/costco')
@login_required
def costco():
    return render_template('searcher.html')

@app.route('/image/<path:filename>', methods=['GET'])
@login_required
def serve_image(filename):
    return send_from_directory(os.path.dirname(filename), os.path.basename(filename))

@app.route('/costco/search-part', methods=['GET'])
@login_required
def search_part():
    query = request.args.get('query')
    with db.engine.connect() as connection:
        results = connection.execute(
            text("SELECT p.part_number, p.description, i.image_path FROM product p, images i WHERE i.part_number = p.part_number AND p.part_number ILIKE :search_query || '%' ORDER BY p.part_number ASC").bindparams(search_query=query)
        ).fetchall()
    
    return jsonify([{
        'part_number': item[0],
        'description': item[1],
        'image': item[2]
    } for item in results])

@app.route('/costco/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    with db.engine.connect() as connection:
        terms = query.split()
        search_conditions = ' AND '.join([f"(p.description ILIKE '%%' || :term{i} || '%%')" for i, term in enumerate(terms)])
        sql = f"""
            SELECT p.part_number, p.description, i.image_path 
            FROM product p, images i 
            WHERE i.part_number = p.part_number 
            AND ({search_conditions})
            ORDER BY p.part_number ASC;
        """
        params = {f"term{i}": term for i, term in enumerate(terms)}
        results = connection.execute(text(sql).bindparams(**params)).fetchall()
    
    return jsonify([{
        'part_number': item[0],
        'description': item[1],
        'image': item[2]
    } for item in results])


@app.route('/amazon')
@login_required
def amazon():
    return render_template('amazon_searcher.html')

@app.route('/amazon/search-part', methods=['GET'])
@login_required
def amazon_search_part():
    query = request.args.get('query')
    with db.engine.connect() as connection:
        results = connection.execute(
            text("SELECT p.part_number, p.description, i.image_path FROM amazon_product p, amazon_images i WHERE i.part_number = p.part_number AND p.part_number ILIKE :search_query || '%' ORDER BY p.part_number ASC").bindparams(search_query=query)
        ).fetchall()
    
    return jsonify([{
        'part_number': item[0],
        'description': item[1],
        'image': item[2]
    } for item in results])

@app.route('/amazon/search', methods=['GET'])
@login_required
def amazon_search():
    query = request.args.get('query')
    with db.engine.connect() as connection:
        terms = query.split()
        search_conditions = ' AND '.join([f"(p.description ILIKE '%%' || :term{i} || '%%')" for i, term in enumerate(terms)])
        sql = f"""
            SELECT p.part_number, p.description, i.image_path 
            FROM amazon_product p, amazon_images i 
            WHERE i.part_number = p.part_number 
            AND ({search_conditions})
            ORDER BY p.part_number ASC
        """
        params = {f"term{i}": term for i, term in enumerate(terms)}
        results = connection.execute(text(sql).bindparams(**params)).fetchall()
    

    return jsonify([{
        'part_number': item[0],
        'description': item[1],
        'image': item[2]
    } for item in results])
