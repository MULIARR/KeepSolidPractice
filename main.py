import asyncio
import logging

import uvicorn
from app import app

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    # port = int(os.environ.get("PUBLIC_PORT", 9097))
    # host = str(os.environ.get("HOST", "127.0.0.1"))

    config = uvicorn.Config(app, "127.0.0.1", port=9097, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("off")

