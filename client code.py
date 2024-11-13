import nest_asyncio
from pyngrok import ngrok
import uvicorn
ngrok.set_auth_token("2oLO0X8FQcJUtjYkRQF0pGgOcx2_3wj5TzjkJrbEme5VccKDb")
ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8000)