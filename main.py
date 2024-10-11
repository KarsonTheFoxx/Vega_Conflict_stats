# Built in python 3.12

async def main(TOKEN:str) -> None:
    from disnake.ext import commands
    from disnake import Intents
    intents = Intents.default()
    
    bot = commands.AutoShardedInteractionBot(intents=intents)
    
    @bot.event
    async def on_ready():
        print("Ready")
        
    bot.load_extensions("extensions")
    
    bot.reload = True
    
    await bot.start(TOKEN)

if __name__ == "__main__":
    from asyncio import run
    
    with open("token.txt", "r") as file:
        TOKEN = file.read()
        
    run(main(TOKEN))