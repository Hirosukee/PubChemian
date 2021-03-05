import pubchempy as pcp
import urllib.request
import discord
import goslate
from discord.ext import commands

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["s"])
    async def search(self, ctx, query: str, *args: str):
        namespace = "name"
        gos = goslate.Goslate()
        translation = True

        if "cid" in args:
            namespace = "cid"
            translation = False
        if "smiles" in args:
            namespace = "smiles"
            translation = False
        if "formula" in args:
            namespace = "formula"
            translation = False

        if "-t" in args & translation:
            query = gos.translate(query, "en")

        # get page
        compound = pcp.get_compounds(query, namespace)

        if not compound:
            await ctx.send("Page not found.")
            return

        for elem in compound:

            #embed
            e = discord.Embed(title=elem.synonyms[0], url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{elem.cid}", description="")
            e.add_field(name="Formula", value=elem.molecular_formula)
            e.add_field(name="Weight", value=str(elem.molecular_weight))
            e.add_field(name="CID", value=str(elem.cid))
            e.add_field(name="IUPAC", value=str(elem.iupac_name), inline=False)
            e.add_field(name="Smile", value=str(elem.isomeric_smiles), inline=False)
            e.set_footer(text=str(elem.synonyms) if len(str(elem.synonyms)) <= 200 else str(elem.synonyms)[:200].replace("[", "").replace("]", "").replace("'", "") + "...")
            e.set_image(url=f"https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid={elem.cid}&t=l")

            #send
            await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Search(bot))