CREATE TABLE "users" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL UNIQUE,
	"password_hash"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);

CREATE TABLE "alerts" (
	"symbol_name"	TEXT NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"notification_id"	INTEGER,
	FOREIGN KEY("notification_id") REFERENCES "notifications"("id") ON DELETE CASCADE,
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
	PRIMARY KEY("symbol_name","user_id")
);

CREATE TABLE "notifications" (
	"id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"content"	TEXT NOT NULL,
	"type"	TEXT NOT NULL CHECK("type" IN ("email", "discord")),
	"discord_webhook_url"	TEXT,
	"smtp_url"	TEXT,
	"email"	TEXT,
	"ntfy_topic"	TEXT,
	PRIMARY KEY("id")
);
