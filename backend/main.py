import app

try:
    app.start()
except KeyboardInterrupt:
    print('Ctrl + C received. Terminating the app...')
