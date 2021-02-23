from Social_Scraper import db

metadata = db.MetaData()

for tbl in reversed(metadata.sorted_tables):
    engine.execute(tbl.delete())

db.create_all()
print('success')
