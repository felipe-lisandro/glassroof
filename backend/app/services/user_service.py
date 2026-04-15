from app import db
from app.models.user import EnterpriseUser, PersonUser, User


class DuplicateError(Exception):
    """Raised when a unique field already exists."""


def create_person_user(data: dict) -> dict:
    if User.query.filter_by(email=data["email"]).first():
        raise DuplicateError("Email já cadastrado")
    if PersonUser.query.filter_by(cpf=data["cpf"]).first():
        raise DuplicateError("CPF já cadastrado")

    user = PersonUser(
        name=data["name"],
        email=data["email"],
        cpf=data["cpf"],
        last_name=data.get("last_name"),
        birthday=data.get("birthday"),
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()
    return user.to_dict()


def create_enterprise_user(data: dict) -> dict:
    if User.query.filter_by(email=data["email"]).first():
        raise DuplicateError("Email já cadastrado")
    if EnterpriseUser.query.filter_by(cnpj=data["cnpj"]).first():
        raise DuplicateError("CNPJ já cadastrado")

    user = EnterpriseUser(
        name=data["name"],
        email=data["email"],
        cnpj=data["cnpj"],
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()
    return user.to_dict()


def get_all_users() -> list[dict]:
    users = User.query.all()
    return [u.to_dict() for u in users]


def get_user_by_id(user_id: int) -> dict | None:
    user = db.session.get(User, user_id)
    return user.to_dict() if user else None
