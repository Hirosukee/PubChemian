import discord
from discord.ext import commands
from textwrap import dedent

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"])
    async def _help(self, ctx):
        await ctx.send(dedent("""\
        __**PubChemian Commands**__

        > `.search[.s] <keyword> (<*args>)`
        To search compounds.
        `-translate[-t]` to translate a keyword to english.
        `-limit[-l] <amount>` to limit to search.
        `-[smiles, cid, formula, name]` to change a search type.
        `-image[-i]` to show structural formula as bigger.
        `-thumbnail[-tb]` to show structural formula as smaller.

        > `.help[.h]`
        To show this help.
        """))

def setup(bot):
    bot.add_cog(Help(bot))