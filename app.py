from flask import Flask, jsonify, request, render_template,send_from_directory
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:passwordHERE@localhost:5432/postgres"
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('searcher.html')

@app.route('/image/<path:filename>', methods=['GET'])
def serve_image(filename):
    print(f"Trying to serve: {filename}")
    return send_from_directory(os.path.dirname(filename), os.path.basename(filename))


@app.route('/search-part', methods=['GET'])
def search_part():
    query = request.args.get('query')
    with db.engine.connect() as connection:
        results = connection.execute(
            text("SELECT p.part_number, p.description, i.image_path FROM product p, images i WHERE i.part_number = p.part_number AND p.part_number ILIKE :search_query || '%'").bindparams(search_query=query)
        ).fetchall()
    
    return jsonify([{
        'part_number': item[0],
        'description': item[1],
        'image': item[2]
    } for item in results])


@app.route('/search', methods=['GET'])
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
        """
        params = {f"term{i}": term for i, term in enumerate(terms)}
        results = connection.execute(text(sql).bindparams(**params)).fetchall()

    return jsonify([{
        'part_number': item[0],
        'description': item[1],
        'image': item[2]
    } for item in results])



