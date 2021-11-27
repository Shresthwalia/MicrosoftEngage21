import pymongo


class MonitoringClusterConnection(object):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MonitoringClusterConnection.__get_mongodb_database()
        return cls._instance

    @staticmethod
    def __get_mongodb_database():
        from OnlineJudge import settings
        url = settings.MONGODB_URL
        client = pymongo.MongoClient(url)
        db = client.online_judge

        return db