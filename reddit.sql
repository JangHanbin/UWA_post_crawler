CREATE TABLE posts (
	id VARCHAR(50) PRIMARY KEY,
	num_comments INT,
	created TIMESTAMP,
	score INT,
	distinguish_type VARCHAR(100),
	is_locked	BOOLEAN,
	is_stickied	BOOLEAN,
	thumbnail	LONGBLOB,
	title		TEXT,
	author		TEXT,
	author_id	VARCHAR(50),
	domain		TEXT,
	view_count	INT,
	gold_count	INT,
	is_archived	BOOLEAN,
	contest_mode	BOOLEAN,
	suggested_sort	VARCHAR(100),
	hidden	BOOLEAN,
	saved	BOOLEAN,
	is_gildable	BOOLEAN,
	is_sponsored	BOOLEAN,
	is_media_only	BOOLEAN,
	is_NSFW	BOOLEAN,
	is_meta	BOOLEAN,
	is_spoiler	BOOLEAN,
	is_blank	BOOLEAN,
	send_replies	BOOLEAN,
	vote_state	INT,
	permalink	TEXT,
	preview	TEXT,
	num_crossports	INT,
	is_crossportable	BOOLEAN,
	live_comments_websocket	TEXT,
	is_original_content	BOOLEAN,
	is_score_hidden	BOOLEAN

);

CREATE TABLE subreddits (
	post_id	VARCHAR(50),
	id	VARCHAR(50),
	allow_chat_post_creation	BOOLEAN,
	is_chat_post_feature_enabled	BOOLEAN,
	display_text	VARCHAR(200),
	type	VARCHAR(100),
	is_quarantined	BOOLEAN,
	is_NSFW		BOOLEAN,
	name		VARCHAR(100),
	url			TEXT,
	title		TEXT,
	whitelist_status	VARCHAR(200),
	wls			INT,
	community_icon	LONGBLOB,
	subscribers		BIGINT,
	free_form_reports	BOOLEAN,

	FOREIGN KEY (post_id)
	REFERENCES posts (id) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE awardings (
	post_id	VARCHAR(50),
	award_type	VARCHAR(50),
	award_sub_type	VARCHAR(50),
	coin_price	INT,
	coin_reward	INT,
	days_of_drip_extension	INT,
	days_of_premium	INT,
	description	TEXT,
	icon	LONGBLOB,
	icon_width	INT,
	icon_height	INT,
	id	TEXT,
	is_enabled	BOOLEAN,
	is_new		BOOLEAN,
	name	TEXT,
	subreddit_count_reward	INT,
	subreddit_id	VARCHAR(50),
	count	INT,
	
	FOREIGN KEY (post_id)
	REFERENCES posts (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE sources (
	post_id	VARCHAR(50),
	display_text	TEXT,
	url				TEXT,
	outbound_url	TEXT,
	outbound_expiration	TIMESTAMP,
	outbound_created	TIMESTAMP,
	
	FOREIGN KEY (post_id)
	REFERENCES posts (id) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE media (
	post_id	VARCHAR(50),
	type	VARCHAR(100),

	FOREIGN KEY (post_id)
	REFERENCES posts (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE richtext (
	post_id VARCHAR(50),
	origin_json		TEXT,
	converted_text	TEXT,

	FOREIGN KEY (post_id)
	REFERENCES posts (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE  gifvideo (
	post_id	VARCHAR(50),
	content_url	TEXT,
	content	LONGBLOB,
	width	INT,
	height	INT,

	FOREIGN KEY (post_id)
	REFERENCES posts (id) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE embed (
	post_id	VARCHAR(50),
	content	TEXT,
	width	INT,
	height	INT,
	provider	TEXT,

	FOREIGN KEY (post_id)
	REFERENCES posts (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE image (
	post_id	VARCHAR(50),
	content_url	TEXT,
	content	LONGBLOB,
	width	INT,
	height	INT,

	FOREIGN KEY (post_id)
	REFERENCES posts (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE video (
	post_id VARCHAR(50),
	hls_url	TEXT,
	dash_url	TEXT,
	is_gif	BOOLEAN,
	scrubber_thumb_source	TEXT,
	poster_url	TEXT,
	poster	LONGBLOB,
	width	INT,
	height	INT,
	
	FOREIGN KEY (post_id)
	REFERENCES posts (id) ON UPDATE CASCADE ON DELETE CASCADE
);


