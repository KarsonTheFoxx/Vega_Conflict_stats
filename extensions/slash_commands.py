from disnake.ext import commands
from disnake_plugins import Plugin
from disnake import Embed, Color, CommandInteraction
import aiohttp

plugin = Plugin()

@plugin.slash_command(name="stats", description="Look up the stats of a player by player id")
@commands.cooldown(rate=5, per=15, type=commands.BucketType.user)
@commands.cooldown(rate=30, per=30, type=commands.BucketType.guild)
async def stats(inter:CommandInteraction, id:str=commands.Param(description="The ingame id of a player")):
    try:
        id = int(id)
    except ValueError:
        await inter.edit_original_message("Invalid ID")
        return
    await inter.response.send_message(embed=Embed(title="Fetching user stats", description="This may take a few moments.", color=Color.blurple()))
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.kixeye.com:443/api/v2/user-games?gameId=386487958112133&playerId={id}") as response:
            kixeye_id = await response.json()
            if len(kixeye_id) < 1:
                await inter.edit_original_message("Player not found")
                return
            kixeye_id = kixeye_id[0]["userId"]
        
        async with session.get(f"https://api.kixeye.com/api/v2/users/{kixeye_id}/games/386487958112133") as response:
            response = await response.json()
            try:
                alias = response["alias"]
                player_id = response["playerId"]
            except KeyError:
                alias = "Not available"
                player_id = "N/A"
            
            try:
                base_attack_wins = response["baseAttackWin"]
                base_attack_draws = response["baseAttackDraw"]
                base_attack_losses = response["baseAttackLoss"]
                fvba = f"{base_attack_wins}/{base_attack_draws}/{base_attack_losses}/{round((base_attack_wins/(base_attack_wins+base_attack_draws+base_attack_losses))*100, 2)}%/{round(base_attack_wins/base_attack_losses, 2)}"
            except KeyError:
                base_attack_wins = 0
                base_attack_draws = 0
                base_attack_losses = 0
                fvba = "No info available"
            except ZeroDivisionError:
                fvba = "No info available"
                
            try:
                base_defend_wins = response["baseDefenceWin"]
                base_defend_draws = response["baseDefenceDraw"]
                base_defend_losses = response["baseDefenceLoss"]
                fvbd = f"{base_attack_wins}/{base_defend_draws}/{base_defend_losses}/{round((base_defend_wins/(base_defend_wins + base_defend_draws + base_defend_losses))*100, 2)}%/{round(base_defend_wins/base_defend_losses, 2)}"
            except KeyError:
                base_defend_wins = 0
                base_attack_draws = 0
                base_attack_losses = 0
                fvbd = "No info available"
            except ZeroDivisionError:
                fvbd = "No info available"
            try:
                fleet_wins = response["fleetWin"]
                fleet_draws = response["fleetDraw"]
                fleet_losses = response["fleetLoss"]
                fvf = f"{fleet_wins}/{fleet_draws}/{fleet_losses}/{round((fleet_wins/(fleet_wins+fleet_draws+fleet_losses))*100, 2)}%/{round(fleet_wins/fleet_losses, 2)}"
            except KeyError:
                fleet_wins = 0
                fleet_draws = 0
                fleet_losses = 0
                fvf = "No info available"
            except ZeroDivisionError:
                fvf = "No info available"
            
            try:
                medals = response["medals"]
                level = response["level"]
            except KeyError:
                medals = "N/A"
                level = "N/A"
            
            try:
                sector = response["sector"]
                planet = response["planet"]
            except KeyError:
                sector = "N/A"
                planet = "N/A"
                
            try:
                last_seen = f"<t:{round(response['seen']/1000)}:R>"
                played_since = f"<t:{round(response['since']/1000)}:d>"
            except KeyError:
                last_seen = "Unavailable"
                played_since = "Unavailable"
                
        await session.close()

    embed = Embed(title=f"{alias}", description=f"-# Played since: {played_since}\n-# Last seen: {last_seen}", color=Color.random())
    embed.set_thumbnail("https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/339600/header.jpg?t=1721853313")
    embed.add_field(name=":identification_card: Player ID", value=player_id, inline=False)
    embed.add_field(name=":beginner: Level"+"**" + " "*20 + "**", value=level, inline=True)
    embed.add_field(name=":medal: Medals", value=medals, inline=True)
    embed.add_field(name="** **", value="** **", inline=False)
    embed.add_field(name=":ringed_planet: Planet", value=planet, inline=True)
    embed.add_field(name=":sunny: Sector", value=sector, inline=True)
    embed.add_field(name=":bomb: FVB (attacking) wins/draws/losses/wins%/KD", value=fvba, inline=False)
    embed.add_field(name=":shield: FVB (Defending) wins/draws/losses/win%/KD", value=fvbd, inline=False)
    embed.add_field(name=":crossed_swords: FVF wins/draws/losses/win%/KD", value=fvf, inline=False)
    await inter.edit_original_message(embed=embed)


setup, teardown = plugin.create_extension_handlers()