import json
import logging

from django.http import HttpResponse, HttpResponseNotFound
import requests
import django_rq
from django_rq import job
from rq.job import Job, NoSuchJobError

from recommendation.model.classes import MatrixPreferenceDataModel as DataModel
from recommendation.metrics.pairwise import euclidean_distances
from recommendation.similarities.basic_similarities import ItemSimilarity
from recommendation.recommender.classes import ItemBasedRecommender
from recommendation.recommender.item_strategies import ItemsNeighborhoodStrategy
from recommendation.group.group import GroupRecommender
from recommendation.metrics.pairwise import disagreement_variance

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Viewer')

base_api_url = "http://harrenhal-php-97705.apse1.nitrousbox.com/elgg/services/api/rest/json/"


def individual_recommend(request):
    user_id = int(request.GET.get('user_id', '244'))
    job = django_rq.enqueue(recommended, user_id)
    response_data = {'status': 'processing', 'job': job.key}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_result(request):
    job_id = request.GET.get('job_id')
    redis_conn = django_rq.get_connection()
    job_id = job_id.split(':')[2]
    logger.info(job_id)
    try:
        job = Job.fetch(job_id, redis_conn)
        if job.is_finished:
            ret = job.return_value
        elif job.is_queued:
            ret = {'status': 'in-queue'}
            status = 201
        elif job.is_started:
            ret = {'status': 'waiting'}
        elif job.is_failed:
            ret = {'status': 'failed'}
        return HttpResponse(json.dumps(ret), content_type="application/json")
    except  NoSuchJobError:
        ret = {'status': 'No Job Found'}
        return HttpResponseNotFound(json.dumps(ret), content_type="application/json")


def group_recommend(request):
    job = django_rq.enqueue(grouprecommend)
    # job = django_rq.enqueue(recommended, user_id)

    response_data = {'status': 'processing', 'job': job.key}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

recommended_uri = "http://harrenhal-php-97705.apse1.nitrousbox.com/elgg/location/recommend"

@job
def recommended(user_id):
    payload = {'method': 'get.all.rating'}
    r = requests.get(base_api_url, params=payload)
    results = r.json()
    results = results['result']
    dataset = {}
    for result in results:
        if result['rating'] != 0:
            _user_id = result['user_id']
            if _user_id not in dataset:
                dataset[_user_id] = {}
            dataset[_user_id].update({result['page_id']: result['rating']})
    model = DataModel(dataset)
    similarity = ItemSimilarity(model, euclidean_distances)
    items_strategy = ItemsNeighborhoodStrategy()
    recsys = ItemBasedRecommender(model, similarity, items_strategy)
    response_data = {user_id : recsys.recommended(user_id)}
    headers = {'content-type': 'application/json'}
    data = json.dumps(response_data)
    logger.debug(data)
    r = requests.post(recommended_uri,data=data, headers=headers)
    logger.info(r.text)
    return response_data


@job
def grouprecommend():
    user_list = [244, 271, 272]
    payload = {'method': 'get.all.rating'}
    r = requests.get(base_api_url, params=payload)
    results = r.json()
    results = results['result']
    dataset = {}
    for result in results:
        if result['rating'] != 0:
            user_id = result['user_id']
            if user_id not in dataset:
                dataset[user_id] = {}
            dataset[user_id].update({result['page_id']: result['rating']})
    model = DataModel(dataset)
    similarity = ItemSimilarity(model, euclidean_distances)
    items_strategy = ItemsNeighborhoodStrategy()
    recsys = ItemBasedRecommender(model, similarity, items_strategy)

    for user in user_list:
        for place in recsys.recommended(user):
            logging.info(place)
            model.set_preference(user, place[0], place[1])

    gr = GroupRecommender(model, user_list, expertise="1", social="1", dissimmilarity=disagreement_variance)
    return gr.recommend()



