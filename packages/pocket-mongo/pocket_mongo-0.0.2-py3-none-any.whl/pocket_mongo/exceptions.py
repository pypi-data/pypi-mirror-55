class PocketMongoConfigError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        Exception.__init__(
            self,
            'A configuration error has occurred: %s. '
            'Make sure you have called pocket_mongo.config' % msg,
        )


class PocketMongoCollectionNotDefined(Exception):
    def __init__(self, _class: str):
        self._class = _class
        Exception.__init__(
            self,
            'Class %s must define a <collection_name> attribute' % _class,
        )
