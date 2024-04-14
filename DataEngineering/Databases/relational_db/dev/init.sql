ALTER SYSTEM SET wal_level = 'logical';
SELECT pg_reload_conf();

CREATE table event(
    id SERIAL PRIMARY KEY,
    si_id VARCHAR(50),
    group_id VARCHAR(50),
    user_id VARCHAR(50),
    source_id VARCHAR,
    label VARCHAR(50),
    object_id VARCHAR(50),
    bbox VARCHAR,
    confidence VARCHAR(50),
    bucket VARCHAR(50),
    image_path VARCHAR,
    time_stamp BIGINT
    );

-- Create the 'si' table
CREATE TABLE si (
    si_id VARCHAR(50) PRIMARY KEY,
    si_name VARCHAR(50)
);

-- Create the 'groups' table
CREATE TABLE groups (
    group_id VARCHAR(50) PRIMARY KEY,
    group_name VARCHAR(50),
    si_id VARCHAR(50) REFERENCES si(si_id)
);

-- Create the 'users' table
CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    group_id VARCHAR(50) REFERENCES groups(group_id),
    role VARCHAR(50) DEFAULT 'user'
);


CREATE TABLE ai_tags (
    tag_id VARCHAR(50) PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL
);

CREATE TABLE ai_models (
    ai_model_id VARCHAR(50) PRIMARY KEY,
    ai_model_name VARCHAR(50) NOT NULL,
    user_id VARCHAR(50) NOT NULL REFERENCES users(id),
    tag_id VARCHAR(50) NOT NULL REFERENCES ai_tags(tag_id),
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ai_domain VARCHAR(50),
    library VARCHAR(50),
    updated_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by_user VARCHAR(50)
);

CREATE OR REPLACE FUNCTION update_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_date = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_trigger
BEFORE UPDATE ON ai_models
FOR EACH ROW
EXECUTE FUNCTION update_trigger_function();

CREATE TABLE model_cards (
    ai_model_card_id VARCHAR(50) PRIMARY KEY,
    ai_model_id VARCHAR(50) NOT NULL REFERENCES ai_models(ai_model_id) ON DELETE CASCADE,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    path_storage VARCHAR(255) NOT NULL,
    path_config VARCHAR(255) NOT NULL,
    bucket VARCHAR(50)
);


INSERT INTO si (si_id, si_name)
VALUES
  ('si1', 'SI1'),
  ('si2', 'SI2'),
  ('si3', 'SI3'),
  ('si4', 'SI4'),
  ('si5', 'SI5');


INSERT INTO groups (group_id, group_name, si_id)
VALUES
  ('group1', 'GROUP1', 'si1'),
  ('group2', 'GROUP2', 'si2'),
  ('group3', 'GROUP3', 'si3'),
  ('group4', 'GROUP4', 'si4'),
  ('group5', 'GROUP5', 'si5');


INSERT INTO users (id, email, password, group_id, role)
VALUES
  ('user1', 'user1@gmail.com', 'password1', 'group1', 'user'),
  ('user2', 'user2@gmail.com', 'password2', 'group2', 'user'),
  ('user3', 'user3@gmail.com', 'password3', 'group3', 'user'),
  ('user4', 'user4@gmail.com', 'password4', 'group4', 'user'),
  ('user5', 'user5@gmail.com', 'password5', 'group5', 'user'),
  ('admin1', 'admin1@gmail.com', 'admin1', 'group1', 'admin'),
  ('admin2', 'admin2@gmail.com', 'admin2', 'group2', 'admin');


INSERT INTO ai_tags (tag_id, tag_name)
VALUES
  ('tag1', 'Feature'),
  ('tag2', 'Text to Image'),
  ('tag3', 'Object Detection'),
  ('tag4', 'Text Classification'),
  ('tag5', 'Question Answering'),
  ('tag6', 'Image Classification'),
  ('tag7', 'Image Segmentation'),
  ('tag8', 'Natural Language Processing'),
  ('tag9', 'Computer Vision'),
  ('tag10', 'Audio Processing'),
  ('tag11', 'Speech Recognition'),
  ('tag12', 'Machine Learning'),
  ('tag13', 'Recommender Systems');

INSERT INTO ai_models (ai_model_id, ai_model_name, user_id, tag_id, ai_domain, library, updated_by_user)
VALUES
  ('model1', 'Feature Extraction', 'user1', 'tag1', 'Multimodal', 'TensorFlow', 'user1'),
  ('model2', 'Text-to-Image', 'user2', 'tag2', 'Natural Language Processing', 'PyTorch', 'user2'),
  ('model3', 'Object Detection', 'user3', 'tag3', 'Computer Vision', 'OpenAI', 'user3'),
  ('model4', 'Text Classification', 'user4', 'tag4', 'Natural Language Processing', 'scikit-learn', 'user4'),
  ('model5', 'Question Answering', 'user5', 'tag5', 'Natural Language Processing', 'LightGBM', 'user5');


INSERT INTO model_cards (ai_model_card_id, ai_model_id, path_storage, path_config, bucket)
VALUES
  ('model_card1', 'model1', 's3://bucket1/model1/storage.zip', 's3://bucket1/model1/config.json', 'bucket1'),
  ('model_card2', 'model2', 's3://bucket2/model2/storage.zip', 's3://bucket2/model2/config.json', 'bucket2'),
  ('model_card3', 'model3', 's3://bucket3/model3/storage.zip', 's3://bucket3/model3/config.json', 'bucket3'),
  ('model_card4', 'model4', 's3://bucket4/model4/storage.zip', 's3://bucket4/model4/config.json', 'bucket4'),
  ('model_card5', 'model5', 's3://bucket5/model5/storage.zip', 's3://bucket5/model5/config.json', 'bucket5');
