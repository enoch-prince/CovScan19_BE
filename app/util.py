""" Some Utility Functions """

def find_user(request, modelClass):
    """Find a User by name & dob and add to database"""

    credentials = None

    if request.is_json:
        credentials = request.get_json()
    else:
       credentials = request.form.to_dict()

    name = credentials.get("name")
    dob = credentials.get("dob")
    if name and dob:
        modelObject = modelClass.query.filter_by( name=name ).first()
        if modelObject is not None and modelObject.dob == dob:
            return (credentials, modelObject) # already exits
        return credentials

    else:
        return 13 #{"msg": "Please enter at least name and dob"}

def find_by_id(id, modelClass):
    """Find by user by ID and returns model object"""
    id = int(id) if isinstance(id, str) else id
    user = modelClass.query.get_or_404(id, description=f"User with ID {id} not found!")
    return user


# def get_user(db, modelClass):
#     """Acess User details from database"""

#     queryString = request.args.get("q")
#     if queryString is not None:        
#         if queryString == "admin":
#             # get users who are admins
#             admins = modelClass.query.filter_by( admin=True ).first_or_404( description="No admins registered yet!" )
#             return { "msg": "{} Admin(s) found".format(len(admins)), "data": admins }

#         if queryString.isdigit():
#             # get user by id
#             userID = int( queryString )
#             user = User.query.get_or_404( userID, description="User with ID {} not found".format(userID) )
#             return user 
        
#         # queryString must contain a name
#         user = modelClass.query.filter_by( username=queryString ).first_or_404( description="{} not found".format(queryString) )
#         return { "msg": "1 found!", "data": user }
    
#     # get all registered users
#     users = modelClass.query.all()
#     if len(users) > 0:
#         return { "msg": "{} found".format(len(users)), "data": users }
#     return { "msg": "No users registered yet!" } 
    
# def delete_user(db, modelClass):
#     """Delete User from database by name or id"""
#     tmp = next(iter(request.json.values())) # returns the first value of the dict from request.json
#     user = modelClass.query.filter_by( username=tmp ).first_or_404( description="{} not found".format(tmp) ) if isinstance(tmp, str) \
#            else modelClass.query.get_or_404( int(tmp), description="User with ID {} not found".format(tmp) ) 
#     db.session.delete( user ) # Delete User record from database
#     db.session.commit() # Commits changes
#     return True


#def get_all(modelClass, )