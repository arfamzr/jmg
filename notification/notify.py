from .models import Notification


class Notify:
    def make_notify(self, to_user, message, link=''):
        notification = Notification(
            to_user=to_user, message=message, link=link)
        notification.save()

    def get_header_notify(self, to_user):
        notifies = Notification.objects.filter(
            to_user=to_user).order_by('-created_at')[:10]
        return notifies
