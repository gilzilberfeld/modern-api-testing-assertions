TOKENS = {
    "token-user-1": "user-1",
    "token-user-2": "user-2",
    "token-user-3": "user-3",
}


def get_user_id(request):
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:]
        return TOKENS.get(token)
    return None
