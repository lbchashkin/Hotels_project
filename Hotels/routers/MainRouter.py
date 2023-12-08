import threading
request_cfg = threading.local()

class RouterMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, args, kwargs):
        request_cfg.user = request.user

    def process_response(self, request, response):
        if hasattr(request_cfg, 'user'):
            del request_cfg.user
        return response

class MainRouter(object):
    #models = ['bookings', 'employees', 'filials', 'guests', 'jobs', 'livings', 'room_types', 'room_types_names',
    #          'rooms', 'statuses', 'work']
    models = ['Hotels']
    def db_for_read(self, model, **hints):
        """
        Reading
        """
        if model._meta.app_label in self.models:
            if hasattr(request_cfg, 'user') and request_cfg.user.groups.filter(name="filial1").exists():
                return 'hotels_1'
            else:
                return 'hotels_main'
        return None

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        if model._meta.app_label in self.models:
            if self.request.user.groups.filter(name="filial1").exists():
                return 'hotels_1'
            else:
                return 'hotels_main'
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
