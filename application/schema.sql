CREATE TABLE "news_sentiment_predict" (
	"id"	INTEGER NOT NULL,
	"datetime"	TEXT NOT NULL,
	"news_sentiment_polarity"	REAL NOT NULL,
	"news_volume"	INTEGER NOT NULL,
	"close_price_previous"	REAL NOT NULL,
	"close_price_next_predicted"	REAL NOT NULL,
	"stock_symbol"	TEXT NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "technical_analysis_predict" (
	"id"	INTEGER NOT NULL,
	"datetime"	TEXT NOT NULL,
	"delta_price_predicted"	REAL NOT NULL,
	"target_datetime"	TEXT NOT NULL,
	"stock_symbol"	TEXT NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "stock_symbol_available" (
	"symbol_name"	TEXT NOT NULL,
	PRIMARY KEY("symbol_name")
);
