import discord
from discord.ext import commands
import tinder_api.session
import itertools
import asyncio

from modules.Match import Match
from modules.Message import Message

# Skrudžai, rim my asshole, čia global variable ir jos reikia.
TINDER_SESSION = None


class Tinder(commands.Cog):

    # Allows to access client within methods
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def login(self, ctx):
        global TINDER_SESSION
        # Start tinder session
        TINDER_SESSION = tinder_api.session.Session()
        await ctx.send(f"Tinder session with id: {TINDER_SESSION.get_id()} started.")

    @commands.command()
    async def parse_matches(self, ctx):
        matches = []
        parsed = 0
        for match in TINDER_SESSION.yield_matches():
            messages = []
            for x in match["messages"]:
                message = Message(id=x["_id"],
                                  by=x["from"],
                                  to=x["to"],
                                  sent_date=x["created_date"],
                                  message=x["message"])
                messages.append(message)

                person = Match(userid=match["_id"],
                               name=match["person"]["name"],
                               match_date=match["created_date"],
                               bio=None,
                               birthday=match["person"]["birth_date"],
                               gender=match["person"]["gender"],
                               messages=messages)
                print(person)
                matches.append(person)
                parsed += 1

        await ctx.send(f"Parsed {parsed} matches. Type .show_matches to see database.")
        print(matches)

    @DeprecationWarning
    # TODO remove after testing for 10 min cooldown to prevent massive spam.
    # FIXME postina tik po viena, speju del to kad eina command chain ir awaitina
    # @commands.cooldown(1, 600, commands.BucketType.user)
    @commands.command()
    async def old_queue(self, ctx, amount):
        try:
            amount = int(amount)
            # Can only get between 1 and 10 matches at once.
            if amount > 10 or amount < 1:
                raise ValueError
            for user in itertools.islice(TINDER_SESSION.yield_users(), amount):
                # FIXME gal be await veiks?
                await send_match_embed(ctx, user)
        except ValueError:
            await ctx.send("Give me an integer between 1 and 10.")

    @commands.command()
    async def queue(self, ctx):
        for user in itertools.islice(TINDER_SESSION.yield_users(), 1):
            await send_match_embed(ctx, user)

    @commands.command()
    async def reply(self, ctx, id, message):
        await ctx.send(f"{id}, {message}")


async def send_match_embed(ctx, user):
    embed = discord.Embed(title=f"{user.name}")
    embed.add_field(name="Id", value=user.id, inline=False)
    embed.add_field(name="Age", value=user.age, inline=False)
    embed.add_field(name="Gender", value=user.gender, inline=False)
    embed.add_field(name="Bio", value=user.bio, inline=False)

    # Try to find all pics and give links.
    try:
        other_images = user.photos[1:]
        other_images = "\n".join(other_images)
    except Exception:
        other_images = "No other images provided."
    embed.add_field(name="Pictures:", value=other_images)

    # If profile pic doesnt exist, dont add to embedding.
    try:
        profile_pic = user.photos[0]
        embed.set_image(url=user.photos[0])
    except Exception:
        pass
    sent_message = await ctx.send(embed=embed)
    await score_sleep_like(ctx, sent_message, user)


async def score_sleep_like(ctx, sent_message, user):
    # Add reactions
    emoji_yes = '\U0001F498'
    emoji_no = '\U0001F44E'
    await sent_message.add_reaction(emoji_yes)
    await sent_message.add_reaction(emoji_no)

    # Sleep 3 minutes to gather votes
    await asyncio.sleep(3 * 60)

    # Get posted message with new reaction values
    sent_message = await ctx.channel.fetch_message(sent_message.id)

    # Get score
    yes, no = -1, -1
    for reaction in sent_message.reactions:
        try:
            if reaction.emoji == emoji_yes:
                yes += reaction.count
            elif reaction.emoji == emoji_no:
                no += reaction.count
        # Skip normal emotes
        except AttributeError:
            continue

    # If upvotes exceed downvotes, like profile.
    # FIXME DRY principle lol.
    if yes > no:
        user.like()
        await ctx.send(f"{user.name} got {yes} hearts and {no} swipe lefts. User was swiped right.")
    else:
        user.dislike()
        await ctx.send(f"{user.name} got {yes} hearts and {no} swipe lefts. User was swiped left.")


# Add cog to client.
def setup(client):
    client.add_cog(Tinder(client))
