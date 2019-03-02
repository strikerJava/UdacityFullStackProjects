from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Inventory, Category

from flask import session as loginState #login sesson object

import random, string, array

app = Flask(__name__)
engine = create_engine('sqlite:///inventory.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def startPoint():
    return render_template('mainPage.html')

@app.route('/oAuth')
def oAuthLogIn():
    sessionToken = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    loginState['state'] = sessionToken
    return render_template('loginPage.html', STATE=sessionToken)


@app.route('/logOut')
def logout():
    return "logout page here"

@app.route('/test')
def reset():
    loginState['state'] = 0
    return "Reset Login State. Please return to main page; token state: %s" %loginState['state']

@app.route('/state')
def status():
    return "State: Token: %s" %loginState['state']

#################Create Functions#################

@app.route('/addItemForm')
def addItemForm():
    categories = session.query(Category).all()
    numberEntries = session.query(Category).count()
    categorieNames = [0] * numberEntries
    x = 0
    for row in categories:
        categorieNames[x] = row.categoryName
        x += 1
    return render_template('newItem.html', categorieNames=categorieNames, numberEntries=numberEntries)

@app.route('/makeItem', methods = ['POST'])
def makeNewItem():
    if request.method == 'POST':
        newItem = Inventory(name = request.form['name'], price = request.form['price'], description = request.form['description'], categoryID = 0, quantity = request.form['quantity'])
    session.add(newItem)
    session.commit()
    return "Added new item"


@app.route('/addNewCategory')
def addNewCategoryForm():
    return render_template('newCategory.html')

@app.route('/makeNewCategory', methods = ['POST'])
def makeNewCategory():
    if request.method == 'POST':
        newCategory = Category(categoryName = request.form['name'], categoryDescript = request.form['categoryDescript'])
    session.add(newCategory)
    session.commit()
    return "new Category Added."


##############################################

#Read Operations

@app.route('/enter/Item')
def getAllItemsByName():
    return render_template('searchByItem.html')

@app.route('/getItemInfo/<int:idInt>', methods = ['GET'])
def getSingleItemInfo(idInt):
    #query DB here
    object = session.query(Inventory).get(idInt)
    output = ''
    output += object.name
    output += ' '
    output += object.description
    return output


@app.route('/enter/Category')
def getItemsByCategory():
    categories = session.query(Category).all()
    numberEntries = session.query(Category).count()
    categorieNames = [0] * numberEntries
    categorieIDs = [0] * numberEntries
    categorieDescripts = [0] * numberEntries
    x = 0
    for row in categories:
        categorieNames[x] = row.categoryName
        x += 1
    return render_template('listAllCategories.html', categorieNames=categorieNames, numberEntries=numberEntries, categorieIDs=categorieIDs, categorieDescripts=categorieDescripts)

@app.route('/database', methods = ['GET', 'POST'])
def getAllDataBase():
    return "Database listing here"

@app.route('/enter/Item/getResults', methods = ['POST'])
def rerurnSearchResults():

    return render_template('ItemSearchResults.html')

@app.route('/itemInfo/<int:idInt>')
def getItemFullInfo(idInt):
    return "empty"


@app.route('/enter')
def DataBaseMainPage():
    return render_template('mainDatabaseUsePoint.html')

##################################################################


####################Update Functions##############################
@app.route('/updateItem/<int:idInt>')
def updateItem(idInt):
    updateItem = session.query(Inventory).get(idInt)
    categories = session.query(Category).all()
    numberEntries = session.query(Category).count()
    categorieNames = [0] * numberEntries
    x = 0
    for row in categories:
        categorieNames[x] = row.categoryName
        x += 1
    return render_template('updatePage.html', updateItem=updateItem, categorieNames=categorieNames, numberEntries=numberEntries)


@app.route('/itemUpdated', methods = ['POST'])
def commitChanges():
    updateThisItem = session.query(Inventory).get(request.form['ID'])
    updateThisItem.name = request.form['name']
    updateThisItem.price = request.form['price']
    updateThisItem.description = request.form['description']
    updateThisItem.quantity = request.form['quantity']
    session.add(updateThisItem)
    session.commit()
    return "Updated Item"


@app.route('/enter/editCategory/<int:idInt>')
def editSingleCategory(idInt):
    category = session.query(Category).get(idInt)
    categoryName = category.categoryName
    categoryDescript = category.categoryDescript
    catID = category.id
    return render_template('editCategory.html', category = category, categoryName=categoryName, categoryDescript=categoryDescript, catID=catID)


@app.route('/enter/editCategory/commit', methods = ['POST'])
def commitCatChange():
    category = session.query(Category).get(request.form['ID'])
    category.categoryName = request.form['name']
    category.categoryDescript = request.form['Descript']
    session.add(category)
    session.commit()
    return "Change Complete"


@app.route('/enter/editCategories')
def editCategoryPage():
    categories = session.query(Category).all()
    numberEntries = session.query(Category).count()
    categorieNames = [0] * numberEntries
    categorieIDs = [0] * numberEntries
    categorieDescripts = [0] * numberEntries
    x = 0
    for categoryX in categories:
        categorieNames[x] = categoryX.categoryName
        categorieIDs[x] = categoryX.id
        categorieDescripts[x] = categoryX.categoryDescript
        x += 1

    return render_template('editCategories.html', categorieNames=categorieNames, categorieIDs=categorieIDs, categorieDescripts=categorieDescripts, count=x)

#############################################################

####################Delete Functions##############################
@app.route('/deleteItem/<int:idInt>', methods = ['DELETE', 'POST'])
def deleteSingleItem(idInt):
    #delete DB entry here
	return "delete Item from database: %s" %idInt


@app.route('/deleteItem/<int:idInt>')
def deleteItemByID(idInt):
    itemToDelete = session.query(Inventory).get(idInt)
    session.delete(itemToDelete)
    session.commit()
    return "Item Deleted."

@app.route('/enter/deleteCategory/<int:idInt>')
def deleteCategory(idInt):
    categoryToDelete= session.query(Category).get(idInt)
    session.delete(categoryToDelete)
    session.commit()
    return render_template('categoryDeleted.html')

###########################################################################




def getItemByID():
    print "Get item"
    session.get

if __name__ == '__main__':
    app.secret_key = 'dummyKey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)
