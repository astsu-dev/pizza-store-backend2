module orders {
    scalar type OrderStatus extending enum<UNCOMPLETED, COMPLETED, CANCELLED>;

    type OrderItem {
        required link product_variant -> products::ProductVariant;
        required property amount -> int16 {
            constraint min_ex_value(0);    
        }
    }

    type CustomerOrder {
        required property phone -> str;
        required multi link items -> OrderItem;
        required property status -> OrderStatus {
            default := OrderStatus.UNCOMPLETED;
        }
        property note -> str {
            default := "";
        }
    }
}
