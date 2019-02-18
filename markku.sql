
CREATE TABLE IF NOT EXISTS name (
    id      BIGINT      NOT NULL PRIMARY KEY,
    name    VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS counter (
    user_id     BIGINT  NOT NULL,
    chat_id     BIGINT  NOT NULL,
    commands    INT     DEFAULT 0,
    gifs        INT     DEFAULT 0,
    kiitos      INT     DEFAULT 0,
    messages    INT     DEFAULT 0,
    photos      INT     DEFAULT 0,
    stickers    INT     DEFAULT 0,
    PRIMARY KEY (user_id, chat_id)
);

CREATE TABLE IF NOT EXISTS word (
    user_id     BIGINT  NOT NULL,
    chat_id     BIGINT  NOT NULL,
    word        VARCHAR(30) NOT NULL,
    count       INT DEFAULT 0
    PRIMARY KEY (user_id, chat_id, word)
);

CREATE TABLE IF NOT EXISTS blacklist (
    user_id     BIGINT  NOT NULL
);