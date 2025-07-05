from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, connect, ObjectIdField
import datetime

connect(db='JobReco', host='localhost', port=27017)

class JobDocument(Document):
    """
    Defines the schema for a Job document in the 'Jobs' collection.
    """
    id = StringField(required=True, unique=True)
    title = StringField(required=True)
    company = StringField(required=True)
    location = StringField(required=True)
    experience = StringField(required=True)
    post_date = StringField(required=True)
    link = StringField(required=True)
    key_skills = ListField(StringField(required=False))
    job_description = StringField(required=True)

    meta = {'collection': 'Jobs'}

    def __str__(self):
        return {
            "_id": ObjectIdField,
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "experience": self.experience,
            "post_date": self.post_date,
            "link": self.link,
            "key_skills": self.key_skills,
            "job_description": self.job_description
        }

    def to_dict(self):
        return {
            "_id": str(self._id),
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "experience": self.experience,
            "post_date": self.post_date,
            "link": self.link,
            "key_skills": self.key_skills,
            "job_description": self.job_description
        }