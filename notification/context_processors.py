from .notify import Notify

notify = Notify()


def notify_context(request):
    if request.user.is_authenticated:
        notifies = notify.get_header_notify(request.user)
    else:
        notifies = None

    context = {
        'notifies': notifies,
    }
    return context
