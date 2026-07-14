from __future__ import annotations

from app import db
from app.exceptions import BadRequest, NotFound
from app.models.category import Category
from app.models.property import Property
from app.models.user import User


class AvaliationValidationStrategy:
    def validate(self, *args, **kwargs):
        raise NotImplementedError("Concrete validation strategies must implement validate")

    def _get_property(self, property_id: int) -> Property:
        property_obj = db.session.get(Property, property_id)
        if not property_obj:
            raise NotFound("Property not found")
        return property_obj

    def _get_person_user(self, user_id: int) -> User:
        try:
            user_id = int(user_id)
        except (TypeError, ValueError) as exc:
            raise BadRequest("user_id must be an integer") from exc

        user_obj = db.session.get(User, user_id)
        if not user_obj:
            raise NotFound("User not found")
        if user_obj.type != "person":
            raise BadRequest("Only person users can create avaliations")
        return user_obj

    def _get_category(self, category_id: int) -> Category:
        try:
            category_id = int(category_id)
        except (TypeError, ValueError) as exc:
            raise BadRequest("category_id must be an integer") from exc

        category_obj = db.session.get(Category, category_id)
        if not category_obj:
            raise NotFound("Category not found")
        return category_obj

    def _validate_comment(self, value: str) -> str:
        comment = (value or "").strip()
        if not comment:
            raise BadRequest("comment is required")
        return comment

    def _validate_stars(self, value) -> int:
        try:
            stars = int(value)
        except (TypeError, ValueError) as exc:
            raise BadRequest("stars must be an integer between 0 and 5") from exc

        if not 0 <= stars <= 5:
            raise BadRequest("stars must be between 0 and 5")
        return stars

    def _validate_photos(self, value):
        photos = value
        if photos is not None and not isinstance(photos, list):
            raise BadRequest("photos must be a list of URLs")
        return photos


class CreateAvaliationValidator(AvaliationValidationStrategy):
    def validate(self, property_id: int, data: dict) -> dict:
        property_obj = self._get_property(property_id)

        user_id = data.get("user_id")
        if user_id is None:
            raise BadRequest("user_id is required")

        category_id = data.get("category_id")
        if category_id is None:
            raise BadRequest("category_id is required")

        return {
            "property": property_obj,
            "user": self._get_person_user(user_id),
            "category": self._get_category(category_id),
            "comment": self._validate_comment(data.get("comment")),
            "stars": self._validate_stars(data.get("stars")),
            "photos": self._validate_photos(data.get("photos")),
        }


class BulkAvaliationValidator(AvaliationValidationStrategy):
    def validate(self, property_id: int, data: dict) -> dict:
        property_obj = self._get_property(property_id)

        user_id = data.get("user_id")
        if user_id is None:
            raise BadRequest("user_id is required")

        items = data.get("avaliations")
        if not isinstance(items, list) or len(items) == 0:
            raise BadRequest("avaliations must be a non-empty list")

        user_obj = self._get_person_user(user_id)
        seen_categories = set()
        formatted_items = []

        for item in items:
            category_id = item.get("category_id")
            if category_id is None:
                raise BadRequest("category_id is required")

            category_obj = self._get_category(category_id)
            if category_obj.id in seen_categories:
                raise BadRequest("category_id must be unique in avaliations list")
            seen_categories.add(category_obj.id)

            formatted_items.append(
                {
                    "category": category_obj,
                    "comment": self._validate_comment(item.get("comment")),
                    "stars": self._validate_stars(item.get("stars")),
                    "photos": self._validate_photos(item.get("photos", [])),
                }
            )

        return {
            "property": property_obj,
            "user": user_obj,
            "avaliations": formatted_items,
        }


class UpdateAvaliationValidator(AvaliationValidationStrategy):
    def validate(self, data: dict) -> dict:
        return {
            "comment": self._validate_comment(data.get("comment")),
            "stars": self._validate_stars(data.get("stars")),
            "photos": self._validate_photos(data.get("photos")) if "photos" in data else None,
        }


class ListAvaliationValidator(AvaliationValidationStrategy):
    def validate(self, property_id: int, stars):
        property_obj = self._get_property(property_id)
        return {
            "property": property_obj,
            "stars": self._validate_stars(stars) if stars is not None else None,
        }


class AvaliationValidationFactory:
    STRATEGIES = {
        "create": CreateAvaliationValidator,
        "bulk": BulkAvaliationValidator,
        "update": UpdateAvaliationValidator,
        "list": ListAvaliationValidator,
    }

    @classmethod
    def get_validator(cls, operation: str) -> AvaliationValidationStrategy:
        strategy_cls = cls.STRATEGIES.get(operation)
        if not strategy_cls:
            raise BadRequest(f"Unknown validation operation: {operation}")
        return strategy_cls()
