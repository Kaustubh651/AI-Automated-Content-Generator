from services.post_router import LivePoster

if __name__ == '__main__':
    print('Starting LivePoster dry-run (live_mode=False)')
    poster = LivePoster(live_mode=False)
    result = poster.post_all()
    print('\nDRY-RUN RESULT SUMMARY:')
    print(result)
