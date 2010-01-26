def create_test_run_listener(sender, request, *args, **kwargs):
    from django.contrib.auth.models import User
    from django.db.models import Q
    run = kwargs.get('test_run', None)
    if not run:
        return
    #notify_list = User.objects.filter(~Q(reporter=run.reporter))
    notify_list = User.objects.all()
    notification.send(notify_list, "squaretracker_testrun",
                      {"creator": run.reporter, "testrun": run})

from django.conf import settings
if "notification" in getattr(settings, "INSTALLED_APPS"):
    from notification import models as notification
    from squaretracker.signals import test_run_started
    test_run_started.connect(create_test_run_listener)

