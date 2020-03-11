CREATE TABLE post (
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

CREATE TABLE subreddit (
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
	icon		LONGBLOB,
	whitelist_status	VARCHAR(200),
	wls			INT,
	community_icon	LONGBLOB,
	subscribers		BIGINT,
	free_form_reports	BOOLEAN,
	account_active		BIGINT,
	advertiser_category	VARCHAR(100),
	using_new_modmail	BOOLEAN,
	description			TEXT,
	show_media		BOOLEAN,
	restrict_posting	BOOLEAN,
	restrict_commenting	BOOLEAN,
	disable_contributor_reqeusts	BOOLEAN,
	subbmit_link_label	TEXT,
	submit_text_label	TEXT,
	created		TIMESTAMP,
	content_category	TEXT,
	all_original_content	BOOLEAN,
	original_content_tag_enabled	BOOLEAN,
	has_external_account	BOOLEAN,
	is_crosspostable_subreddit	BOOLEAN,

	FOREIGN KEY (post_id)
	REFERENCES post (id) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE subreddit_allow_post_types (
	subreddit_id	VARCHAR(50) PRIMARY KEY,
	links	BOOLEAN,
	images	BOOLEAN,
	videos	BOOLEAN,
	text	BOOLEAN,
	spoiler	BOOLEAN,
	pools	BOOLEAN
);


CREATE TABLE source (
	post_id	VARCHAR(50),
	display_text	TEXT,
	url				TEXT,
	outbound_url	TEXT,
	outbound_expiration	TIMESTAMP,
	outbound_created	TIMESTAMP,
	
	FOREIGN KEY (post_id)
	REFERENCES post (id) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE media (
	post_id	VARCHAR(50),
	type	VARCHAR(100),

	FOREIGN KEY (post_id)
	REFERENCES post (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE richtext (
	post_id VARCHAR(50),
	origin_json		TEXT,
	converted_text	TEXT,

	FOREIGN KEY (post_id)
	REFERENCES post (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE  gifvideo (
	post_id	VARCHAR(50),
	content_url	TEXT,
	content	LONGBLOB,
	width	INT,
	height	INT,

	FOREIGN KEY (post_id)
	REFERENCES post (id) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE embed (
	post_id	VARCHAR(50),
	content	TEXT,
	width	INT,
	height	INT,
	provider	TEXT,

	FOREIGN KEY (post_id)
	REFERENCES post (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE image (
	post_id	VARCHAR(50),
	content_url	TEXT,
	content	LONGBLOB,
	width	INT,
	height	INT,

	FOREIGN KEY (post_id)
	REFERENCES post (id) ON UPDATE CASCADE ON DELETE CASCADE
);


