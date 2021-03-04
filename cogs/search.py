import pubchempy as pcp
import urllib.request
import discord
import goslate
from discord.ext import commands

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["s"])
    async def search(self, ctx, query: str, translate: bool=None, namespace: str=None):
        query_text = query
        if namespace == None:
            namespace = "name"

        if translate == None:
            translator = goslate.Goslate()
            query_text = translator.translate(query, "en")

        # get page
        compound = pcp.get_compounds(query_text, namespace)

        for elem in compound:

            #embed
            e = discord.Embed(title=elem.iupac_name, description="")
            e.add_field(name="Formula", value=elem.molecular_formula)
            e.add_field(name="Weight", value=str(elem.molecular_weight))
            e.add_field(name="CID", value=str(elem.cid))
            e.add_field(name="CID", value=str(elem.charge))
            e.add_field(name="Smile", value=str(elem.isomeric_smiles), inline=False)
            e.set_footer(text=str(elem.synonyms) if len(str(elem.synonyms)) <= 200 else str(elem.synonyms)[:200].replace("[", "").replace("]", "").replace("'", "") + "...")
            e.set_image(url=f"https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid={elem.cid}&t=l")

            #send
            await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Search(bot))