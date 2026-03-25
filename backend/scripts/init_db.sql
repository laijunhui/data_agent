-- 创建 sessions 表
CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(255) PRIMARY KEY,
    tenant_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) DEFAULT '新会话',
    user_id VARCHAR(255),
    is_shared BOOLEAN DEFAULT FALSE,
    share_token VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建 messages 表
CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(255) PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    content TEXT,
    metadata TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建 agent_logs 表
CREATE TABLE IF NOT EXISTS agent_logs (
    id VARCHAR(255) PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    request_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    step VARCHAR(50) NOT NULL,
    content TEXT,
    duration_ms INTEGER
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
CREATE INDEX IF NOT EXISTS idx_logs_session ON agent_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_logs_request ON agent_logs(request_id);
CREATE INDEX IF NOT EXISTS idx_sessions_tenant ON sessions(tenant_id);

-- 创建 Storage Bucket
INSERT INTO storage.buckets (id, name, public) VALUES ('files', 'files', true);