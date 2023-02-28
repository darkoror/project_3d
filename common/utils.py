from project_3d.settings import SITE_URL


def build_url(scheme, path, uid, token):
    """
    Build url to send it in email
    """
    return f'{scheme}://{SITE_URL}{path}?token={uid}.{token}'
