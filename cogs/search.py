import pubchempy as pcp
import urllib.request
import discord
from discord.ext import commands

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["s"])
    async def search(self, ctx, query: str, namespace: str=None):
        if namespace == None:
            namespace = "name"

        # get page
        c = pcp.get_compounds(query, namespace)

        for i in c:

            #embed
            e = discord.Embed(title=i.iupac_name, description="")
            e.add_field(name="Formula", value=i.molecular_formula)
            e.add_field(name="Weight", value=str(i.molecular_weight))
            e.add_field(name="CID", value=str(i.cid))
            e.add_field(name="Smile", value=str(i.isomeric_smiles), inline=False)
            e.set_footer(text=str(i.synonyms) if len(str(i.synonyms)) <= 200 else str(i.synonyms)[:200].replace("[", "").replace("]", "").replace("'", "") + "...")
            e.set_image(url=f"https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid={i.cid}&t=l")

            #send
            await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Search(bot))