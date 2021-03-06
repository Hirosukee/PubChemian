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
        if ctx.author.bot:
            return

        namespace = "name"
        image_mode = "thumbnail"
        gos = goslate.Goslate()
        limiter = 1

        # args
        def check(arg) -> bool:
            return arg in args

        if check("-smiles"):
            namespace = "smiles"
        if check("-cid"):
            namespace = "cid"
        if check("-formula"):
            namespace = "formula"
        if check("-name"):
            namespace = "name"

        if check("-image") | check("-i"):
            image_mode = "image"
        if check("-thumbnail") | check("-tb"):
            image_mode = "thumbnail"

        if check("-l") | check("-limit"):
            for i, hoge in enumerate(args):
                if hoge.isdigit():
                    limiter = int(hoge)

        if check("-t") | check("-translate"):
            if not (check("-formula") | check("-cid") | check("-smiles")):
                query = gos.translate(query, "en")

        # get page
        compound = pcp.get_compounds(query, namespace)

        # 404
        if not compound:
            await ctx.send("Page not found.")
            return

        for i,elem in enumerate(compound):

            if i >= limiter:
                break

            image_url = f"https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid={elem.cid}&t=l"

            #embed
            e = discord.Embed(title=elem.synonyms[0], url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{elem.cid}", description="")
            e.add_field(name="Formula", value=str(elem.molecular_formula), inline=True)
            e.add_field(name="Weight",  value=str(elem.molecular_weight),  inline=True)
            e.add_field(name="CID",     value=str(elem.cid),               inline=True)
            e.add_field(name="IUPAC",   value=str(elem.iupac_name),        inline=False)
            e.add_field(name="Smile",   value=str(elem.isomeric_smiles),   inline=False)
            e.set_footer(text=str(elem.synonyms) if len(str(elem.synonyms)) <= 100 else str(elem.synonyms)[:100].replace("[", "").replace("]", "").replace("'", "") + "...")
            if image_mode == "image":
                e.set_image(url=image_url)
            if image_mode == "thumbnail":
                e.set_thumbnail(url=image_url)

            #send
            await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Search(bot))