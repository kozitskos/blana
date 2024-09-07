-- Enable uuid-ossp extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

-- Create notes table
CREATE TABLE notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    owner_id UUID REFERENCES users(id) ON DELETE CASCADE
);

-- Create feedbacks table
CREATE TABLE feedbacks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    comment TEXT,
    rating INTEGER CHECK (rating >= 0 AND rating <= 5),
    note_id UUID REFERENCES notes(id) ON DELETE CASCADE,
    author_id UUID REFERENCES users(id) ON DELETE CASCADE
);

-- Create summaries table
CREATE TABLE summaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    note_id UUID REFERENCES notes(id) ON DELETE CASCADE,
    author_id UUID REFERENCES users(id) ON DELETE CASCADE
);


