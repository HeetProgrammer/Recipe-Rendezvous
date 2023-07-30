from directory import db, app
app.app_context().push()
db.drop_all()
db.create_all()