from db import *

db = DB()

db.collection_voter_details.update_one({'voter_id' : 'abcd123'},{ "$set": { 'pub_key': '','vote' : 0 } })
db.collection_voter_details.update_one({'voter_id' : 'abcd12345'},{ "$set": { 'pub_key': '','vote' : 0 } })
db.collection_voter_details.update_one({'voter_id' : 'abcd123456'},{ "$set": { 'pub_key': '','vote' : 0 } })


