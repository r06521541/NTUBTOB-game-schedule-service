from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy import update, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from connect import connect_with_connector, get_table_name, get_schema_name

Base = declarative_base()

required_add_game_fields = ['year', 'season', 'start_datetime', 'duration', 'location', 'home_team', 'away_team']
    
class Game(Base):
    __tablename__ = get_table_name()
    __table_args__ = {'schema': get_schema_name()}

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    season = Column(Integer)
    start_datetime = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer)
    location = Column(String)
    home_team = Column(String)
    away_team = Column(String)
    invitation_time = Column(DateTime)
    cancellation_announcement_time = Column(DateTime)
    
    def as_dict(self):    
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
        # Convert datetime to ISO 8601 format
        if 'start_datetime' in result and isinstance(result['start_datetime'], datetime):
            result['start_datetime'] = result['start_datetime'].isoformat()
        if 'invitation_time' in result and isinstance(result['invitation_time'], datetime):
            result['invitation_time'] = result['invitation_time'].isoformat()
        if 'cancellation_announcement_time' in result and isinstance(result['cancellation_announcement_time'], datetime):
            result['cancellation_announcement_time'] = result['cancellation_announcement_time'].isoformat()

        return result
        
# 配置 SQLAlchemy 引擎
engine = connect_with_connector()

def is_game_json_valid(game_json):
    return all(field in game_json for field in required_add_game_fields)

def add_game(game_json):
    
    # 創建 Session 來處理資料庫操作
    Session = sessionmaker(bind=engine)
    session = Session()

    # 建立新比賽物件
    new_game = Game(year = game_json['year'], 
                    season = game_json['season'],
                    start_datetime = game_json['start_datetime'],
                    duration = game_json['duration'],
                    location = game_json['location'],
                    home_team = game_json['home_team'],
                    away_team = game_json['away_team'])

    # 加入資料庫
    session.add(new_game)
    session.commit()

    # 關閉 Session
    session.close()

def is_search_game_json_valid(json):
    required_fields = ['start_time', 'end_time']
    return all(field in json for field in required_fields)

def search_games_between(json):    
    Session = sessionmaker(bind=engine)
    session = Session()

    start_time = json['start_time']
    end_time = json['end_time']

    games = session.query(Game).filter(
        and_(
            Game.start_datetime.between(start_time, end_time),
            Game.cancellation_announcement_time == None
        )
    ).all()

    # 關閉 Session
    session.close()

    return games

def search_games_for_invitation(json):    
    Session = sessionmaker(bind=engine)
    session = Session()

    start_time = json['start_time']
    end_time = json['end_time']

    games = session.query(Game).filter(
        and_(
            Game.start_datetime.between(start_time, end_time),
            Game.invitation_time == None,
            Game.cancellation_announcement_time == None
        )
    ).all()

    # 關閉 Session
    session.close()

    return games

def is_update_game_time_valid(json):
    required_fields = ['id', 'time']
    return all(field in json for field in required_fields)

def update_invitation_time(json):
    
    # 創建 Session 來處理資料庫操作
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 加入資料庫
    game_id = json['id']  # 替換為實際的比賽 ID
    time = json['time']

    session.execute(update(Game).where(Game.id == game_id).values(invitation_time=time))
    session.commit()

    # 關閉 Session
    session.close()

def update_cancellation_time(json):
    
    # 創建 Session 來處理資料庫操作
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 加入資料庫
    game_id = json['id']  # 替換為實際的比賽 ID
    time = json['time']

    session.execute(update(Game).where(Game.id == game_id).values(cancellation_announcement_time=time))
    session.commit()

    # 關閉 Session
    session.close()

