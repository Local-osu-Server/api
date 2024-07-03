from v1.models.api import ConfigUpdate
from sqlalchemy.engine import Engine
from sqlmodel import Session
from v1.models.database.config import Config


def update(config: ConfigUpdate, database_engine: Engine):
    
    # TODO: make a repositories.config.insert function
    database_insertable_config = Config(
        osu_folder_path=config.osu_folder_path,
        osu_username=config.osu_username,
        osu_password=config.osu_password,
        osu_api_v2_client_id=config.osu_api_v2_client_id,
        osu_api_v2_client_secret=config.osu_api_v2_client_secret,
        display_pp_on_leaderboard=config.display_pp_on_leaderboard,
        rank_scores_by_pp_or_score=config.rank_scores_by_pp_or_score,
        allow_pp_from_modified_maps=config.allow_pp_from_modified_maps,
        num_scores_seen_on_leaderboards=config.num_scores_seen_on_leaderboards,
        osu_api_key=config.osu_api_key,
        osu_daily_api_key=config.osu_daily_api_key,    
    )

    try: 
        with Session(database_engine) as session:
            session.add(database_insertable_config)
            session.commit()
    except Exception as e:
        return {"message": f"Error updating config: {e}"}
        
    return {"message": "Config updated successfully"}
    
