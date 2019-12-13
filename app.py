import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'vegan_inspired'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-xvp8g.mongodb.net/vegan_inspired?retryWrites=true&w=majority'
mongo = PyMongo(app)


@app.route('/')
@app.route('/get_recips')
def get_recips():
    return render_template("recips.html", 
    recip=mongo.db.recip.find())

@app.route('/add_recip')
def add_recips():
     return render_template("addrecip.html",
                             categories=mongo.db.categories.find())

@app.route('/insert_recip', methods=['POST'])
def insert_recip():
    recip = mongo.db.recip
    recip.insert_one(request.form.to_dict())
    return render_template("recips.html", 
        recip=mongo.db.recip.find())
    

@app.route('/edit_recip/<recip_id>')
def edit_recip(recip_id):
    the_recip = mongo.db.recip.find_one({"_id": ObjectId(recip_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editrecip.html', recip=the_recip,
                           categories=all_categories)

@app.route('/update_recip/<recip_id>', methods=["POST"])
def update_recip(recip_id):
    recip = mongo.db.recip
    recip.update( {'_id': ObjectId(recip_id)},
    {
        'recip_name':request.form.get('recip_name'),
        'category_name':request.form.get('category_name'),
        'recip_description': request.form.get('recip_description'),
        'gluten_free':request.form.get('gluten_free')
    })
    #return redirect(url_for('get_recips'))
    return render_template("recips.html",
                recip=mongo.db.recip.find())

@app.route('/delete_recip/<recip_id>')
def delete_recip(recip_id):
    mongo.db.recip.remove({'_id': ObjectId(recip_id)})
    return redirect (url_for('get_recips'))

@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))

@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=(os.environ.get('PORT')),
            debug=True)

#if __name__ == '__main__':
#    app.run(host=os.environ.get('IP'),
#            port=(os.environ.get('PORT')),
#            debug=True)