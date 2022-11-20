import falcon.asgi

from .model import Model

def create_app():
    app = falcon.asgi.App()
    model = Model(type='base')
    model.start()
    app.add_route('/generate', model)
    app.add_route('/generate/{generate_id:uuid}', model, suffix='generate')
    return app
