#!/usr/bin/python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


my_bot = ChatBot("Training demo",
                 database="./db.sqlite3")

# 直接写语句训练
my_bot.set_trainer(ListTrainer)

my_bot.train(["你叫什么名字？", "我叫小白兔！", ])
my_bot.train([
    "Test1",
    "Test2",
    "Test3",
    "Test4",
])

# 使用自定义语句训练它
my_bot.set_trainer(ChatterBotCorpusTrainer)
my_bot.train("chatterbot.corpus.mytrain")
# while True:
#     print(my_bot.get_response(input("user:")))
