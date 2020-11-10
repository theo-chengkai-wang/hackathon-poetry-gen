import pymongo as pm

client = pm.MongoClient("mongodb://localhost:27017")
db = client.hackathon_techx
poems = db.poems_tang


def search_1(request):
    res_list = poems.find({'$or': [{'name': {'$regex': request.form['search']}}, {'author_name': {
                          '$regex': request.form['search']}}, {'content': {'$regex': request.form['search']}}]})[:5]
    #print(res_list[0])
    #print([res_list[0]['tags_emotional'],res_list[0]['tags_epic'],res_list[0]['tags_neutral'],res_list[0]['tags_philo'],res_list[0]['tags_relax'],res_list[0]['tags_sad']])
    return list(res_list)
