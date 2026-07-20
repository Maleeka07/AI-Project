from models import db

db.execute_update("UPDATE movies SET poster_path = REPLACE(poster_path, '/static/', 'static/')")
print("Paths updated successfully.")
