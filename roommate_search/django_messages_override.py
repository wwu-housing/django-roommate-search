import re

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from django_messages.fields import CommaSeparatedUserField
from django_messages.forms import ComposeForm
from django_messages.models import Message
from django_messages.utils import format_quote

from models import Profile


## widgets
class CommaSeparatedProfileInput(forms.widgets.Input):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif isinstance(value, (list, tuple)):
            value = (', '.join([profile.screen_name for profile in value]))
        return super(CommaSeparatedProfileInput, self).render(name, value, attrs)

## fields
class CommaSeparatedProfileField(CommaSeparatedUserField):
    widget = CommaSeparatedProfileInput

    def clean(self, value):
        forms.Field(self).clean(value)
        if not value:
            return ''
        if isinstance(value, (list, tuple)):
            return value

        names = set(value.split(','))
        names_set = set([name.strip() for name in names if name.strip()])
        profiles = list(Profile.objects.filter(screen_name__in=names_set))
        unknown_names = names_set ^ set([profile.screen_name for profile in profiles])

        recipient_filter = self._recipient_filter
        invalid_users = []
        if recipient_filter is not None:
            for r in profiles:
                if recipient_filter(r) is False:
                    users.remove(r)
                    invalid_users.append(r.screen_name)

        if unknown_names or invalid_users:
            raise forms.ValidationError(u"""The following screen names are
                incorrect: %(users)s""" % {'users': ', '.join(list(unknown_names)+invalid_users)})

        users = [profile.user for profile in profiles]
        return users

## forms
class ProfileComposeForm(ComposeForm):
    recipient = CommaSeparatedProfileField(label=u"Recipient")

## views
# Override django_messages compose and reply views to replace User.username
# with Profile.screen_name
@login_required
def compose(request, recipient=None, form_class=ProfileComposeForm,
        template_name='django_messages/compose.html', success_url=None, recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user)
            request.user.message_set.create(
                message=u"Message successfully sent.")
            if success_url is None:
                success_url = reverse('messages_inbox')
            if request.GET.has_key('next'):
                success_url = request.GET['next']
            return redirect(success_url)
    else:
        form = form_class()
        if recipient is not None:
            recipients = [p for p in Profile.objects.filter(screen_name__in=[r.strip() for r in recipient.split('+')])]
            form.fields['recipient'].initial = recipients
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def reply(request, message_id, form_class=ProfileComposeForm,
        template_name='django_messages/compose.html', success_url=None,
        recipient_filter=None, quote_helper=format_quote):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote. To change the quote format
    assign a different ``quote_helper`` kwarg in your url-conf.

    """
    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            request.user.message_set.create(
                message=u"Message successfully sent.")
            if success_url is None:
                success_url = reverse('messages_inbox')
            return redirect(success_url)
    else:
        parent_profile = Profile.objects.get(user=parent.sender)
        # TODO: use util function to strip out many "RE:"
        form = form_class(initial={
            'body': quote_helper(parent_profile.screen_name, parent.body),
            'subject': format_reply_subject(parent.subject),
            'recipient': [parent_profile,]
            })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

## utils
def format_reply_subject(subject):
    """
    Prepends 'Re:' to the subject. To avoid multiple 'Re:'s
    a counter is added.
    """
    subject_prefix_re = r'^Re\[(\d*)\]:\ '
    m = re.match(subject_prefix_re, subject, re.U)
    prefix = u""
    if subject.startswith('Re: '):
        prefix = u"[2]"
        subject = subject[4:]
    elif m is not None:
        try:
            num = int(m.group(1))
            prefix = u"[%d]" % (num+1)
            subject = subject[6+len(str(num)):]
        except:
            # if anything fails here, fall back to the old mechanism
            pass

    return u"Re%(prefix)s: %(subject)s" % {
        'subject': subject,
        'prefix': prefix
    }

