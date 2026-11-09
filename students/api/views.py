from rest_framework import generics,viewsets
from rest_framework.permissions import IsAuthenticated

from students.models import Student
from .serializers import StudentSerializer

class StudentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class=StudentSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)

# This method runs when a new Student is being created through API.

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)



# Generics are ready-made, reusable API view classes provided by DRF(django rest framework).
# Generic view

# ListAPIView    => Lists records

# CreateAPIView  => Creates records

# RetrieveAPIView  => Gets one record

# UpdateAPIView    => Updates a record

# DestroyAPIView    =>  Deletes a record

# ListCreateAPIView  => Lists records and creates records


# PERMISSIONS
# A permission class decides whether a request is allowed to access a particular API view.
# IsAuthenticated means that the request must come from an authenticated user.

# For example:
# A logged-in user can proceed to the view, subject to other checks.
# An anonymous user is denied access when the permission is enforced.

# What is a queryset?

# A QuerySet is a Django object that represents a collection of database records and lets you filter, order and retrieve them.

# A request is the information sent by a client to your server.
# Important: This works only if your Student model has a suitable user field, typically a ForeignKey to Django's user model. If your model doesn't have that field, this query will fail.

# Difference bw IsAuthenticated and  get_queryset:=>
# IsAuthenticated checks that a user is logged in; get_queryset() limits which records that user can see.


# PERFORM_CREATE:
# This method controls what happens when a new student is created through the API.
# "Save the new student and assign the currently logged-in user as its owner."
# example:
# name      age      city      user
# Rahul       21       Delhi   Logged-in user



# SERIALIZERS

# A serializer acts as a bridge between complex Python objects, such as Django model instances, and simple data types(JSON) that an API can return or accept.

# Think about this:
# Django model instances:
# student = Student.objects.get(id=1)

# The variable student contains a Django model instance. It is not directly a JSON response.
# A serializer can turn that object into simple data:

# {
#   "id": 1,
#   "name": "Rahul",
#   "age": 21,
#   "email": "rahul@example.com"
# }

# How do we convert the model object into that data format? We use a serializer.

#           Django model object
            # Python model instance
#                 ⇓

#         Student(name="Rahul", age=21)
#                 ⇓

#        Convert to simple data types
#                 ⇓
#              StudentSerializer
#          Serialization and deserialization

#                 ⇓
                # JSON RESPONSE
#                  {}
#               Simple data
#          {'name': 'Rahul', 'age': 21}

# A serializer works in two directions:

# Serialization: Python object → simple data → JSON response.

# Deserialization: incoming JSON → parsed data → validation → Python/model object. 

class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=StudentSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)



class StudentViewSet(viewsets.ModelViewSet):
    serializer_class=StudentSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        return serializer.save(user=self.request.user)