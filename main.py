from config import token
token=token
def get_zapros(token,method, params):
    import requests
    url = f'https://api.telegram.org/bot{token}/{method}'
    req=requests.get(url,params)

    # print(req.json())
    return req.json()

print(get_zapros(token, 'messages.search',{'q':'start'}))
def sendMessag(token,  params):
    '''' Отпраляем сообщение пользователю'''
    # params = {'chat_id': '2036285926', 'text': 'hi,men'}
    get_zapros(token, 'sendMessage', params)

def  getUpdates(token):
    '''получаем сообщение от пользователя
     возвращаем result'''
    ask=get_zapros(token, 'getUpdates','')

    return ask['result']



def registrations():
    for x in (getUpdates(token)):
        text = (x['message']['text'])
        from_id=(x['message']['from']['id'])

        if text == '/start':
            sendMessag(token,  params={'chat_id': from_id, 'text': 'пройди регистрацию'})

RKM='''ReplyKeyboardMarkup(
  keyboard = list(
    list(KeyboardButton("Yes, they certainly are!")),
    list(KeyboardButton("I'm not quite sure")),
    list(KeyboardButton("No..."))
  ),
  resize_keyboard = FALSE,
  one_time_keyboard = TRUE
)'''
params = {'chat_id': '2036285926', 'text': 'hi,men', 'reply_markup':RKM}

