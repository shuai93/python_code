from vibora import Vibora, Request
from vibora.responses import Response, JsonResponse, StreamingResponse
from vibora.router import RouterStrategy
from vibora.static import StaticHandler
from vibora.schemas import Schema


import asyncio
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

static_dirs = os.path.join(BASE_DIR, 'static/')
template_dirs = os.path.join(BASE_DIR, 'templates')

# app = Vibora()
# app = Vibora(router_strategy=RouterStrategy.STRICT)

app = Vibora(
    static=StaticHandler(
        paths=[static_dirs],
        # host='static.vibora.io',
        url_prefix='/static',
        max_cache_size=1 * 1024 * 1024
    ),
    template_dirs=[template_dirs]
)


class SimpleSchema(Schema):
    name: str


@app.route('/form', methods=['POST'])
async def form(request: Request):
    schema = await SimpleSchema.load_json(request)
    return JsonResponse({'name': schema.name})


@app.route('/')
async def home():
    return Response(b"Hello  World!")


@app.route("/home", methods=['GET'])
async def home():
    return Response(b'123')


@app.route('/<page_id>')
async def page(page_id: int):
    return Response(f'Page {page_id}'.encode())


@app.route('/api')
async def api():
    return JsonResponse({'Hello': 'world'})


@app.route('/home1', methods=['GET'])
async def home1():
    async def stream_builder():
        print('StreamingResponse start ')
        for x in range(0, 5):
            yield str(x).encode()
            await asyncio.sleep(0.5)
        print('StreamingResponse stop ')
        
    return StreamingResponse(stream_builder, chunk_timeout=5, complete_timeout=30)


@app.route('/page/<page_id>')
async def page(page_id: int):
    print(page_id)
    return await app.render('index.html', tmp=page_id)


if __name__ == '__main__':
    app.run(debug=True, port=8000)