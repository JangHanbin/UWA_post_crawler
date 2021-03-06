CREATE TABLE tweets (
	id_str			BIGINT	PRIMARY KEY,
	id 				BIGINT,
	created_at 		TIMESTAMP,
	text			VARCHAR(500),
	source 			VARCHAR(1000),
	truncated		BOOLEAN,
	in_reply_to_status_id	BIGINT,
	in_reply_to_user_id		BIGINT,
	in_reply_to_screen_name	VARCHAR(1000),
	quoted_status_id		BIGINT,
	is_quote_status			BOOLEAN,
	quote_count		INT,
	reply_count		INT,
	retweet_count 	INT,
	favorite_count	INT,
	favorited		BOOLEAN,
	retweeted		BOOLEAN,
	possibly_sensitive		BOOLEAN,
	filter_level	VARCHAR(100),
	lang			VARCHAR(10),
	retweeted_status_id		BIGINT,		
	search_keyword	VARCHAR(500),
	search_stamp		TIMESTAMP
	);

CREATE TABLE users (
	tweet_id		BIGINT,
	id				BIGINT,
	id_str			BIGINT,
	name			VARCHAR(100),
	screen_name		VARCHAR(100),
	location		VARCHAR(1000),
	url				TEXT,
	description		VARCHAR(1000),
	protected		BOOLEAN,
	verified		BOOLEAN,
	followers_count	INT,
	friends_count	INT,
	listed_count	INT,
	favourites_count		INT,
	statuses_count	INT,
	created_at		TIMESTAMP,
	profile_banner_url		TEXT,
	profile_image_url_https	TEXT,
	default_profile	BOOLEAN,
	default_profile_image	BOOLEAN,
	withheld_in_countries	VARCHAR(1000),
	withheld_scope	VARCHAR(1000),

	FOREIGN KEY (tweet_id)
	REFERENCES tweets (id_str) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE coordinates (
	tweet_id		BIGINT,
	coordinates		VARCHAR(200),
	type			VARCHAR(20),

	FOREIGN KEY (tweet_id)
	REFERENCES tweets (id_str) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE place (
	tweet_id		BIGINT,
	id				VARCHAR(200),
	url				TEXT,
	place_type		VARCHAR(100),
	name			VARCHAR(100),
	full_name		VARCHAR(300),
	country_code	VARCHAR(20),
	country			VARCHAR(400),
	bouding_box		VARCHAR(700),

	FOREIGN KEY (tweet_id)
	REFERENCES tweets (id_str) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE hashtag (
	tweet_id 		BIGINT,
	indices			VARCHAR(200),
	text			VARCHAR(1200),

	FOREIGN KEY (tweet_id)
	REFERENCES tweets (id_str) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE media (
	tweet_id		BIGINT,
	display_url		TEXT,
	expanded_url	TEXT,
	id				BIGINT,
	indicies		VARCHAR(200),
	media_url		TEXT,
	media_url_https	TEXT,
	source_status_id	BIGINT,
	type			VARCHAR(20),
	url				TEXT,
	data			LONGBLOB,

	FOREIGN KEY (tweet_id)
	REFERENCES tweets (id_str) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE url (
	tweet_id		BIGINT,
	display_url		TEXT,
	expanded_url	TEXT,
	indices			VARCHAR(200),
	url				TEXT,

	FOREIGN KEY (tweet_id)
	REFERENCES tweets (id_str) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE user_mention (
	tweet_id	BIGINT,
	id			BIGINT,
	indicies	VARCHAR(200),
	name		VARCHAR(1000),
	screen_name	VARCHAR(1000),


	FOREIGN KEY (tweet_id)
	REFERENCES tweets (id_str) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE symbol (
	tweet_id	BIGINT,
	indicies	VARCHAR(200),
	text		VARCHAR(500),

	FOREIGN KEY (tweet_id)
	REFERENCES tweets (id_str) ON UPDATE CASCADE ON DELETE CASCADE
);



