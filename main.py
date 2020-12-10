#!/usr/bin python3
# -*- coding: utf-8 -*-

from graphqlclient import GraphQLClient
import json
import requests
import time
import schedule
import telegram

endpoint = "https://api.thegraph.com/subgraphs/name/pooltogether/pooltogether"

client = GraphQLClient(endpoint)

query = """
{
  draws(first: 5, orderBy: committedAt, orderDirection: desc) {
    id
    drawId
    committedAt
    feeBeneficiary
    secretHash
  }
  players(first: 5, orderBy: winnings, orderDirection: desc) {
    id
    address
    winnings
    latestBalance
    consolidatedBalance
  }
}
"""

result = json.loads(client.execute(query))
draws = result['data']['draws']
players = result['data']['players']


def telegram_bot_sendtext(bot_message):
    
    bot_token = '1408779274:AAGcV2y16afqqd3RX8piV9cG2N7SEDuDXy8'
    bot_chatID = '-1001467444260'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def report():
    players_message = '\n'.join([i['address'] for i in players])
    draws_message = '\n'.join([i['drawId'] for i in draws])
    telegram_bot_sendtext('Danh sách 5 người thắng cuộc nhiều nhất cập nhật hôm nay là: \n {}'.format(players_message))
    telegram_bot_sendtext('Danh sách 5 người lượt rút cập nhật hôm nay: \n {}'.format(draws_message))

schedule.every().day.at("20:00").do(report)

while True:
    schedule.run_pending()
    time.sleep(1)
