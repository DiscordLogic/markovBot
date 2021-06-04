import discord
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from chaincode import build_chain


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


StorageArray = {}

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.relationship("Post", backref='author', lazy=True)

    def __str__(self):
        output = ''
        for c in self.__table__.columns:
            output += '{}: {}\n'.format(c.name, getattr(self, c.name))
        return output


class Post(db.Model):
    postsId = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post = db.Column(db.Text, nullable=False)


# Collects all messages of a discord user on request, then uses markov chains to generate
# a sample message based on their message history


# array to store add me users.

addMe = [394993333539307524, 730479245419085865, 490489005394100225, 394993333539307524, 291332069244796928, ]
addMePush = []
error = 0


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        global error
        global addMe
        global addMePush

        if message.content.split(" ")[0] == "~addThem":
            for x in message.mentions:
                if error == 1:
                    await message.channel.send("nuuuuuu please i can only handle uno request at a timeeeeee")
                    return
                addMe.append(message.author.id)
                get_or_create(db.session, User, **{"id": x.id})
                await message.channel.send("awww sussy sussy baka adding their friendsss!! XD *pat pat*")


        if message.content.split(" ")[0] == "~copyThem":
            for x in message.mentions:
                rows = db.session.query(Post).filter(Post.user_id == x.id).all()
                print(rows)
                array = []
                for row in rows:
                    array.append(row.post)

                await message.channel.send(build_chain(array))


        if message.author == self.user:
            return

        if message.content == "~copyme":

            rows = db.session.query(Post).filter(Post.user_id == message.author.id).all()

            array = []
            for row in rows:
                array.append(row.post)
            print("Following the code for array  \n")
            print(array)
            await message.channel.send(build_chain(array))

        if message.content == "~addme":
            if error == 1:
                await message.channel.send("nuuuuuu please i can only handle uno request at a timeeeeee")
                return
            addMe.append(message.author.id)
            get_or_create(db.session, User, **{"id": message.author.id})
            await message.channel.send("Added to the List uwu, *pat pat*")

        if message.content == "~watchme":

            if error == 1:
                await message.channel.send("baka!! please wait :), it takes a bit to load *pat pat*")
                await message.channel.send(
                    message.author.name + "uwu u sussy sussy baka, you're such an imposter go back to waiting or i'll get mad rawrrrs XD hehe~!!")
                return

            for x in addMe:
                await message.channel.send(x)
            error = 1
            addMePush = addMe
            await message.channel.send(
                "hewwo sussy baka *pat pat* we are running the code, this might take a while so sit back relax and reading the communist uwu manifesto!!")

            array_guild = [688582834746687510,784875761038524486,838774299561164830,756363971581313085,784872990751588362,449826506043031552,449822299147862018,784876185535774741,753708196962631730,797663513203965972,774692408411684884,784873416179580929,694412014470037515,708932886887268362,784876185535774741]
            for x in message.guild.text_channels:
                if x.id in array_guild:
                    async for msg in x.history(limit=20000):  # As an example, I've set the limit to 10000
                            data = {"postsId": msg.id, "user_id": msg.author.id, "post": msg.content}
                            get_or_create(db.session, User, **{"id": msg.author.id})
                            get_or_create(db.session, Post, **data)
                            print(msg.content)

            await message.channel.send(
                "hewwo i'm back and I missed u soooooo much uwu, *xd rawr in rice purity of 90+* All of the chains are done, try ~copyme now")

        if message.content == '~ping':
            await message.channel.send(
                "hewwo sussy baka *pat pat* pong🏓")


client = MyClient()
client.run("NDcwMjg5Mjk5MjA4NjY3MTM2.W1N1Cg.m5fb6lA2-bpn_k8c-tlDLyhHyvM")
