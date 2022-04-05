module products {
    type Category {
        required property name -> str {
            constraint exclusive;
        };
        multi link products := .<category[is Product];
    }

    type Product {
        required property name -> str {
            constraint exclusive;
        };
        required link category -> Category {
            on target delete delete source;
        };
        required property image_url -> str;
        multi link variants := .<product[is ProductVariant];
    }

    type ProductVariant {
        required property name -> str;
        required property weight -> decimal {
            constraint min_ex_value(0.0n);
        }
        required property weight_units -> str;
        required property price -> decimal {
            constraint min_value(0.0n);
        }
        required link product -> Product {
            on target delete delete source;
        };
    }
}
