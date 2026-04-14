from datetime import date, datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    register_date = db.Column(db.Date, default=date.today, nullable=False)
    type = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "user",
    }

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "register_date": self.register_date.isoformat(),
            "type": self.type,
        }


class PersonUser(User):
    __mapper_args__ = {"polymorphic_identity": "person"}

    cpf = db.Column(db.String(14), unique=True)
    last_name = db.Column(db.String(120))
    birthday = db.Column(db.Date)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
                "cpf": self.cpf,
                "last_name": self.last_name,
                "birthday": self.birthday.isoformat() if self.birthday else None,
            }
        )
        return data


class EnterpriseUser(User):
    __mapper_args__ = {"polymorphic_identity": "enterprise"}

    cnpj = db.Column(db.String(18), unique=True)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"cnpj": self.cnpj})
        return data
