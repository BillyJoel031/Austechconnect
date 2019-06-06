import os
from json.decoder import JSONDecodeError

import requests


def setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "austech_connect.settings")
    import django
    django.setup()


setup()


def get_user_bio(url):
    r = requests.get(url)
    try:
        response = r.json()
        return response
    except JSONDecodeError:
        return None


def create_new_project(project_json):
    from search.models import Project, Category, Person

    p = project_json
    project = Project()
    project.id = p['id']
    project.name = p.get('name', '')
    project.short_description = p.get('blurb', '')
    if 'location' in p:
        p_location = p['location']
        project.location = p_location['displayable_name']
    if 'category' in p:
        p_category = p['category']
        category = Category.objects.filter(name__icontains=p_category['slug'].split('/')[0])[0]
        if category:
            project.category = category

    # check if creator exits, if not then create
    if 'creator' in p:
        p_creator = p['creator']
        creator = Person.objects.filter(id=p_creator['id']).first()
        if not creator:
            creator = Person()
            creator.id = p_creator['id']
            creator.name = p_creator['name']
            creator_bio_api = p_creator['urls']['api']['user']
            creator_bio = get_user_bio(url=creator_bio_api)
            if creator_bio is None:
                print('{} - None'.format(creator_bio_api))
                return
            if 'location' in creator_bio and creator_bio['location']:
                creator.location = creator_bio['location']['displayable_name']
            if 'biography' in creator_bio and creator_bio['biography']:
                creator.about = creator_bio['biography']
            if 'join_date' in creator_bio and creator_bio['join_date']:
                creator.joined_date = creator_bio['join_date']
            creator.save()
            print('Created person: {}'.format(creator.name))
        project.creator = creator

    project.save()
    print('Created project: {}'.format(project.name))


def main():
    from search.models import Project

    url = "https://www.kickstarter.com/discover/advanced"

    querystring = {"google_chrome_workaround": "", "woe_id": "0", "sort": "magic", "seed": "2596426", "page": "0"}

    payload = ""
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9,vi;q=0.8",
        'cache-control': "no-cache,no-cache",
        'cookie': "vis=784b1ccc7e38b94e-f3ceae7ff9864ea5-d54466d000569054v1; _ga=GA1.2.83354959.1557240420; __ssid=a6703c3d115b505122f5b1b719f8a9d; lang=en; woe_id=VXJQbTZLdzlibVpJVzNsb3RxQUpHQT09LS1wMVoraWx0UW03RzE4MkhaQ2pTWTR3PT0%3D--d54ae00acda42c6dd27a7256dfb078a1cddb702a; _gid=GA1.2.1488885418.1557846662; __stripe_mid=83dc235c-6470-4e20-a79c-4c35b66bcd2f; __stripe_sid=f35ce963-c556-4b63-9219-a24095316983; last_page=https%3A%2F%2Fwww.kickstarter.com%2Fprofile%2Fjohn-kurzy%2Fabout; local_offset=-989; _ksr_session=RkliTXEvYTN6Z0RmbXJzWUVEL1BuRkxlbUtoek5oQytkSVBoLzJNbktTZkY3T201TmNzSkR3d2hoYklQS0pQSzBRSWVFUnVrRVhBN3g3Qms0OWFTclFQcjZjREtLeGJ4RnJ1T0g4RTE4QUdsbzVhY0FhbE1ha1JQV1krS0x3R0dnejg0bGFqcE4yMkNRR0VJUXp1cFpnPT0tLVJOczk2aGt1RjBpdkNGSG5KYWJrQ3c9PQ%3D%3D--7378345eb835194105ee52d68bb40434ad7ce118; request_time=Tue%2C+14+May+2019+18%3A09%3A17+-0000, vis=784b1ccc7e38b94e-f3ceae7ff9864ea5-d54466d000569054v1; _ga=GA1.2.83354959.1557240420; __ssid=a6703c3d115b505122f5b1b719f8a9d; lang=en; woe_id=VXJQbTZLdzlibVpJVzNsb3RxQUpHQT09LS1wMVoraWx0UW03RzE4MkhaQ2pTWTR3PT0%3D--d54ae00acda42c6dd27a7256dfb078a1cddb702a; _gid=GA1.2.1488885418.1557846662; __stripe_mid=83dc235c-6470-4e20-a79c-4c35b66bcd2f; __stripe_sid=f35ce963-c556-4b63-9219-a24095316983; last_page=https%3A%2F%2Fwww.kickstarter.com%2Fprofile%2Fjohn-kurzy%2Fabout; local_offset=-989; _ksr_session=RkliTXEvYTN6Z0RmbXJzWUVEL1BuRkxlbUtoek5oQytkSVBoLzJNbktTZkY3T201TmNzSkR3d2hoYklQS0pQSzBRSWVFUnVrRVhBN3g3Qms0OWFTclFQcjZjREtLeGJ4RnJ1T0g4RTE4QUdsbzVhY0FhbE1ha1JQV1krS0x3R0dnejg0bGFqcE4yMkNRR0VJUXp1cFpnPT0tLVJOczk2aGt1RjBpdkNGSG5KYWJrQ3c9PQ%3D%3D--7378345eb835194105ee52d68bb40434ad7ce118; request_time=Tue%2C+14+May+2019+18%3A09%3A17+-0000; vis=b1263f242d1c5bfc-35ec91baaec30aa4-cb4ed49dcefb736fv1; lang=en; last_page=https%3A%2F%2Fwww.kickstarter.com%2Fdiscover%2Fadvanced%3Fgoogle_chrome_workaround%26woe_id%3D0%26sort%3Dmagic%26seed%3D2596426%26page%3D4; woe_id=NE5SRUhIQ1I2NTk3OXdncmZnTzF4dz09LS0xYmFQdjU3RHM0ZmRIYmx6dVIyRXBRPT0%3D--d72de5bc043e2e83ba778b1dc3bf555f463dcdbd; _ksr_session=NWNFTDhxaExuZFFOSVlEd0ZRd3dHWFFvUW9QaWNGWk5IK1NUQWVmY2RWNWdJdlFZWFBNUWgzR1B4Z25adTBSU2F1bGpRSU8vQWF0aFBaM1NZb1dPbFcvSEdINWZ1OEVlWldyUEl6ZnBiaUVHQ2xhWXExTTgzMXdSbEFUTVNNRG5VZzQ4cmY4a0wyVXM3cm4yTCtoZllnPT0tLUdpMEFkamR0T2t1R1dXYjRoeld5SWc9PQ%3D%3D--5843d5b1756b4a9260cb100a4775f20e6375b67c; request_time=Tue%2C+14+May+2019+18%3A43%3A52+-0000",
        'pragma': "no-cache",
        'referer': "https://www.kickstarter.com/discover/advanced?woe_id=0&sort=magic&seed=2596426&page=3",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'x-csrf-token': "EinaQwHTKrycUAuXoIwW1FwbOYK+FY/Kb8kNqNJQw0Tooj39Y0ZCgq7oHg1MBa7Frj7Fi4D9EMPI4AL3kcAEbA==",
        'x-requested-with': "XMLHttpRequest",
        'Postman-Token': "839a0089-fc9f-4082-93b2-ad13084f6fad,732b48ec-200c-4f00-8e68-5b376ff998ab",
        'Host': "www.kickstarter.com",
        'Connection': "keep-alive"
    }

    page_start = 1
    page_end = 100
    for page in range(page_start, page_end + 1):
        querystring.update({'page': page})
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        json_response = response.json()
        projects = json_response['projects']
        print('page {} - {} projects'.format(page, len(projects)))
        for p in projects:
            project = Project.objects.filter(id=p['id']).first()
            if not project:
                create_new_project(project_json=p)


if __name__ == '__main__':
    main()
