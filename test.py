import json
import alchemy_game
from datetime import datetime

def test_add():
    # 建立一個空的 JSON 物件（字典）
    json_data = {}

    # 在 JSON 物件中塞值
    json_data['year'] = 2024
    json_data['season'] = 1
    json_data['start_datetime'] = '2023-12-03 13:30'
    json_data['duration'] = 150
    json_data['location'] = '觀山E'
    json_data['home_team'] = '輔大'
    json_data['away_team'] = '臺大'

    #print(json_string)
    alchemy_game.add_game(json_data)

def test_search_games():    
    start_datetime = datetime(2023, 11, 11)
    start_datetime_str = start_datetime.isoformat()

    current_datetime = datetime.now().replace(microsecond=0)
    current_datetime_str = current_datetime.isoformat()
    request_json = {'start_time': start_datetime_str, 'end_time': current_datetime_str}
    
    if (alchemy_game.is_search_game_json_valid(request_json)):
        
        # 讀取比賽資訊，輸出
        games = alchemy_game.search_games_between(request_json)

        # 使用列表推導式將每個物件轉換為字典
        game_list = [game.as_dict() for game in games]

        # 使用 json.dumps 將整個列表轉換為 JSON 字串
        json_string = json.dumps(game_list, indent=2, ensure_ascii=False)
        print(json_string)

def test_update_invitation_time():    
    alchemy_game.update_invitation_time({'id': 14, 'time': '2023-12-03 13:30:00'})

def test_update_cancellation_time():    
    alchemy_game.update_cancellation_time({'id': 14, 'time': '2023-12-04 13:30:00'})

test_search_games()