CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    bio TEXT,
    photo_url VARCHAR(255),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    resume_url VARCHAR(255)
);

CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    skill_name VARCHAR(50) NOT NULL,
    description TEXT,
    proficiency_level INTEGER CHECK (proficiency_level >= 1 AND proficiency_level <= 5)
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    image_url VARCHAR(255),
    project_url VARCHAR(255),
    date_completed DATE
);

CREATE TABLE blogposts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    date_published TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE posttags (
    post_id INTEGER NOT NULL REFERENCES blogposts(id),
    tag_id INTEGER NOT NULL REFERENCES tags(id),
    PRIMARY KEY (post_id, tag_id)
);

CREATE TABLE projecttags (
    project_id INTEGER NOT NULL REFERENCES projects(id),
    tag_id INTEGER NOT NULL REFERENCES tags(id),
    PRIMARY KEY (project_id, tag_id)
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    date_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(20) NOT NULL
);

CREATE TABLE socialmedia (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    platform_name VARCHAR(50) NOT NULL,
    profile_url VARCHAR(255) NOT NULL
);

CREATE TABLE testimonials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    quote TEXT NOT NULL,
    author VARCHAR(100) NOT NULL,
    date DATE
);

CREATE TABLE telegramsubscribers (
    id SERIAL PRIMARY KEY,
    telegram_user_id VARCHAR(50) NOT NULL UNIQUE,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subscriberpreferences (
    id SERIAL PRIMARY KEY,
    telegram_user_id VARCHAR(50) NOT NULL REFERENCES telegramsubscribers(telegram_user_id),
    notification_type VARCHAR(50) NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE
);

CREATE TABLE polls (
    id SERIAL PRIMARY KEY,
    telegram_user_id VARCHAR(50) NOT NULL REFERENCES telegramsubscribers(telegram_user_id),
    question TEXT NOT NULL,
    answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE education (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    institution VARCHAR(100) NOT NULL,
    degree VARCHAR(100),
    field_of_study VARCHAR(100),
    start_date DATE,
    end_date DATE
);

CREATE TABLE workexperience (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    company VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE
);

CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    page_url VARCHAR(255) NOT NULL,
    visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    session_id VARCHAR(50),
    action VARCHAR(50),
    duration INTEGER
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mlpredictions (
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES messages(id),
    input_text TEXT NOT NULL,
    prediction TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для оптимизации
CREATE INDEX idx_analytics_visit_time ON analytics(visit_time);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_messages_date_sent ON messages(date_sent);