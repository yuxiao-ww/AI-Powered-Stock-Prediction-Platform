# graphql_models.py
from mongoengine import (DateTimeField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, IntField, ListField,
                         ObjectIdField, StringField)


class UserInfo(EmbeddedDocument):
    user_id = StringField(required=True)
    user_name = StringField(required=True)


class Post(Document):
    meta = {"collection": "post"}
    post_title = StringField(required=True, min_length=3, max_length=200)
    post_url = StringField()
    post_date = DateTimeField(required=True)
    poster_user_info = EmbeddedDocumentField(UserInfo)
    content = StringField(required=True, min_length=1, max_length=1000)
    comment_ids = ListField(ObjectIdField())
    upvote = IntField(default=0, max_value=1000000)
    downvote = IntField(default=0, max_value=1000000)
    all_comment_ids = ListField(ObjectIdField())


class Comment(Document):
    meta = {"collection": "comment"}
    post_id = ObjectIdField(required=True)
    commenter_info = EmbeddedDocumentField(UserInfo)
    content = StringField(required=True, min_length=1, max_length=1000)
    comment_ids = ListField(ObjectIdField())


class User(Document):
    meta = {"collection": "user"}
    user_id = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True, min_length=5, max_length=100)
    display_name = StringField(required=True, min_length=1, max_length=50)
    password = StringField(required=True, min_length=128)
