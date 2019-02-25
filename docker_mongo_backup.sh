#!/bin/sh
export $(cat $1 | xargs)				# .env file as first argument
CONTAINER=$(docker ps|grep $2_mongo|cut -c-13 -)	# Docker stack name as second argument

# Temp files for collection jsons
CHATS_FILE=$(date '+%N')'_temp_chats.json'
WORDS_FILE=$(date '+%N')'_temp_words.json'
BLACKLIST_FILE=$(date '+%N')'_temp_bl.json'

# Output file
BACKUP_FILE='MarkkuBot_Backup_'$(date '+%Y-%m-%d_%H-%M-%S')'.tar.gz'

# Execute mongo export inside db container
docker exec $CONTAINER sh -c 'mongoexport --jsonarray --db '$DB_NAME' --collection '$CHATS_COLL_NAME'' > $CHATS_FILE
docker exec $CONTAINER sh -c 'mongoexport --jsonarray --db '$DB_NAME' --collection '$WORDS_COLL_NAME'' > $WORDS_FILE
docker exec $CONTAINER sh -c 'mongoexport --jsonarray --db '$DB_NAME' --collection '$BLACKLIST_COLL_NAME'' > $BLACKLIST_FILE

# Make tar and remove temp files
tar cvzf $BACKUP_FILE $CHATS_FILE $WORDS_FILE $BLACKLIST_FILE
rm $CHATS_FILE $WORDS_FILE $BLACKLIST_FILE
