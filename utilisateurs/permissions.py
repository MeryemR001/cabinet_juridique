from __future__ import annotations

from typing import Any, Final, TypedDict


class SidebarItem(TypedDict):
    label: str
    icon: str
    url_name: str
    permission: str | None


ROLE_LABELS: Final[dict[str, str]] = {
    'admin': 'Administrateur',
    'avocat': 'Avocat',
    'assistante': 'Assistante',
}

# Single source of truth for role permissions by action key.
VIEW_PERMISSIONS: Final[dict[str, set[str]]] = {
    # Dashboard
    'dashboard.admin': {'admin'},
    'dashboard.avocat': {'avocat'},
    'dashboard.assistante': {'assistante'},

    # Utilisateurs
    'utilisateurs.list': {'admin'},
    'utilisateurs.create': {'admin'},
    'utilisateurs.update': {'admin'},
    'utilisateurs.delete': {'admin'},

    # Dossiers
    'dossiers.list': {'admin', 'assistante', 'avocat'},
    'dossiers.create': {'admin', 'assistante'},
    'dossiers.update': {'admin', 'assistante'},
    'dossiers.delete': {'admin'},

    # Clients
    'clients.list': {'admin', 'assistante'},
    'clients.detail': {'admin', 'assistante'},
    'clients.create': {'admin', 'assistante'},
    'clients.update': {'admin', 'assistante'},
    'clients.delete': {'admin', 'assistante'},

    # Interventions
    'interventions.list': {'admin', 'assistante', 'avocat'},
    'interventions.add': {'admin', 'assistante', 'avocat'},
    'interventions.detail': {'admin', 'assistante', 'avocat'},
    'interventions.delete': {'admin'},

    # Audiences
    'audiences.list': {'admin', 'assistante', 'avocat'},
    'audiences.create': {'admin', 'avocat'},
    'audiences.update': {'admin', 'avocat'},
    'audiences.delete': {'admin'},

    # Factures
    'factures.list': {'admin', 'assistante', 'avocat'},
    'factures.detail': {'admin', 'assistante', 'avocat'},
    'factures.create': {'admin', 'avocat'},
    'factures.update': {'admin', 'avocat'},
    'factures.delete': {'admin'},
    'factures.print': {'admin', 'assistante', 'avocat'},

    # Documents
    'documents.list': {'admin', 'assistante', 'avocat'},
    'documents.upload': {'admin', 'assistante'},
    'documents.download': {'admin', 'assistante', 'avocat'},
    'documents.delete': {'admin', 'assistante'},
}

DASHBOARD_URL_BY_ROLE: Final[dict[str, str]] = {
    'admin': 'dashboard:admin',
    'avocat': 'dashboard:avocat',
    'assistante': 'dashboard:assistante',
}

DEFAULT_ROLE_LABEL: Final[str] = 'Utilisateur'
DEFAULT_DASHBOARD_URL: Final[str] = 'utilisateurs:login'

# Sidebar links are also centralized here for easy maintenance.
SIDEBAR_ITEMS: Final[tuple[SidebarItem, ...]] = (
    {'label': 'Utilisateurs', 'icon': 'badge', 'url_name': 'utilisateurs:liste', 'permission': 'utilisateurs.list'},
    {'label': 'Clients', 'icon': 'group', 'url_name': 'dossiers:liste_clients', 'permission': 'clients.list'},
    {'label': 'Dossiers', 'icon': 'folder_shared', 'url_name': 'dossiers:liste', 'permission': 'dossiers.list'},
    {'label': 'Interventions', 'icon': 'work_history', 'url_name': 'dossiers:liste_interventions', 'permission': 'interventions.list'},
    {'label': 'Audiences', 'icon': 'gavel', 'url_name': 'audiences:liste', 'permission': 'audiences.list'},
    {'label': 'Factures', 'icon': 'receipt_long', 'url_name': 'factures:liste', 'permission': 'factures.list'},
)


def _normalize_role_name(role: Any) -> Any:
    if isinstance(role, str):
        return role.strip().lower()
    return role


def get_user_role(user: Any) -> Any:
    return _normalize_role_name(getattr(user, 'role', None))


def has_role(user: Any, *roles: str) -> bool:
    normalized_roles = {role.strip().lower() for role in roles if isinstance(role, str)}
    return get_user_role(user) in normalized_roles


def has_permission(user: Any, permission_key: str) -> bool:
    if not getattr(user, 'is_authenticated', False):
        return False
    if getattr(user, 'is_superuser', False):
        return True

    allowed_roles = VIEW_PERMISSIONS.get(permission_key, set())
    return get_user_role(user) in allowed_roles


def get_role_label(user: Any) -> str:
    return ROLE_LABELS.get(get_user_role(user), DEFAULT_ROLE_LABEL)


def get_dashboard_url_name(user: Any) -> str:
    return DASHBOARD_URL_BY_ROLE.get(get_user_role(user), DEFAULT_DASHBOARD_URL)


def get_sidebar_items(user: Any) -> list[SidebarItem]:
    if not getattr(user, 'is_authenticated', False):
        return []

    items: list[SidebarItem] = [
        {
            'label': 'Dashboard',
            'icon': 'dashboard',
            'url_name': get_dashboard_url_name(user),
            'permission': None,
        }
    ]

    for item in SIDEBAR_ITEMS:
        if has_permission(user, item['permission']):
            items.append(item)

    return items
