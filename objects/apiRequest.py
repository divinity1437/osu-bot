import requests

import glob
import json

class New():

	def __init__(self):

		# Profile part
		self.username = None
		self.user_id = None
		self.join_date = None
		self.pp_rank = None
		self.pp_raw = None
		self.count300 = None
		self.count100 = None
		self.count50 = None
		self.level = None
		self.accuracy = None
		self.country = None
		self.pp_country_rank = None
		self.playcount = None
		self.found = False
		self.country_acronym = None

		# Score part
		self.beatmap_id = None
		self.score = None
		self.maxcombo = None
		self.countmiss = None
		self.perfect = None
		self.enabled_mods = None
		self.date = None
		self.rank = None
		self.score_id = None

		# Beatmap part
		self.beatmapset_id = None
		self.beatmap_id = None
		self.total_length = None
		self.diff_size = None # cs
		self.diff_overall = None # od
		self.diff_approach = None # ar 
		self.diff_drain = None # hp
		self.artist = None
		self.title = None
		self.creator = None
		self.creator_id = None
		self.bpm = None
		self.max_combo = None
		self.difficultyrating = None
		self.version = None


	def get_user(self,entry):

		response = requests.get(f"https://osu.ppy.sh/api/get_user?k={glob.osu_api_key}&u={entry}").json()
		
		if not response:
			return
		self.found = True

		user_dict = response[0]

		self.username = user_dict["username"]
		self.user_id = user_dict["user_id"]
		self.join_date = user_dict["join_date"]
		self.pp_rank = user_dict["pp_rank"]
		self.pp_raw = user_dict["pp_raw"]
		self.count300 = user_dict["count300"]
		self.count100 = user_dict["count100"]
		self.count50 = user_dict["count50"]
		self.level = user_dict["level"]
		self.accuracy = user_dict["accuracy"]
		self.country = user_dict["country"]
		self.pp_country_rank = user_dict["pp_country_rank"]
		self.playcount = user_dict["playcount"]
		self.country_acronym = user_dict["country"]

	def get_beatmaps(self,entry):

		response = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={glob.osu_api_key}&b={entry}").json() 

		if not response:
			return

		user_dict = response[0]

		self.beatmapset_id = user_dict["beatmapset_id"]
		self.beatmap_id = user_dict["beatmap_id"]
		self.total_length = user_dict["total_length"]
		self.diff_size = user_dict["diff_size"] # cs
		self.diff_overall = user_dict["diff_overall"] # od
		self.diff_approach = user_dict["diff_approach"] # ar 
		self.diff_drain  = user_dict["diff_drain"] # hp
		self.artist = user_dict["artist"]
		self.title = user_dict["title"]
		self.creator = user_dict["creator"]
		self.creator_id = user_dict["creator_id"]
		self.bpm = user_dict["bpm"]
		self.max_combo = user_dict["max_combo"]
		self.difficultyrating  = user_dict["difficultyrating"]
		self.version = user_dict["version"]

	def get_user_recent(self,entry):

		response = requests.get(f"https://osu.ppy.sh/api/get_user_recent?k={glob.osu_api_key}&u={entry}").json()

		if not response:
			return

		user_dict = response[0]

		self.user_id = user_dict["user_id"]
		self.beatmap_id = user_dict["beatmap_id"]
		self.score = user_dict["score"]
		self.maxcombo = user_dict["maxcombo"]
		self.count300 = user_dict["count300"]
		self.count100 = user_dict["count100"]
		self.count50 = user_dict["count50"]
		self.countmiss = user_dict["countmiss"]
		self.perfect = user_dict["perfect"]
		self.enabled_mods = user_dict["enabled_mods"]
		self.date = user_dict["date"]
		self.rank = user_dict["rank"]
		self.score_id = user_dict["score_id"]

	def get_user_kurikku(self,entry,mode=0):

		if entry.isnumeric():
			response = requests.get(f"https://kurikku.pw/api/v1/users/full?id={entry}").json()
		else:
			response = requests.get(f"https://kurikku.pw/api/v1/users/full?name={entry}").json()

		if int(response["code"]) == 404:
			return

		self.found = True

		self.username = response["username"]
		self.user_id = response["id"]
		self.join_date = response["registered_on"]

		if mode == 0:
			mode_acronym = "std"
		elif mode == 1:
			mode_acronym = "taiko"
		elif mode == 2:
			mode_acronym = "ctb"
		elif mode == 3:
			mode_acronym = "mania"

		self.pp_rank = response[f"{mode_acronym}"]["global_leaderboard_rank"]
		self.pp_raw = response[f"{mode_acronym}"]["pp"]
		self.count300 = 0 # no count 300 wtf wenin
		self.count100 = 0
		self.count50 = 0
		self.level = response[f"{mode_acronym}"]["level"]
		self.accuracy = response[f"{mode_acronym}"]["accuracy"]
		self.country = response["country"]
		self.pp_country_rank = response[f"{mode_acronym}"]["country_leaderboard_rank"]

		if self.pp_country_rank is None:
			self.pp_country_rank = "Unranked"
		if self.pp_rank is None:
			self.pp_rank = "Unranked"

		self.playcount = response[f"{mode_acronym}"]["playcount"]
		self.country_acronym = response["country"]


