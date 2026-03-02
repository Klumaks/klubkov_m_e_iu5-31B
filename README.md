# klubkov_m_e_iu5-31B
erDiagram
    user ||--o| user_profile : has
    user ||--o{ user_role : has
    user ||--o| trainer_details : has
    user ||--o| client_details : has

    sport_category ||--o{ trainer_category : includes
    user ||--o{ trainer_category : belongs_to

    user ||--o{ subscription_tier : creates
    subscription_tier ||--o{ tier_feature : contains
    feature_dictionary ||--o{ tier_feature : included_in

    user ||--o{ user_subscription : purchases_as_client
    subscription_tier ||--o{ user_subscription : granted_by_tier

    user ||--o{ post : authors_as_trainer
    subscription_tier ||--o{ post : may_gate_access
    post ||--o{ post_attachment : has_files

    user ||--o{ chat : as_client
    user ||--o{ chat : as_trainer

    chat ||--o{ message : contains
    user ||--o{ message : sends
    message ||--o{ message_attachment : has_files

    user_subscription ||--o{ payment : billed_by
    payment ||--o{ refund : may_have
    user ||--o{ payout : withdraws

    user {
        bigint id PK
        text email UK "NOT NULL"
        text password_hash "NOT NULL"
        timestamp created_at "NOT NULL, DEFAULT now()"
        timestamp updated_at "NOT NULL, DEFAULT now()"
    }

    user_profile {
        bigint user_id PK, FK "-> user.id"
        text first_name "NOT NULL"
        text last_name "NOT NULL"
        text bio "NULL"
        text avatar_url "NULL"
    }

    user_role {
        bigint user_id PK, FK "-> user.id"
        text role PK "NOT NULL, CHECK (role IN ('trainer','client','admin'))"
        timestamp created_at "NOT NULL, DEFAULT now()"
    }

    trainer_details {
        bigint user_id PK, FK "-> user.id"
        integer experience_years "NULL, CHECK (experience_years >= 0)"
        text sports_rank "NULL"
        text education_degree "NULL"
    }

    client_details {
        bigint user_id PK, FK "-> user.id"
        text fitness_goal "NULL"
    }

    sport_category {
        bigint id PK
        text name UK "NOT NULL"
    }

    trainer_category {
        bigint trainer_id PK, FK "-> user.id"
        bigint category_id PK, FK "-> sport_category.id"
    }

    subscription_tier {
        bigint id PK
        bigint trainer_id FK "NOT NULL -> user.id"
        text title "NOT NULL"
        text description "NULL"
        text price_currency "NOT NULL, DEFAULT 'RUB'"
        bigint price_integer "NOT NULL, CHECK (price_integer >= 0)"
        integer price_fraction "NOT NULL, CHECK (price_fraction BETWEEN 0 AND 99)"
        integer level_rank "NOT NULL, CHECK (level_rank > 0), UNIQUE (trainer_id, level_rank)"
    }

    feature_dictionary {
        bigint id PK
        text code_name UK "NOT NULL"
        text description "NOT NULL"
    }

    tier_feature {
        bigint tier_id PK, FK "-> subscription_tier.id"
        bigint feature_id PK, FK "-> feature_dictionary.id"
    }

    user_subscription {
        bigint id PK
        bigint client_id FK "NOT NULL -> user.id"
        bigint tier_id FK "NOT NULL -> subscription_tier.id"
        text status "NOT NULL, CHECK (status IN ('active','expired','cancelled'))"
        timestamp started_at "NOT NULL"
        timestamp expires_at "NOT NULL"
        timestamp cancelled_at "NULL"
    }

    post {
        bigint id PK
        bigint trainer_id FK "NOT NULL -> user.id"
        bigint min_tier_id FK "NULL -> subscription_tier.id"
        text title "NOT NULL"
        text text_content "NOT NULL"
        timestamp created_at "NOT NULL, DEFAULT now()"
        timestamp updated_at "NOT NULL, DEFAULT now()"
    }

    post_attachment {
        bigint id PK
        bigint post_id FK "NOT NULL -> post.id"
        text file_url "NOT NULL"
        text kind "NOT NULL, CHECK (kind IN ('image','video','document'))"
        text mime_type "NOT NULL"
    }

    chat {
        bigint id PK
        bigint client_id FK "NOT NULL -> user.id"
        bigint trainer_id FK "NOT NULL -> user.id"
        bigint client_last_read_message_id "NULL -> message.id"
        bigint trainer_last_read_message_id "NULL -> message.id"
        timestamp created_at "NOT NULL, DEFAULT now()"
    }

    message {
        bigint id PK
        bigint chat_id FK "NOT NULL -> chat.id"
        bigint sender_id FK "NOT NULL -> user.id"
        text text_content "NULL"
        timestamp created_at "NOT NULL, DEFAULT now()"
        timestamp updated_at "NOT NULL, DEFAULT now()"
    }

    message_attachment {
        bigint id PK
        bigint message_id FK "NOT NULL -> message.id"
        text file_url "NOT NULL"
        text kind "NOT NULL, CHECK (kind IN ('image','video','document'))"
        text mime_type "NOT NULL"
    }

    payment {
        bigint id PK
        bigint subscription_id FK "NOT NULL -> user_subscription.id"
        bigint client_id FK "NOT NULL -> user.id"
        bigint trainer_id FK "NOT NULL -> user.id"
        text amount_currency "NOT NULL, DEFAULT 'RUB'"
        bigint amount_integer "NOT NULL, CHECK (amount_integer >= 0)"
        integer amount_fraction "NOT NULL, CHECK (amount_fraction BETWEEN 0 AND 99)"
        text status "NOT NULL, CHECK (status IN ('pending','paid','failed'))"
        text provider "NULL"
        text provider_ref "NULL"
        timestamp created_at "NOT NULL, DEFAULT now()"
    }

    refund {
        bigint id PK
        bigint payment_id FK "NOT NULL -> payment.id"
        text amount_currency "NOT NULL, DEFAULT 'RUB'"
        bigint amount_integer "NOT NULL, CHECK (amount_integer >= 0)"
        integer amount_fraction "NOT NULL, CHECK (amount_fraction BETWEEN 0 AND 99)"
        text status "NOT NULL, CHECK (status IN ('pending','refunded','failed'))"
        timestamp created_at "NOT NULL, DEFAULT now()"
    }

    payout {
        bigint id PK
        bigint trainer_id FK "NOT NULL -> user.id"
        text amount_currency "NOT NULL, DEFAULT 'RUB'"
        bigint amount_integer "NOT NULL, CHECK (amount_integer >= 0)"
        integer amount_fraction "NOT NULL, CHECK (amount_fraction BETWEEN 0 AND 99)"
        text status "NOT NULL, CHECK (status IN ('pending','paid','failed'))"
        text provider "NULL"
        text provider_ref "NULL"
        timestamp created_at "NOT NULL, DEFAULT now()"
    }

