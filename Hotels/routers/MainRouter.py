class MainRouter(object):
    #models = ['bookings', 'employees', 'filials', 'guests', 'jobs', 'livings', 'room_types', 'room_types_names',
    #          'rooms', 'statuses', 'work']
    models = ['Hotels']
    def db_for_read(self, model, **hints):
        """
        Reading
        """
        if model._meta.app_label in self.models:
            return 'hotels'
        return None

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        if model._meta.app_label in self.models:
            return 'hotels'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return None
