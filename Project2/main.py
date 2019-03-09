from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Inventory, Category

from flask import session as loginstate

import random
import string

app = Flask(__name__)
engine = create_engine('sqlite:///inventory.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def startpoint():
    return render_template('mainPage.html')


@app.route('/oAuth')
def oauthlogin():
    sessiontoken = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    loginstate['state'] = sessiontoken
    return render_template('loginPage.html', STATE=sessiontoken)


@app.route('/logOut')
def logout():
    return "logout page here"


@app.route('/test')
def reset():
    loginstate['state'] = 0
    return "Reset Login State. Please return to main page; token state:" \
           " %s" % loginstate['state']


@app.route('/state')
def status():
    return "State: Token: %s" % loginstate['state']

# Create Functions


@app.route('/addItemForm')
def additemform():
    categories = session.query(Category).all()
    numberentries = session.query(Category).count()
    categorienames = [0] * numberentries
    x = 0
    for row in categories:
        categorienames[x] = row.categoryName
        x += 1
    return render_template('newItem.html', categorieNames=categorienames,
                           numberEntries=numberentries)


@app.route('/makeItem', methods=['POST'])
def makenewitem():
    if request.method == 'POST':
        categoryname = request.form.getlist("allCategories")
        print(categoryname[0])
        queryresults = session.query(Category)\
            .filter(Category.categoryName == categoryname[0]).first()
        categoryid = queryresults.id
        newitem = Inventory(name=request.form['name'],
                            price=request.form['price'],
                            description=request.form['description'],
                            categoryID=categoryid,
                            quantity=request.form['quantity'])
        session.add(newitem)
        session.commit()
        return render_template('ItemMade.html')
    else:
        return "404"


@app.route('/addNewCategory')
def addnewcategoryform():
    return render_template('newCategory.html')


@app.route('/makeNewCategory', methods=['POST'])
def makenewcategory():
    if request.method == 'POST':
        newcategory = Category(categoryName=request.form['name'],
                               categoryDescript=request.form['categoryDescript'])
    else:
        return "404"
    session.add(newcategory)
    session.commit()
    return "new Category Added."


##############################################

# Read Operations


@app.route('/enter/Item')
def getallitemsbyname():
    array = session.query(Inventory).all()
    size = session.query(Inventory).count()
    itemnames = [0] * size
    itemid = [0] * size
    x = 0
    for name in array:
        itemnames[x] = name.name
        itemid[x] = name.id
        x += 1
    return render_template('searchByItem.html',
                           itemNames=itemnames, itemID=itemid, count=x)


@app.route('/enter/searchResult/<int:idInt>', methods=['GET'])
def getsingleiteminfo(idint):
    inventory_object = session.query(Inventory).get(idint)
    item_array = [0] * 6
    item_array[0] = inventory_object.name
    item_array[1] = inventory_object.price
    item_array[2] = inventory_object.description
    item_array[3] = inventory_object.quantity
    x = inventory_object.categoryID
    cat_name = session.query(Category).get(x)
    item_array[4] = cat_name.categoryName
    item_array[5] = inventory_object.id
    return render_template('ItemRead.html', ItemArray=item_array)


@app.route('/enter/searchResult/<int:idInt>/json')
def jsongetsingleitem(idint):
    invintory_object = session.query(Inventory).get(idint)
    return jsonify(Object=invintory_object.serialize)


@app.route('/enter/Category')
def getitemsbycategory():
    categories = session.query(Category).all()
    number_entries = session.query(Category).count()
    categorie_names = [0] * number_entries
    categorie_ids = [0] * number_entries
    categorie_descripts = [0] * number_entries
    x = 0
    for row in categories:
        categorie_names[x] = row.categoryName
        categorie_ids[x] = row.id
        x += 1
    return render_template('listAllCategories.html',
                           categorieNames=categorie_names,
                           numberEntries=number_entries,
                           categorieIDs=categorie_ids,
                           categorieDescripts=categorie_descripts)


@app.route('/enter/Item/getResults', methods=['POST'])
def rerurnsearchresults():
    return render_template('ItemSearchResults.html')


@app.route('/enter/searchCat/<int:idInt>')
def getitemfullinfo(idint):
    items = session.query(Inventory).filter(Inventory.categoryID == idint)
    number_entries = session.query(Category).count()
    ids = [0] * number_entries
    names = [0] * number_entries
    descriptions = [0] * number_entries
    # prices = session.query(Category).count()
    quantitys = [0] * number_entries
    # categoryIDs = [0] * number_entries
    x = 0
    for itemX in items:
        ids[x] = itemX.id
        names[x] = itemX.name
        descriptions[x] = itemX.description
        quantitys[x] = itemX.quantity
        x += 1

    return render_template('catSearch.html', ids=ids, names=names,
                           descriptions=descriptions,
                           quantitys=quantitys, count=x)


@app.route('/enter')
def databasemainpage():
    return render_template('mainDatabaseUsePoint.html')

##################################################################


# Update Functions
@app.route('/updateItem/<int:idInt>')
def updateitem(idint):
    update_item = session.query(Inventory).get(idint)
    categories = session.query(Category).all()
    number_entries = session.query(Category).count()
    category_names = [0] * number_entries
    x = 0
    for row in categories:
        category_names[x] = row.categoryName
        x += 1
    return render_template('updatePage.html', updateItem=update_item,
                           categorieNames=category_names,
                           numberEntries=number_entries)


@app.route('/itemUpdated', methods=['POST'])
def commitchanges():
    update_this_item = session.query(Inventory).get(request.form['ID'])
    update_this_item.name = request.form['name']
    update_this_item.price = request.form['price']
    update_this_item.description = request.form['description']
    update_this_item.quantity = request.form['quantity']
    session.add(update_this_item)
    session.commit()
    return "Updated Item"


@app.route('/enter/editCategory/<int:idInt>')
def editsinglecategory(idint):
    category = session.query(Category).get(idint)
    category_name = category.categoryName
    category_descript = category.categoryDescript
    cat_id = category.id
    return render_template('editCategory.html',
                           category=category,
                           categoryName=category_name,
                           categoryDescript=category_descript,
                           catID=cat_id)


@app.route('/enter/editCategory/commit', methods=['POST'])
def commitcatchange():
    category = session.query(Category).get(request.form['ID'])
    category.categoryName = request.form['name']
    category.categoryDescript = request.form['Descript']
    session.add(category)
    session.commit()
    return "Change Complete"


@app.route('/enter/editCategories')
def editcategorypage():
    categories = session.query(Category).all()
    number_entries = session.query(Category).count()
    categorie_names = [0] * number_entries
    categorie_ids = [0] * number_entries
    categorie_descripts = [0] * number_entries
    x = 0
    for categoryX in categories:
        categorie_names[x] = categoryX.categoryName
        categorie_ids[x] = categoryX.id
        categorie_descripts[x] = categoryX.categoryDescript
        x += 1

    return render_template('editCategories.html',
                           categorieNames=categorie_names,
                           categorieIDs=categorie_ids,
                           categorieDescripts=categorie_descripts,
                           count=x)

# end Update Functions

# Start Delete Functions


@app.route('/deleteItem/confircmDelete', methods=['DELETE', 'POST'])
def deletesingleitem():
    id_value = request.form['hidden']
    item_id = session.query(Inventory).get(id_value)
    session.delete(item_id)
    session.commit()
    return render_template('confirmDelete.html')


@app.route('/deleteItem/<int:idInt>')
def deleteitembyid(idint):
    itemtodelete = session.query(Inventory).get(idint)
    session.delete(itemtodelete)
    session.commit()
    return render_template('itemDeleted.html')


@app.route('/enter/deleteCategory/<int:idInt>')
def deletecategory(idint):
    categorytodelete = session.query(Category).get(idint)
    session.delete(categorytodelete)
    session.commit()
    return render_template('categoryDeleted.html')


# End Delete Functions


if __name__ == '__main__':
    app.secret_key = 'dummyKey'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
