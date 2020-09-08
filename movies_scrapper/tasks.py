from bs4 import BeautifulSoup
import requests
import re

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import shared_task

from movie.models import Movie
from requests.exceptions import MissingSchema, InvalidURL, ConnectionError, RequestException

@shared_task
def scrapping_from_url(url):
    try:
        # url = 'http://www.imdb.com/chart/top'
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        movies = soup.select('td.titleColumn')
        links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
        crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
        ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
        votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

        imdb = []

        # Store each item into dictionary (data), then put those into a list (imdb)
        for index in range(0, len(movies)):
            # Seperate movie into: 'place', 'title', 'year'
            movie_string = movies[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index))+1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            place = movie[:len(str(index))-(len(movie))]
            data = {"name": movie_title,
                    "year": year,
                    "place": place,
                    "star_cast": crew[index],
                    "rating": ratings[index],
                    "vote": votes[index],
                    "link": links[index],
                    "title_id": links[index].split("/")[2]}
            imdb.append(data)

        for item in imdb:
            print({ "name": item['name'], "description": "", "year": str(item['year'] or ''), "place": str(item['place'] or ''), "crew": str(item['star_cast'] or ''), "ratings": str(item['rating'] or ''), "votes": str(item['vote'] or ''), "links" : str(item['link'] or '')})
            try:
                obj, created = Movie.objects.update_or_create(title_unique_id=item['title_id'],defaults={ "name": item['name'], "description": "", "year": item['year'], "place": str(item['place'] or ''), "crew": str(item['star_cast'] or ''), "ratings": str(item['rating'] or ''), "votes": str(item['vote'] or ''), "links" : str(item['link'] or '')})
                print(obj, created)
            except:
                print("Error ==>")
    except (MissingSchema, InvalidURL):
        print("Invalid URL")
    except (RequestException):
        print("Unknown error connecting")
    except Exception as error:
        print("Failed to retrieve data", error)

