def destroy_tweets(): # utility function
	tweets = twitter.statuses.user_timeline(screen_name='anybdywannapnut', count=200)
	for t in tweets:
		twitter.statuses.destroy(id=t['id'])