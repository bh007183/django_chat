
from django.http import request


class ConnectionObject:
    # constructor
    def __init__(self, request):
        self.friend_id = request.data['friend_id']
        self.profile_id = request.user.id
    # These methods are for the initial connection request
    # returns dictonary in form that is required for setting the initiator in the DB
    def set_solicitor(self):
        data = {'friend_id': self.friend_id, 'profile_id': self.profile_id}
        return data
    # returns dictonary in form that is requred for setting recipient in the DB
    def set_recipient(self):
        data = {'friend_id': self.profile_id, 'profile_id': self.friend_id}
        return data

  

    








