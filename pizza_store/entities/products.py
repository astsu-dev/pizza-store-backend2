import uuid
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Category:
    """Product category.

    Attributes:
        id: category id.
        name: category name (example: "Pizzas").
    """

    id: uuid.UUID
    name: str


@dataclass(frozen=True)
class ProductVariant:
    """Product variant.

    Attributes:
        id: product variant id.
        name: product variant name.
        weight: weight of this product variant.
        weight_units: units for `weight`.
        price: price of this product variant.
    """

    id: uuid.UUID
    name: str
    weight: Decimal
    weight_units: str
    price: Decimal


@dataclass(frozen=True)
class ProductWithoutVariants:
    """Product

    Attributes:
        id: product id.
        name: product name (example: name of pizza).
        category: product category.
        image_url: url to product image.
    """

    id: uuid.UUID
    name: str
    category: Category
    image_url: str


@dataclass(frozen=True)
class Product(ProductWithoutVariants):
    """Product

    Attributes:
        id: product id.
        name: product name (example: name of pizza).
        category: product category.
        image_url: url to product image.
        variants: list of product variants.
    """

    variants: list[ProductVariant]


@dataclass(frozen=True)
class ProductVariantWithProduct(ProductVariant):
    """Product variant with info about product.

    Attributes:
        id: product variant id.
        name: product variant name.
        weight: weight of this product variant.
        weight_units: units for `weight`.
        price: price of this product variant.
        product: product info.
    """

    product: ProductWithoutVariants
