def on_failure(self, exc, task_id, *args, **kwargs):
    print("Oh no! Task failed: %r" % (exc, ))


def on_success(self, retval, task_id, *args, **kwargs):
    print('Task success. (id: {}, retval: {} args: {}, kwargs: {}'.format(task_id, retval, args, kwargs))
