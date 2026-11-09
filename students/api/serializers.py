from rest_framework import serializers
from students.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:

        model=Student
        
        fields=[            
            "id",
            "name",
            "age",
            "email",
            "phone",
            "marks",
            "city",
            "course",
            "skills",

        ]

        read_only_fields=["id"]

# read_only_fields makes selected fields output-only (read only but not edit).

# GET METHOD=> DJANGO MODEL < SERIALIZATION< JSON RESPONSE
# POST => JSON <DESERIALIATION < DJANGO MODEL(Save to database)

# API stands for Application Programming Interface. An API allows two software applications to communicate with each other.

# REST stands for Representational State Transfer. It is a set of architectural principles commonly used to design web APIs.

# Django REST Framework (DRF) is a Django library that makes building REST-style APIs easier