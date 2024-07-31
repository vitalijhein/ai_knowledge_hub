import pymongo


'''
lit_listicle_collection
private_tweet_collection
actionable_posters_collection
actionable_single_tweet_collection
thread_outline_collection
'''

class MongoDatabase: 
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["mydatabase"]

    def get_or_create_collection(self, collection_name):
        try:
            return self.db[collection_name]
        except pymongo.errors.OperationFailure:
            # Collection doesn't exist, let's create it
            self.db.create_collection(collection_name)
            return self.db[collection_name]
        
    def insert_one_into_collection_mdb(self, collection_name, my_dict):
        '''mydict = { "name": "Peter", "address": "Lowstreet 27" }'''
        try:
            collection = self.get_or_create_collection(collection_name)
            collection.insert_one(my_dict)
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while inserting one into the collection: {e}")
            
            
    def insert_many_into_collection_mdb(self, collection_name, my_list_dict):
        '''
        mylist = [
            { "name": "Amy", "address": "Apple st 652"},
            { "name": "Hannah", "address": "Mountain 21"},
            { "name": "Michael", "address": "Valley 345"},
            { "name": "Sandy", "address": "Ocean blvd 2"},
            { "name": "Betty", "address": "Green Grass 1"},
            { "name": "Richard", "address": "Sky st 331"},
            { "name": "Susan", "address": "One way 98"},
            { "name": "Vicky", "address": "Yellow Garden 2"},
            { "name": "Ben", "address": "Park Lane 38"},
            { "name": "William", "address": "Central st 954"},
            { "name": "Chuck", "address": "Main Road 989"},
            { "name": "Viola", "address": "Sideway 1633"}
        ]
        '''
        try:
            collection = self.get_or_create_collection(collection_name)
            collection.insert_many(my_list_dict)
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while inserting many into the collection: {e}")

    def insert_many_into_collection_with_id_mdb(self, collection_name, my_list_dict):
        '''
        mylist = [
            { "_id": 1, "name": "John", "address": "Highway 37"},
            { "_id": 2, "name": "Peter", "address": "Lowstreet 27"},
            { "_id": 3, "name": "Amy", "address": "Apple st 652"},
            { "_id": 4, "name": "Hannah", "address": "Mountain 21"},
            { "_id": 5, "name": "Michael", "address": "Valley 345"},
            { "_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
            { "_id": 7, "name": "Betty", "address": "Green Grass 1"},
            { "_id": 8, "name": "Richard", "address": "Sky st 331"},
            { "_id": 9, "name": "Susan", "address": "One way 98"},
            { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
            { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
            { "_id": 12, "name": "William", "address": "Central st 954"},
            { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
            { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
        ]
        '''
        try:
            collection = self.get_or_create_collection(collection_name)
            collection.insert_many(my_list_dict)
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while inserting many with specific id into the collection: {e}")

    def find_the_first_occurence_in_col_mdb(self, collection_name):
        try:
            collection = self.get_or_create_collection(collection_name)
            return collection.find_one()
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while finding the first occurrence in the collection: {e}")
            return None
        
    def find_the_first_occurence_in_col_mdb(self, collection_name):
        try:
            collection = self.get_or_create_collection(collection_name)
            return collection.find_one()
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while finding the first occurrence in the collection: {e}")
            return None
        
    def find_the_record_in_col_mdb(self, collection_name, query_dict):
        '''
        # Query for a single document
        document = collection.find_one({"name": "John"})
        '''
        try:
            collection = self.get_or_create_collection(collection_name)
            return collection.find_one(query_dict)
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while filtering the collection: {e}")
            return None
    
    def find_all_occurences_in_col_mdb(self, collection_name, limit = 1000000):
        try:
            collection = self.get_or_create_collection(collection_name)
            return collection.find().limit(limit)
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while searching all occurrences in the collection: {e}")
            return []
        
        
    def find_the_record_exclude_columns_in_col_mdb(self, collection_name, query_dict):
        '''
        # 0 = Exlcude, 1 = Include
        mycol.find({},{ "_id": 0, "name": 1, "address": 1 })
        Only exlcude address
        mycol.find({},{ "address": 0 })

        '''
        try:
            collection = self.get_or_create_collection(collection_name)
            return collection.find({},query_dict)
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while finding the first occurrence in the collection: {e}")
            return None

    
    def filter_results_in_col_mdb(self, collection_name, query_dict):
        '''
        # Filter the result based on the address
        myquery = { "address": "Park Lane 38" }
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)
        '''
        try:
            collection = self.get_or_create_collection(collection_name)
            return collection.find(query_dict)
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while filtering the collection: {e}")
            return None
    
    
    def sort_results_in_col_mdb(self, collection_name, sort_key, sort_order=1):
        '''
        sort("name", 1) #ascending
        sort("name", -1) #descending
        sort_key = "name"
        # Sort the result alphabetically by name
        mydoc = mycol.find().sort("name")
        for x in mydoc:
            print(x)
        '''
        try:
            collection = self.get_or_create_collection(collection_name)
            return collection.find().sort(sort_key, sort_order)
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while sorting the collection: {e}")
            return None
        
    def delete_one_from_col_mdb(self, collection_name, query_dict):
        '''
        # Delete the document with the address "Mountain 21"
        myquery = { "address": "Mountain 21" }
        mycol.delete_one(myquery)
        '''
        try:
            collection = self.get_or_create_collection(collection_name)
            x = collection.delete_one(query_dict)
            print(f"{x.deleted_count} documents deleted.")

        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while deleting one from the collection: {e}")
            
    def delete_many_from_col_mdb(self, collection_name, query_dict):
        '''
        # Delete all documents were the address starts with the letter "S"
        myquery = { "address": {"$regex": "^S"} }
        x = mycol.delete_many(myquery)
        print(x.deleted_count, " documents deleted.")
        '''
        try:
            collection = self.get_or_create_collection(collection_name)
            x = collection.delete_many(query_dict)
            print(f"{x.deleted_count} documents deleted.")

        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while deleting many from the collection: {e}")
            
    def delete_all_doc_in_collection_mdb(self, collection_name):
        try:
            collection = self.get_or_create_collection(collection_name)
            x = collection.delete_many({})
            print(f"{x.deleted_count} documents deleted.")

        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while deleting the collection: {e}")
            
    def delete_collection_mdb(self, collection_name):
        try:
            collection = self.get_or_create_collection(collection_name)
            collection.drop()
            print(f"The collection {collection_name} has been deleted.")
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while deleting the collection: {e}")
            
            
    def update_one_in_collection_mdb(self, collection_name, query_dict, new_dict):
        '''
        # Update the address of the first document whose name is "John"
        myquery = { "name": "John" }
        newvalues = { "$set": { "address": "Canyon 123" } }
        mycol.update_one(myquery, newvalues)
        '''
        try:
            new_values = { "$set": new_dict }
            collection = self.get_or_create_collection(collection_name)
            collection.update_one(query_dict, new_values)
            print("1 document updated.")
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while updating one in the collection: {e}")
            
    def update_many_in_collection_mdb(self, collection_name, query_dict, new_dict):
        '''
        # Update all documents where the address starts with the letter "S"
        myquery = { "address": { "$regex": "^S" } }
        newvalues = { "$set": { "name": "Minnie" } }
        x = mycol.update_many(myquery, newvalues)
        print(x.modified_count, "documents updated.")
        '''
        try:
            new_values = { "$set": new_dict }
            collection = self.get_or_create_collection(collection_name)
            collection.update_many(query_dict, new_values)
            print("Documents updated.")

        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred while updating many in the collection: {e}")
            
            
    def upsert_into_collection(self, collection_name, query_dict, update_dict):
        """
        Upserts a document into the specified collection based on a query.
        If a document matching the query exists, it updates it with the values in update_dict.
        If no document matches, it inserts a new document combining query_dict and update_dict.

        Args:
        - collection_name (str): The name of the collection to upsert into.
        - query_dict (dict): The query criteria to locate the document to update.
        - update_dict (dict): The document's new values or fields to add.

        Example:
            query_dict = {"id": "some_unique_id"}
            update_dict = {"$set": {"key1": "value1", "key2": "value2"}}
            upsert_into_collection("mycollection", query_dict, update_dict)
        """
        try:
            collection = self.get_or_create_collection(collection_name)
            result = collection.update_one(query_dict, update_dict, upsert=True)
            
            # After upsert, retrieve the document to display it
            document = collection.find_one(query_dict)
            
            if result.matched_count > 0:
                print("Document updated:", document)
            elif result.upserted_id is not None:
                print("New document inserted with _id:", result.upserted_id, document)
            else:
                print("No changes made to the collection.")
            
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred during the upsert operation: {e}")
