module auth {
    type User {
        required property username -> str {
            constraint exclusive;
        }
        required property password_hash -> str;
        property is_admin -> bool {
            default := false;
        }
    }
}
