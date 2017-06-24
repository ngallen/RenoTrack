import primary
import random
import string
import datetime

app = primary.app
APPLICATION_NAME = "Renovation Tracker"
session = primary.session
engine = primary.engine

# Show front page
@app.route('/')
def redir():
    return primary.redirect("renoTrack")

@app.route('/renoTrack')
def showIndex():
    if 'user_id' in primary.login_session:
        user_id = primary.login_session['user_id']
    else:
        user_id = None
    [areas, areaLength, numRenoItems] = primary.getAreas()
    [items] = primary.getRenoItems()
    return primary.render_template('index.html',
                                    areas=areas,
                                    activeNav = primary.makeActive(-1, areaLength),
                                    areaLength = areaLength,
                                    numRenoItems = numRenoItems,
                                    items = items,
                                    user_id = user_id)

# Show an area's reno-list
@app.route('/renoTrack/area/<int:area_id>/')
def showArea(area_id):
    [areas, areaLength, numRenoItems] = primary.getAreas()
    liveArea = primary.getOneArea(area_id)
    [items] = primary.getRenoItems(area_id)
    if 'user_id' in primary.login_session:
        user_id = primary.login_session['user_id']
    else:
        user_id = None
    return primary.render_template('area.html',
                                    activeNav = primary.makeActive(area_id-1, areaLength),
                                    items=items,
                                    liveArea=liveArea,
                                    areas=areas,
                                    areaLength = areaLength,
                                    numRenoItems = numRenoItems,
                                    user_id=user_id)

# Show an area's reno-list
@app.route('/renoTrack/renoItem/<int:reno_id>/')
def showRenoItem(reno_id):
    [areas, areaLength, numRenoItems] = primary.getAreas()
    oneItem = primary.getOneItem(reno_id)
    liveArea = primary.getOneArea(oneItem.area_id)
    if 'user_id' in primary.login_session:
        user_id = primary.login_session['user_id']
    else:
        user_id = None
    return primary.render_template('showrenoitem.html',
                                    activeNav = primary.makeActive(oneItem.area_id-1, areaLength),
                                    item=oneItem,
                                    liveArea=liveArea,
                                    areas=areas,
                                    areaLength = areaLength,
                                    numRenoItems = numRenoItems,
                                    user_id=user_id)


# Create a new reno item
@app.route('/renoTrack/renoItem/new/', methods=['GET', 'POST'])
def newRenoItem():
    [areas, areaLength, numRenoItems] = primary.getAreas()
    [items] = primary.getRenoItems()
    if 'user_id' in primary.login_session:
        userID = primary.login_session['user_id']
    else:
        return primary.redirect('/renoTrack/login')

    if primary.request.method == 'POST':
        newItem = primary.RenoItem(name=primary.request.form['name'], description=primary.request.form['description'], cost=primary.request.form[
                           'cost'], area_id=primary.request.form[
                           'area_id'], user_id=userID)
        session.add(newItem)
        session.commit()
        primary.flash('New Reno %s Item Successfully Created' % (newItem.name))
        return primary.redirect('/')

    return primary.render_template('newrenoitem.html',
                                    activeNav = primary.makeActive(-1, areaLength),
                                    items=items,
                                    areas=areas,
                                    areaLength = areaLength,
                                    numRenoItems = numRenoItems,
                                    user_id=userID)

# Edit a reno item
@app.route('/renoTrack/renoItem/<int:reno_id>/edit', methods=['GET', 'POST'])
def editRenoItem(reno_id):
    [areas, areaLength, numRenoItems] = primary.getAreas()
    oneItem = primary.getOneItem(reno_id)
    liveArea = primary.getOneArea(oneItem.area_id)
    if 'user_id' in primary.login_session:
        userID = primary.login_session['user_id']
        if primary.login_session['user_id'] != oneItem.user_id:
            return "<script>function myFunction() {alert('You are not authorized to edit this renovation item');}</script><body onload='myFunction()''>"
    else:
        return primary.redirect('/renoTrack/login')

    if primary.request.method == 'POST':
        if primary.request.form['name']:
            oneItem.name = primary.request.form['name']
        if primary.request.form['description']:
            oneItem.description = primary.request.form['description']
        if primary.request.form['cost']:
            oneItem.cost = primary.request.form['cost']
        if primary.request.form['area_id']:
            oneItem.course = primary.request.form['area_id']
        session.add(oneItem)
        session.commit()
        primary.flash('Renovation Item Successfully Edited %s')
        return primary.redirect('/renoTrack/renoItem/%s/' % oneItem.id)
    else:
        return primary.render_template('editrenoitem.html',
                                    activeNav = primary.makeActive(-1, areaLength),
                                    areas = areas,
                                    areaLength = areaLength,
                                    numRenoItems = numRenoItems,
                                    item=oneItem,
                                    liveArea=liveArea,
                                    user_id=userID)



# Delete a reno item
@app.route('/renoTrack/renoItem/<int:reno_id>/delete', methods=['GET', 'POST'])
def deleteRenoItem(reno_id):
    [areas, areaLength, numRenoItems] = primary.getAreas()
    oneItem = primary.getOneItem(reno_id)
    liveArea = primary.getOneArea(oneItem.area_id)
    if 'user_id' in primary.login_session:
        userID = primary.login_session['user_id']
        if primary.login_session['user_id'] != oneItem.user_id:
            return "<script>function myFunction() {alert('You are not authorized to edit this renovation item');}</script><body onload='myFunction()''>"
    else:
        return primary.redirect('/renoTrack/login')

    if primary.request.method == 'POST':
        session.delete(oneItem)
        session.commit()
        primary.flash('%s Successfully Deleted' % oneItem.name)
        return primary.redirect('/renoTrack')
    else:
        return primary.render_template('deleterenoitem.html',
                                    activeNav = primary.makeActive(-1, areaLength),
                                    areas = areas,
                                    areaLength = areaLength,
                                    numRenoItems = numRenoItems,
                                    item=oneItem,
                                    liveArea=liveArea,
                                    user_id=userID)

# Create anti-forgery state token
@app.route('/renoTrack/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    primary.login_session['state'] = state
    return primary.render_template('login.html', STATE=state)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

# JSON APIs to view Area Information
@app.route('/renotrack/<int:area_id>/JSON')
def areaRenoJSON(area_id):
    area = session.query(Area).filter_by(id=area_id).one()
    items = session.query(RenoItem).filter_by(
        area_id=area_id).all()
    return jsonify(RenoItems=[i.serialize for i in items])

@app.route('/renotrack/<int:reno_id>/JSON')
def renoItemJSON(reno_id):
    Reno_Item = session.query(RenoItem).filter_by(id=reno_id).one()
    return jsonify(Reno_Item=Reno_Item.serialize)


@app.route('/renotrack/JSON')
def areasJSON():
    areas = session.query(Area).all()
    return jsonify(areas=[r.serialize for r in areas])