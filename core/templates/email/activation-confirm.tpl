{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activation Confirm
{% endblock %}

{% block html %}
http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{token}}
{% endblock %}