-- Drop tables if they exist
DROP TABLE IF EXISTS tool_usage_feedback;
DROP TABLE IF EXISTS recommended_tools;
DROP TABLE IF EXISTS cad_feature_types;
DROP TABLE IF EXISTS cad_features;
DROP TABLE IF EXISTS cad_files;
DROP TABLE IF EXISTS tools;
DROP TABLE IF EXISTS machines;

-- Create machines table
CREATE TABLE machines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model VARCHAR(255),
    manufacturer VARCHAR(255),
    max_rpm INTEGER,
    max_feed_rate NUMERIC(10, 2),
    spindle_power NUMERIC(10, 2),
    max_tool_diameter NUMERIC(10, 2),
    min_tool_diameter NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tools table
CREATE TABLE tools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    material VARCHAR(100),
    diameter NUMERIC(10, 2),
    flute_count INTEGER,
    overall_length NUMERIC(10, 2),
    cutting_length NUMERIC(10, 2),
    shank_diameter NUMERIC(10, 2),
    max_doc NUMERIC(10, 2),
    max_rpm INTEGER,
    manufacturer VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create CAD files table
CREATE TABLE cad_files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_size BIGINT,
    file_format VARCHAR(10),
    parsed BOOLEAN DEFAULT FALSE,
    parsed_data_path VARCHAR(512)
);

-- Create CAD features table
CREATE TABLE cad_features (
    id SERIAL PRIMARY KEY,
    cad_file_id INTEGER REFERENCES cad_files(id) ON DELETE CASCADE,
    feature_name VARCHAR(255),
    x_position NUMERIC(10, 2),
    y_position NUMERIC(10, 2),
    z_position NUMERIC(10, 2),
    width NUMERIC(10, 2),
    height NUMERIC(10, 2),
    depth NUMERIC(10, 2),
    radius NUMERIC(10, 2),
    angle NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create CAD feature types table
CREATE TABLE cad_feature_types (
    id SERIAL PRIMARY KEY,
    cad_feature_id INTEGER REFERENCES cad_features(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'hole', 'slot', 'pocket', 'chamfer', etc.
    confidence NUMERIC(5, 2), -- 0-100% confidence of classification
    classified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create recommended tools table
CREATE TABLE recommended_tools (
    id SERIAL PRIMARY KEY,
    cad_file_id INTEGER REFERENCES cad_files(id) ON DELETE CASCADE,
    tool_id INTEGER REFERENCES tools(id) ON DELETE CASCADE,
    operation_type VARCHAR(50) NOT NULL, -- 'roughing', 'finishing', 'drilling'
    recommended_speed NUMERIC(10, 2),
    recommended_feed NUMERIC(10, 2),
    adjusted_speed NUMERIC(10, 2),
    adjusted_feed NUMERIC(10, 2),
    wear_score INTEGER, -- 1-10 scale
    recommendation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tool usage feedback table
CREATE TABLE tool_usage_feedback (
    id SERIAL PRIMARY KEY,
    recommended_tool_id INTEGER REFERENCES recommended_tools(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL, -- 1-5 scale
    comments TEXT,
    feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_cad_features_cad_file_id ON cad_features(cad_file_id);
CREATE INDEX idx_cad_feature_types_cad_feature_id ON cad_feature_types(cad_feature_id);
CREATE INDEX idx_recommended_tools_cad_file_id ON recommended_tools(cad_file_id);
CREATE INDEX idx_recommended_tools_tool_id ON recommended_tools(tool_id);
CREATE INDEX idx_tool_usage_feedback_recommended_tool_id ON tool_usage_feedback(recommended_tool_id); 