from django.urls import reverse, NoReverseMatch

from .permissions import get_role_label, get_sidebar_items


def app_ui_context(request):
    if not request.user.is_authenticated:
        return {}

    sidebar_items = []
    current_path = request.path

    for item in get_sidebar_items(request.user):
        try:
            item_url = reverse(item['url_name'])
        except NoReverseMatch:
            item_url = '#'

        sidebar_items.append({
            **item,
            'url': item_url,
            'active': item_url != '#' and (current_path == item_url or current_path.startswith(item_url.rstrip('/') + '/')),
        })

    return {
        'sidebar_items': sidebar_items,
        'sidebar_role_label': get_role_label(request.user),
    }
