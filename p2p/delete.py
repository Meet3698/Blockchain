from db import *

db = DB()

db.collection_voter_details.update_one({'voter_id' : 'abcd123'},{ "$set": { 'pub_key': '','vote' : 0 } })
