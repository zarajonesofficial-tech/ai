-- CHRIZ__3656 AI Database Schema

-- 1. Enums
CREATE TYPE user_role AS ENUM ('admin', 'moderator', 'user');
CREATE TYPE op_status AS ENUM ('online', 'maintenance', 'offline');
CREATE TYPE job_status AS ENUM ('pending', 'running', 'completed', 'failed');
CREATE TYPE ticket_status AS ENUM ('open', 'closed', 'escalated');

-- 2. Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    discord_id TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    role user_role DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Operational State Table
CREATE TABLE IF NOT EXISTS operational_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status op_status DEFAULT 'online',
    active_events JSONB DEFAULT '[]'::jsonb,
    owner_available BOOLEAN DEFAULT true,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Initialize operational state if empty
INSERT INTO operational_state (status, active_events, owner_available)
SELECT 'online', '[]'::jsonb, true
WHERE NOT EXISTS (SELECT 1 FROM operational_state);

-- 4. Knowledge Base Table
CREATE TABLE IF NOT EXISTS knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536), -- Adjust dimensions based on model (e.g., 1536 for OpenAI, 1024 for others)
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 5. Automation Jobs Table
CREATE TABLE IF NOT EXISTS automation_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_type TEXT NOT NULL,
    payload JSONB DEFAULT '{}'::jsonb,
    status job_status DEFAULT 'pending',
    result JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 6. Tickets Table
CREATE TABLE IF NOT EXISTS tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    status ticket_status DEFAULT 'open',
    summary TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 7. AI Conversations Table
CREATE TABLE IF NOT EXISTS ai_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT UNIQUE NOT NULL,
    history JSONB DEFAULT '[]'::jsonb,
    token_usage INTEGER DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 8. Moderation Logs Table
CREATE TABLE IF NOT EXISTS moderation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action TEXT NOT NULL,
    reason TEXT,
    moderator_id UUID REFERENCES users(id),
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE operational_state ENABLE ROW LEVEL SECURITY;
-- ... add more RLS policies as needed for public vs admin access
