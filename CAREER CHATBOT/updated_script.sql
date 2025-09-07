-- CBE Career Guide Database Setup Script
-- Run this script in your Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create user profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    school TEXT,
    grade TEXT,
    date_of_birth DATE,
    phone_number TEXT,
    county TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create assessment results table
CREATE TABLE IF NOT EXISTS assessment_results (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    pathway_recommendation TEXT NOT NULL,
    interests JSONB,
    environment_preference TEXT,
    score INTEGER DEFAULT 0,
    assessment_type TEXT DEFAULT 'career_pathway',
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create career interactions table
CREATE TABLE IF NOT EXISTS career_interactions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    career_name TEXT NOT NULL,
    pathway TEXT,
    interaction_type TEXT DEFAULT 'view',
    interaction_data JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user activities table
CREATE TABLE IF NOT EXISTS user_activities (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    activity_type TEXT NOT NULL,
    activity_data JSONB,
    page_visited TEXT,
    session_id TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create chat conversations table
CREATE TABLE IF NOT EXISTS chat_conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    response TEXT,
    conversation_context JSONB,
    language TEXT DEFAULT 'en',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create scenarios progress table
CREATE TABLE IF NOT EXISTS scenarios_progress (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    scenario_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    progress_data JSONB,
    completed BOOLEAN DEFAULT FALSE,
    score INTEGER DEFAULT 0,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create resources downloads table
CREATE TABLE IF NOT EXISTS resource_downloads (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    resource_name TEXT NOT NULL,
    resource_type TEXT,
    resource_url TEXT,
    download_count INTEGER DEFAULT 1,
    last_downloaded TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    achievement_type TEXT NOT NULL,
    achievement_name TEXT NOT NULL,
    achievement_description TEXT,
    achievement_data JSONB,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create pathway preferences table
CREATE TABLE IF NOT EXISTS pathway_preferences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    pathway_type TEXT NOT NULL,
    preference_score INTEGER DEFAULT 0,
    subjects_interested JSONB,
    career_goals TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create API configurations table (for storing Gemini API and other service keys)
CREATE TABLE IF NOT EXISTS api_configurations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    service_name TEXT NOT NULL UNIQUE,
    api_key TEXT NOT NULL,
    api_url TEXT,
    configuration JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create chat sessions table for better conversation management
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    session_name TEXT DEFAULT 'New Chat',
    total_messages INTEGER DEFAULT 0,
    last_message_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Update chat_conversations to link to sessions
ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE;

-- Row Level Security policies
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE career_interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE scenarios_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE resource_downloads ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE pathway_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_configurations ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;

-- Policies for user_profiles
CREATE POLICY "Users can view own profile" ON user_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own profile" ON user_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own profile" ON user_profiles FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own profile" ON user_profiles FOR DELETE USING (auth.uid() = user_id);

-- Policies for assessment_results
CREATE POLICY "Users can view own assessments" ON assessment_results FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own assessments" ON assessment_results FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own assessments" ON assessment_results FOR UPDATE USING (auth.uid() = user_id);

-- Policies for career_interactions
CREATE POLICY "Users can view own interactions" ON career_interactions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own interactions" ON career_interactions FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for user_activities
CREATE POLICY "Users can view own activities" ON user_activities FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own activities" ON user_activities FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for chat_conversations
CREATE POLICY "Users can view own conversations" ON chat_conversations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own conversations" ON chat_conversations FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own conversations" ON chat_conversations FOR UPDATE USING (auth.uid() = user_id);

-- Policies for scenarios_progress
CREATE POLICY "Users can view own scenarios progress" ON scenarios_progress FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own scenarios progress" ON scenarios_progress FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own scenarios progress" ON scenarios_progress FOR UPDATE USING (auth.uid() = user_id);

-- Policies for resource_downloads
CREATE POLICY "Users can view own downloads" ON resource_downloads FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own downloads" ON resource_downloads FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own downloads" ON resource_downloads FOR UPDATE USING (auth.uid() = user_id);

-- Policies for user_achievements
CREATE POLICY "Users can view own achievements" ON user_achievements FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own achievements" ON user_achievements FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for pathway_preferences
CREATE POLICY "Users can view own pathway preferences" ON pathway_preferences FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own pathway preferences" ON pathway_preferences FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own pathway preferences" ON pathway_preferences FOR UPDATE USING (auth.uid() = user_id);

-- Policies for api_configurations (admin only - no user access)
CREATE POLICY "Only service role can access API configs" ON api_configurations FOR ALL USING (auth.role() = 'service_role');

-- Policies for chat_sessions
CREATE POLICY "Users can view own chat sessions" ON chat_sessions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own chat sessions" ON chat_sessions FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own chat sessions" ON chat_sessions FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own chat sessions" ON chat_sessions FOR DELETE USING (auth.uid() = user_id);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_assessment_results_user_id ON assessment_results(user_id);
CREATE INDEX IF NOT EXISTS idx_career_interactions_user_id ON career_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_conversations_user_id ON chat_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_scenarios_progress_user_id ON scenarios_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_resource_downloads_user_id ON resource_downloads(user_id);
CREATE INDEX IF NOT EXISTS idx_user_achievements_user_id ON user_achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_pathway_preferences_user_id ON pathway_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_api_configurations_service_name ON api_configurations(service_name);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_conversations_session_id ON chat_conversations(session_id);

-- Create timestamp indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_assessment_results_created_at ON assessment_results(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_career_interactions_timestamp ON career_interactions(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_user_activities_timestamp ON user_activities(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_chat_conversations_timestamp ON chat_conversations(timestamp DESC);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pathway_preferences_updated_at BEFORE UPDATE ON pathway_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_api_configurations_updated_at BEFORE UPDATE ON api_configurations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert API configurations (run this after creating the tables)
INSERT INTO api_configurations (service_name, api_key, api_url, configuration, is_active) VALUES
('gemini', 'AIzaSyDumlwe8yV6zJdTqUx9CW2lD_D-upVPjUQ', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent', 
 '{"temperature": 0.7, "topK": 40, "topP": 0.95, "maxOutputTokens": 1024}', true)
ON CONFLICT (service_name) DO UPDATE SET
    api_key = EXCLUDED.api_key,
    api_url = EXCLUDED.api_url,
    configuration = EXCLUDED.configuration,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- Insert some sample data for testing (optional)
-- You can uncomment these if you want sample data

/*
-- Sample CBE pathways data
INSERT INTO pathway_preferences (user_id, pathway_type, preference_score, subjects_interested, career_goals) VALUES
(auth.uid(), 'STEM', 85, '["Mathematics", "Physics", "Chemistry", "Biology"]', 'Become a software engineer'),
(auth.uid(), 'Social Sciences', 70, '["History", "Geography", "English", "Kiswahili"]', 'Work in journalism'),
(auth.uid(), 'Arts & Sports', 60, '["Art", "Music", "Physical Education"]', 'Become a professional artist'),
(auth.uid(), 'Technical', 75, '["Technical Drawing", "Woodwork", "Metalwork"]', 'Work in construction');

-- Sample achievements
INSERT INTO user_achievements (user_id, achievement_type, achievement_name, achievement_description) VALUES
(auth.uid(), 'assessment', 'First Assessment Complete', 'Completed your first career assessment'),
(auth.uid(), 'exploration', 'Career Explorer', 'Explored 10 different careers'),
(auth.uid(), 'learning', 'Quick Learner', 'Completed 5 learning scenarios');
*/

-- Create a view for user dashboard statistics
CREATE OR REPLACE VIEW user_dashboard_stats AS
SELECT 
    u.user_id,
    COUNT(DISTINCT a.id) as total_assessments,
    COUNT(DISTINCT c.id) as careers_explored,
    COUNT(DISTINCT s.id) as scenarios_completed,
    COUNT(DISTINCT r.id) as resources_downloaded,
    COUNT(DISTINCT ac.id) as achievements_earned,
    MAX(ua.timestamp) as last_activity
FROM user_profiles u
LEFT JOIN assessment_results a ON u.user_id = a.user_id
LEFT JOIN career_interactions c ON u.user_id = c.user_id
LEFT JOIN scenarios_progress s ON u.user_id = s.user_id AND s.completed = true
LEFT JOIN resource_downloads r ON u.user_id = r.user_id
LEFT JOIN user_achievements ac ON u.user_id = ac.user_id
LEFT JOIN user_activities ua ON u.user_id = ua.user_id
GROUP BY u.user_id;

-- Grant necessary permissions
GRANT SELECT ON user_dashboard_stats TO authenticated;

-- Create a function to get user progress
CREATE OR REPLACE FUNCTION get_user_progress(user_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_assessments', COALESCE(total_assessments, 0),
        'careers_explored', COALESCE(careers_explored, 0),
        'scenarios_completed', COALESCE(scenarios_completed, 0),
        'resources_downloaded', COALESCE(resources_downloaded, 0),
        'achievements_earned', COALESCE(achievements_earned, 0),
        'last_activity', last_activity
    ) INTO result
    FROM user_dashboard_stats
    WHERE user_id = user_uuid;
    
    RETURN COALESCE(result, '{"total_assessments":0,"careers_explored":0,"scenarios_completed":0,"resources_downloaded":0,"achievements_earned":0,"last_activity":null}'::JSON);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create a function to get API configuration (for frontend use)
CREATE OR REPLACE FUNCTION get_api_config(service_name_param TEXT)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'api_key', api_key,
        'api_url', api_url,
        'configuration', configuration,
        'is_active', is_active
    ) INTO result
    FROM api_configurations
    WHERE service_name = service_name_param AND is_active = true;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create a function to create or get chat session
CREATE OR REPLACE FUNCTION get_or_create_chat_session(user_uuid UUID, session_name_param TEXT DEFAULT 'New Chat')
RETURNS UUID AS $$
DECLARE
    session_uuid UUID;
BEGIN
    -- Try to get the most recent session for the user
    SELECT id INTO session_uuid
    FROM chat_sessions
    WHERE user_id = user_uuid
    ORDER BY last_message_at DESC
    LIMIT 1;
    
    -- If no session exists, create a new one
    IF session_uuid IS NULL THEN
        INSERT INTO chat_sessions (user_id, session_name)
        VALUES (user_uuid, session_name_param)
        RETURNING id INTO session_uuid;
    END IF;
    
    RETURN session_uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permission on the functions
GRANT EXECUTE ON FUNCTION get_user_progress(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_api_config(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION get_or_create_chat_session(UUID, TEXT) TO authenticated;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'CBE Career Guide database setup completed successfully!';
    RAISE NOTICE 'All tables, policies, indexes, and functions have been created.';
    RAISE NOTICE 'Your application is now ready to use with Supabase.';
END $$;