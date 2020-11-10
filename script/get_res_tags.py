# param: res array of Poem Objects (mongo)
def get_tags(res):
    tags = []
    for poem in res:
        tags.append([poem['tags_emotional'],
                     poem['tags_epic'],
                     poem['tags_neutral'],
                     poem['tags_philo'],
                     poem['tags_relax'],
                     poem['tags_sad']])
    return tags
