import random
import time
import uuid
from copy import deepcopy

import dask
import numpy as np
import pandas as pd
from crayons import blue, cyan, green, magenta, red, white, yellow
from funtime import Converter, Store

from funhandler.stochastic.base import StochasticGenerator

stg = StochasticGenerator()


def generate_session(session_id, num=1000, session_type="gbm", trend_rate=0.5):
    session_list = []
    current_time = round(time.time(), 0)
    base = {"type": "session", "session_id": session_id}

    close = stg.generate(num, random.uniform(0.01, 1000), interest_rate=trend_rate, _type=session_type.upper())
    volume = stg.generate(
        num,
        random.normalvariate(10000, 3000),
        interest_rate=random.normalvariate(1.0, 1.5),
        _type=session_type.upper())
    close = list(close)
    volume = list(volume)
    for i in range(num):
        bb = deepcopy(base)
        bb["close"] = close.pop(0)
        bb["open"] = bb["close"] * random.normalvariate(1.0, 0.05)
        bb["high"] = bb["close"] * random.normalvariate(1.1, 0.01)
        bb["low"] = bb["close"] * random.normalvariate(.94, 0.05)
        bb["volume"] = volume.pop(0)
        bb["timestamp"] = current_time + (i*60)
        session_list.append(bb)

    return session_list


# class Handler(object):
#     def __init__(self):
#         # self._store = Store("localhost").create_lib("_global").get_store()['_global']
#         self.session_dict = {}
#         self.episode_dict = {}

#     def generate_stochastic_episodes(
#             self,
#             episode_number=10,
#             types_per_episode=['GBM', 'HESTON', 'MERTON'],
#             sessions_per_episode=10,
#             steps_per_session=100):
#         """ Generate a local set of stochastic episodes. Reference a set id for all of the episodes """
#         # TODO: Create a list and save using funtime

#         # TODO: Create a bulk insert

#         self.episodes = []
#         self.session_types = types_per_episode
#         # Create episodes
#         # Create sessions first. Save sessions to an episode using an ID
#         # Save an episode to a set using a reference ID


#         set_id = str(uuid.uuid4())
#         for _ in range(episode_number):
#             nepisode_id = str(uuid.uuid4())
#             self.episodes.append(nepisode_id)
#             self._store.store({
#                 "type": "ref",
#                 "refname": "set_episode",
#                 "episode_id": nepisode_id,
#                 "set_id": set_id,
#                 "timestamp": time.time()
#             })



#         for ep in self.episodes:
#             for __ in range(sessions_per_episode):
#                 session_id = str(uuid.uuid4())
#                 self._store.store({
#                     "type": "ref",
#                     "ref_name": "episode_sess",
#                     "episode_id": ep,
#                     "session_id": session_id,
#                     "timestamp": time.time()
#                 })
#                 # Randomly pick between the options: [GEO, JUMP, DIFFUSION]
#                 step_sess = generate_session(
#                     session_id,
#                     num=steps_per_session,
#                     trend_rate=random.normalvariate(0.0, 0.60),
#                     session_type=types_per_episode
#                 )
#                 # print(step_sess[-1])
#                 # dask_computations = []
#                 self._store.bulk_upsert(step_sess, _column_first=["type", "session_id"])

#                 # dask.compute(*dask_computations)
#         print("Done creating sessions")
#         # print(list(self._store.query({"type": "session"})))
#         # print(f"Set_ID: {set_id} \n\nEpisodes: {self.episodes}")
#         return set_id

#     def get_episodes(self, set_id):
#         episodes = list(self._store.query({"type": "ref", "refname": "set_episode", "set_id": set_id}))
#         episode_ids = []
#         if len(episodes) > 0:
#             for ep in episodes:
#                 del ep['timestamp']
#                 episode_ids.append(ep["episode_id"])
#         return episode_ids

#     def get_sessions(self, episode_id):
#         session_list = []
#         sessions = list(self._store.query_latest({
#             "type": "ref",
#             "ref_name": "episode_sess",
#             "episode_id": episode_id,
#         }))
#         for s in sessions:
#             session_list.append(s["session_id"])
#         self.episode_dict[episode_id] = session_list
#         return session_list

#     def load_session(self, session_id):
#         results = list(self._store.query({
#             "type": "session",
#             "session_id": session_id
#         }))

#         sss = Converter().to_dataframe(results)
#         if len(sss) == 0:
#             return None
#         ts = sss['timestamp']
#         dt = pd.to_datetime(ts, unit='s')
#         sss = sss.drop(['timestamp'], axis=1)
#         sss = sss.set_index(pd.DatetimeIndex(dt))
#         sss = sss.sort_index(ascending=False)
#         is_below = (sss.iloc[-1]['close'] < 40)
#         if is_below:
#             sss['base'] = "BTC"
#         else:
#             sss['base'] = "USD"

#         self.session_dict[session_id] = sss

#         # Get the last
#         print(sss)

#         return self.session_dict[session_id]

#     def pop_session(self, episode_id):
#         sessions = self.episode_dict.get(episode_id)
#         if sessions == None or len(sessions) == 0:
#             return None
#         session_id = self.episode_dict[episode_id].pop(0)
#         return session_id

#     def is_sessions(self, episode_id):
#         sessions = self.episode_dict.get(episode_id)
#         if sessions == None:
#             return False
#         elif len(sessions) == 0:
#             return False
#         else:
#             return True

#     def is_session(self, session_id):
#         session = self.session_dict.get(session_id, None)
#         if session is None:
#             return False

#         if not isinstance(session, pd.DataFrame):
#             return False

#         # if limit provided then it will be the number of rows returned back.

#         if len(session) == 0:
#             return False

#         return True


#     def pop_data(self, session_id, **kwargs):
#         session = self.session_dict.get(session_id, None)
#         if session is None:
#             return False

#         if not isinstance(session, pd.DataFrame):
#             return False

#         # if limit provided then it will be the number of rows returned back.

#         if len(session) == 0:
#             return False

#         limit = kwargs.get('limit', 1)
#         result = session.tail(limit).sort_index(ascending=True)
#         session.drop(session.tail(1).index, inplace=True)  # Pop only one bar
#         return result
#     def is_limit(self, frame, limit):
#         if len(frame) >= limit:
#             return True
#         else:
#             return False



class InMemoryHandler(object):
    def __init__(self):
        """ Handle the creation of the stochastic variables without storing it into the database (for speed purposes) """
        # self._store = Store("localhost").create_lib(
        #     "_global").get_store()['_global']
        self.session_dict = {}
        self.episode_dict = {}
        self.net_episode_dict = {}

    def generate_coin_in_episode(self,
            eid:str,
            coin_name:str,
            steps_in_coin=1000, **kwargs):

        random_choice = random.choice(["GBM", "HESTON", "MERTON"])
        stohastic_type = kwargs.get("stochastic_type", random_choice)
        # Check to see if episode exist
        current_episode = self.net_episode_dict.get(eid)

        if current_episode is None:
            # If episode doesn't exist, add it to the episode dictionary
            self.net_episode_dict[eid] = {}


        # Check to see if coin exist
        current_coin = self.net_episode_dict[eid].get(coin_name)
        if current_coin is None:
            # If the coin doesn't exist, add it to the episode dictionary
            self.net_episode_dict[eid][coin_name] = []




        # Choose a trend for the stochatsic variable function
        trend_rate = random.normalvariate(0.0, 0.60)


        step_sess = generate_session(
            coin_name,
            num=steps_in_coin,
            trend_rate=random.normalvariate(0.0, 0.60),
            session_type=stohastic_type)

        step_frame = pd.DataFrame(step_sess)
        ts_extract = step_frame.timestamp
        datetime_index = pd.to_datetime(ts_extract, unit='s')
        step_frame = step_frame.set_index(datetime_index)
        step_frame.drop("timestamp", axis=1)
        self.net_episode_dict[eid][coin_name] = step_frame


    def pop_coin(self, eid: str, coin_name: str, **kwargs):
        episode = self.net_episode_dict.get(eid, None)
        if episode is None:
            return None

        coin = episode.get(coin_name)

        if not isinstance(coin, pd.DataFrame):
            return None

        # # if limit provided then it will be the number of rows returned back.

        if len(coin) == 0:
            return None

        coin = coin.sort_index(ascending=False)

        limit = kwargs.get('limit', 1)
        result = coin.tail(limit).sort_index(ascending=True)
        coin.drop(coin.tail(1).index, inplace=True)  # Pop only one bar
        self.net_episode_dict[eid][coin_name] = coin
        return result


    def is_coins_in_episode(self, eid):
        episode = self.net_episode_dict.get(eid, None)

        if episode is None:
            return False

        # Get all of the coins for a given episode
        coins = episode.keys()
        if len(coins) == 0:
            return False

        # Check all coins in the episode. If the coins still have anything inside of the return True

        for coin in coins:
            ccoin = episode[coin]
            if len(ccoin) > 0:
                return True
        return False

    def is_price_in_coin(self, eid, coin):
        episode = self.net_episode_dict.get(eid, None)

        if episode is None:
            return False

        # Get all of the coins for a given episode
        coins = episode.keys()
        if len(coins) == 0:
            return False

        current_coin = episode[coin]
        if len(current_coin) == 0:
            return False
        return True

    def is_all_episodes_done(self):
        """ Check to see if all episodes are empty """
        episode_list = list(self.net_episode_dict.keys())
        for eid in episode_list:

            episode = self.net_episode_dict.get(eid, None)

            if episode is None:
                return True

            # Get all of the coins for a given episode
            coins = episode.keys()
            if len(coins) == 0:
                return True

            # Check all coins in the episode. If the coins still have anything inside of the return True

            for coin in coins:
                ccoin = episode[coin]

                if len(ccoin) == 0:
                    return True

        return True

    def is_coin_done(self, episode, coin, index_len=150):
        """ Checks to see if there's any more coins left in the frame"""
        episode = self.net_episode_dict.get(episode, None)
        
        if episode is None:
            return True

        # Get all of the coins for a given episode
        coins = episode.keys()
        if len(coins) == 0:
            return True

        current_coin = episode.get(coin, [])
        if len(current_coin) >= index_len:
            return False
        return True


    def pop_session(self, episode_id):
        sessions = self.episode_dict.get(episode_id) # Instead of popping the session we're just going to get the coin
        if sessions == None or len(sessions) == 0:
            return None
        session_id = self.episode_dict[episode_id].pop(0)
        return session_id

    def is_sessions(self, episode_id):
        sessions = self.episode_dict.get(episode_id) # this should be a list
        if sessions == None:
            return False
        elif len(sessions) == 0:
            return False
        else:
            return True

    def is_session(self, session_id):
        session = self.session_dict.get(session_id, None)
        if session is None:
            return False

        if not isinstance(session, pd.DataFrame):
            return False

        # if limit provided then it will be the number of rows returned back.

        if len(session) == 0:
            return False

        return True

    def pop_data(self, session_id, **kwargs):
        session = self.session_dict.get(session_id, None)
        if session is None:
            return False

        if not isinstance(session, pd.DataFrame):
            return False

        # if limit provided then it will be the number of rows returned back.

        if len(session) == 0:
            return False

        limit = kwargs.get('limit', 1)
        result = session.tail(limit).sort_index(ascending=False)
        session.drop(session.tail(1).index, inplace=True)  # Pop only one bar
        return result

    def is_limit(self, frame, limit):
        if len(frame) >= limit:
            return True
        else:
            return False



def main():

    handle = InMemoryHandler()
    episodes = [uuid.uuid4().hex for x in range(1)]
    coins = ["BTC", "ETH", "XRP"]
    limit = 100
    for eid in episodes:
        for coin in coins:
            handle.generate_coin_in_episode(
                eid,
                coin
            )
    # Create all of the coins first

    while True:
        for eid in episodes:
            # Check to see if coins are all done for the given episode
            if handle.is_coins_in_episode(eid) == False:
                continue
            for coin in coins:
                # Check to see if the coin is out of price information


                coin_data = handle.pop_coin(eid, coin, limit=limit)
                if coin_data is not None:
                    if len(coin_data) >= limit:
                        print(handle.is_coin_done(eid, coin, limit))
                    else:
                        break
                
        # If so, break the loop
        is_done = handle.is_all_episodes_done()
        if is_done:
            break
        # print("\n\n")


if __name__ == "__main__":
    main()
    # episode_id = uuid.uuid4().hex
    # handle = InMemoryHandler()
    # handle.generate_coin_in_episode(
    #     episode_id,
    #     "BTC",
    # )


    # limit = 100
    # while True:

    #     coin_data = handle.pop_coin(episode_id, "BTC", limit=limit)
    #     if coin_data is not None:
    #         if len(coin_data) >= limit:
    #             print(coin_data)
    #         else:
    #             break

    # set_id = handle.generate_stochastic_episodes(
    #     episode_number=5,
    #     sessions_per_episode=3,
    #     steps_per_session=1000
    # )
    # # set_id = "027da34a-4289-4dd2-aa19-01a6a05cda03"
    # # set_id = "869b57bf-00bf-4281-9531-a2cea01a3c35"
    # # set_id = "726241df-f49f-42c8-b6e4-3fcff08d5744"
    # print(set_id)
    # time.sleep(5)
    # limit=100
    # episodes = handle.get_episodes(set_id)
    # for eps in episodes:
    #     eid = uuid.uuid4().hex
    #     sessions = handle.get_sessions(eps)
    #     while handle.is_sessions(eps):
    #         session_id = handle.pop_session(eps)
    #         print(f"Trying session: {session_id}")
    #         handle.load_session(session_id)
    #         while handle.is_session(session_id):
    #             result = handle.pop_data(session_id, limit=limit)
    #             if handle.is_limit(result, limit):
    #                 print(result)
    # print("Working")
    # print(eid)
    # print(sess)
    # print(session)
    # break
    # for s in sessions:
    #     print(session)
    # print(sessions)
    # {
    #     "type": "ref",
    #     "ref_name": "episode_sess"
    # }
    # for eps in episodes:
    #     print(f"Running Episode: {eps}")
    #     # In place of client.start_episode()
    #     while handle.is_sessions(eps):
    #         session_id = handle.pop_session(eps)
    #         while handle.is_session(session_id=session_id): # while the session still has data
    #             data = handle.pop_data(session_id=session_id)
    #             preprocessed = np.linspace(1, 100, num=1000) * data # Do this to simulate live feature engineering
    #             action = random.choice([1, 2, 3, 4])
    #             reward = random.uniform(0, 100)
    #             if reward != None:
    #                 print(f"Log returns: {reward}")
