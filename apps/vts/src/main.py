import yaml
import asyncio
from utils.args import args
from utils.logging import logger
from utils.vts_plugin import VTSHotkeyPlugin

async def main():
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
        print(config)
        print(type(config))

    vts = VTSHotkeyPlugin(config)
    await vts.start()
    logger.info("VTS Hotkey Plugins initialized")
    
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
