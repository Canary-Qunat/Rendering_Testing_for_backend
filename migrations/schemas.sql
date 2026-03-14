CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS refresh_tokens (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS positions(
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFRENCES users(id) ON DELETE CASCADE,
    trading_symbol      VARCHAR(50) NOT NULL,
    exchange            VARCHAR(10) NOT NULL,
    quantity            INTEGER NOT NULL,
    avg_price           NUMERIC(12,4) NOT NULL,
    last_price          NUMERIC(12,4) NOT NULL,
    pnl                 NUMERIC(14,4) NOT NULL,
    pnl_percent         NUMERIC(8,4) NOT NULL,
    product             VARCHAR(10) NOT NULL,
    synced_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
