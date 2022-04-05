module orders {
    type CustomerOrder {
        required property phone -> str;
        required multi link products -> products::ProductVariant;
        property note -> str {
            default := "";
        };
    }
}
