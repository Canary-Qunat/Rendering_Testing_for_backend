-- Create tokens table
CREATE TABLE IF NOT EXISTS tokens(
    id SERIAL PRIMARY KEY,
    access_token VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    expired_at TIMESTAMP NOT NULL
);

-- Create indexes for better query performance
-- FIX: Changed 'token' to 'tokens' to match table name
CREATE INDEX IF NOT EXISTS idx_tokens_created_at ON tokens(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_tokens_expired_at ON tokens(expired_at);

-- Optional: Add comments for documentation
COMMENT ON TABLE tokens IS 'Stores Zerodha OAuth access tokens with expiration tracking';
COMMENT ON COLUMN tokens.access_token IS 'Zerodha API access token';
COMMENT ON COLUMN tokens.created_at IS 'Token creation timestamp';
COMMENT ON COLUMN tokens.expired_at IS 'Token expiration timestamp (6 AM next day)';