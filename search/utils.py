from search.models import Person


def person_2_dict(person: Person):
    return {
        'pk': person.pk,
        'name': person.name,
        'location': person.location,
        'category': str(person.category),
        'about': person.about
    }
