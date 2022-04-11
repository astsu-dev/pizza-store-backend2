module orders {
    scalar type OrderStatus extending enum<UNCOMPLETED, COMPLETED, CANCELLED>;

    type OrderItem {
        required link product_variant -> products::ProductVariant;
        required property amount -> int16 {
            constraint min_ex_value(0);    
        }
        required link customer_order -> CustomerOrder {
            on target delete delete source;
        }
    }

    type CustomerOrder {
        required property phone -> str;
        required property address -> str;
        required property status -> OrderStatus {
            default := OrderStatus.UNCOMPLETED;
        }
        required property note -> str {
            default := "";
        }
        required property created_at -> datetime {
            default := datetime_current();
        }
        multi link items := .<customer_order[is OrderItem];
    }
}
