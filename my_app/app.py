from my_app import create_app, config

app = create_app(config.DevelopmentConfig)  # DEVELOPMENT / TESTING / PRODUCTION


if __name__ == '__main__':
    app.run()
