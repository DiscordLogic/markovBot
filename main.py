import discord
import numpy as numpy
import random as random
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import secrets
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import datetime
import json
import operator
from chaincode import generate_message, build_chain


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

addMe = []
addMePush = []
error = 0


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "!copyme":

            rows = db.session.query(Post).filter(Post.user_id == message.id).all()
            array = []
            for row in rows:
                array.append(row.text)

            await message.channel.send(generate_message(build_chain(array), count=30))

        if message.content == "!addme":
            global addMe
            addMe.append(message.author.id)
            get_or_create(db.session, User, **{"id": message.author.id})
            await message.channel.send("Added to the List uwu, *pat pat*")

        if message.content == "!watchme":
            global error
            global addMe
            global addMePush
            if error == 1:
                await message.channel.send("baka!! please wait :), it takes a bit to load *pat pat*")
            error = 1
            addMePush = addMe
            addMe = []
            await message.channel.send(
                "hewwo sussy baka *pat pat* we are running the code, this might take a while so sit back relax and reading the communist uwu manifesto!!")
            for x in message.guild.text_channels:
                async for msg in message.channel.history(limit=100000):  # As an example, I've set the limit to 10000
                    if msg.author.id in addMePush:
                        data = {"postsId": msg.id, "user_id": msg.author.id, "post": msg.content}
                        get_or_create(db.session, Post, **data)

        if message.content == '!ping':
            pong = "pong🏓"


client = MyClient()
client.run('ODUwMTU1NDI4ODc1OTkzMTMw.YLlm8Q.6D0KvNYLEEHwhyUGBziSmM8kPrY')
