from flask import Flask, request, jsonify, abort
import alchemy_game

app = Flask(__name__)

with app.app_context():
    response_400 = jsonify({'status': 'error', 'message': f'Invalid JSON format or missing required fields'})

@app.route('/add_game', methods=['POST'])
def add_game():
    try:
        # 解析 POST 請求中的比賽資訊
        request_json = request.get_json(silent=True)
        if (not alchemy_game.is_game_json_valid(request_json)):
            return response_400, 400

        # 寫入比賽資訊到資料庫
        alchemy_game.add_game(request_json)
        return jsonify({'status': 'success', 'message': 'Game added successfully'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed to add game: {e}'}), 500

@app.route('/search_for_invitation', methods=['POST'])
def search_for_invitation():
    try:
        # 解析 POST 請求中的開始結束時間
        request_json = request.get_json(silent=True)
        if (not alchemy_game.is_search_game_json_valid(request_json)):
            return response_400, 400
        
        # 讀取比賽資訊，輸出
        games = alchemy_game.search_for_invitation(request_json)
        # 使用列表推導式將每個物件轉換為字典
        game_list = [game.as_dict() for game in games]
        return jsonify({'status': 'success', 'games': game_list})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed to search games to invite: {e}'}), 500
    
@app.route('/search_invited', methods=['POST'])
def search_invited():
    try:
        # 解析 POST 請求中的開始結束時間
        request_json = request.get_json(silent=True)
        if (not alchemy_game.is_search_game_json_valid(request_json)):
            return response_400, 400
        
        # 讀取比賽資訊，輸出
        games = alchemy_game.search_for_invited(request_json)
        # 使用列表推導式將每個物件轉換為字典
        game_list = [game.as_dict() for game in games]
        return jsonify({'status': 'success', 'games': game_list})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed to search invited games: {e}'}), 500

@app.route('/search_cancelled_to_announce', methods=['POST'])
def search_cancelled_to_announce():
    try:
        # 解析 POST 請求中的開始結束時間
        request_json = request.get_json(silent=True)
        if (not alchemy_game.is_search_game_json_valid(request_json)):
            return response_400, 400
        
        # 讀取比賽資訊，輸出
        games = alchemy_game.search_cancelled_to_announce(request_json)
        # 使用列表推導式將每個物件轉換為字典
        game_list = [game.as_dict() for game in games]
        return jsonify({'status': 'success', 'games': game_list})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed to search games to announce cancellation: {e}'}), 500
    

@app.route('/search_by_id', methods=['POST'])
def search_by_id():
    try:
        # 解析 POST 請求中的開始結束時間
        request_json = request.get_json(silent=True)
        if (not alchemy_game.is_search_game_id_json_valid(request_json)):
            return response_400, 400
        
        # 讀取比賽資訊，輸出
        games = alchemy_game.search_by_id(request_json)
        # 使用列表推導式將每個物件轉換為字典
        game_list = [game.as_dict() for game in games]
        return jsonify({'status': 'success', 'games': game_list})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed to search games: {e}'}), 500
    
@app.route('/search_by_time', methods=['POST'])
def search_by_time():
    try:
        # 解析 POST 請求中的開始結束時間
        request_json = request.get_json(silent=True)
        if (not alchemy_game.is_search_game_json_valid(request_json)):
            return response_400, 400
        
        # 讀取比賽資訊，輸出
        games = alchemy_game.search_between(request_json)
        # 使用列表推導式將每個物件轉換為字典
        game_list = [game.as_dict() for game in games]
        return jsonify({'status': 'success', 'games': game_list})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed to search games: {e}'}), 500

@app.route('/update_invitation_time', methods=['POST'])
def update_invitation_time():
    try:
        # 解析 POST 請求中的比賽資訊
        request_json = request.get_json(silent=True)
        if (not alchemy_game.is_update_game_time_valid(request_json)):
            return response_400, 400

        # 寫入比賽資訊到資料庫
        alchemy_game.update_invitation_time(request_json)
        return jsonify({'status': 'success', 'message': 'Update invitation time successfully'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed to update invitation time: {e}'}), 500

@app.route('/update_cancellation_time', methods=['POST'])
def update_cancellation_time():
    try:
        # 解析 POST 請求中的比賽資訊
        request_json = request.get_json(silent=True)
        if (not alchemy_game.is_update_game_time_valid(request_json)):
            return response_400, 400

        # 寫入比賽資訊到資料庫
        alchemy_game.update_cancellation_time(request_json)
        return jsonify({'status': 'success', 'message': 'Update cancellation time successfully'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed to update cancellation time: {e}'}), 500

@app.route('/update_cancellation_announcement_time', methods=['POST'])
def update_cancellation_announcement_time():
    try:
        # 解析 POST 請求中的比賽資訊
        request_json = request.get_json(silent=True)
        if (not alchemy_game.is_update_game_time_valid(request_json)):
            return response_400, 400

        # 寫入比賽資訊到資料庫
        alchemy_game.update_cancellation_announcement_time(request_json)
        return jsonify({'status': 'success', 'message': 'Update cancellation announcement time successfully'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed to update cancellation announcement time: {e}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
