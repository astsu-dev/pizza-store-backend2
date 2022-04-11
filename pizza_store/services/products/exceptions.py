class CategoryAlreadyExistsError(Exception):
    """Will be raised on try to create already exist category."""


class CategoryNotFoundError(Exception):
    """Will be raised if category does not exist."""


class ProductAlreadyExistsError(Exception):
    """Will be raised on try to create already exist product."""


class ProductNotFoundError(Exception):
    """Will be raised if product does not exist."""


class ProductVariantNotFoundError(Exception):
    """Will be raised if product variant does not exist."""
