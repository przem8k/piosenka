from django.conf.urls import url
from django.core.urlresolvers import reverse


class EditReviewApprove(object):
    """Url scheme for notes, which do not have their own view view.

    Needs the inheriting class to have:

    - get_url_name()
    """
    def get_edit_url(self):
        return reverse('edit_' + self.get_url_name(),
                       kwargs=self.get_url_params())

    def get_review_url(self):
        return reverse('review_' + self.get_url_name(),
                       kwargs=self.get_url_params())

    def get_approve_url(self):
        return reverse('approve_' + self.get_url_name(),
                       kwargs=self.get_url_params())


class ViewEditReviewApprove(EditReviewApprove):
    """Needs the inheriting class to have:

    - get_url_name()
    """
    def get_absolute_url(self):
        return reverse('view_' + self.get_url_name(),
                       kwargs=self.get_url_params())


def edit_review_approve(name, edit, review, approve):
    """Returns the standard scheme of three views for a content item type.

    Three views are suitable for notes, which do not have their own view view.
    """
    return [
        url(r'^edytuj/$', edit.as_view(),
            name='edit_' + name),
        url(r'^korekta/$',
            review.as_view(),
            name='review_' + name),
        url(r'^zatwierdz/$',
            approve.as_view(),
            name='approve_' + name),
    ]


def view_edit_review_approve(name, view, edit, review, approve):
    """Returns the standard scheme of four views for a content item type."""
    return [
        url(r'^$', view.as_view(), name='view_' + name),
    ] + edit_review_approve(name, edit, review, approve)
