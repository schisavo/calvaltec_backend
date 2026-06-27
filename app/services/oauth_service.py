from app.repositories.user_repository import get_user_by_email, create_user
from app.schemas.auth import UserOut

def oauth_login_service(db, user_info):
    email = user_info["email"].lower()
    user = get_user_by_email(db, email)
    if not user:
        user = create_user(
            db,
            email=email,
            password="oauth",  # marcador, no se usa
            name=user_info.get("name", ""),
            role="company",
            company_id=None
        )
    return UserOut.from_orm(user)
