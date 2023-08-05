#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Tmpod 2019
#
# This file is part of aiohypixel.
#
# aiohypixel is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# aiohypixel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with aiohypixel. If not, see <https://www.gnu.org/licenses/>.
"""
Achievement models.
"""

__all__ = ("AchievementTier", "TieredAchievement", "OneTimeAchievement", "GamemodeAchievements", "Achievements")

import dataclasses
import datetime
import typing

from ..shared import HypixelModel, APIResponse


@dataclasses.dataclass(frozen=True)
class AchievementTier(HypixelModel):
    """Represents an achievement tier on the Hypixel Network."""

    #: Tier position.
    tier: int
    #: Amount of achievement points gotten from completing this tier.
    points: int
    #: Amount of times the achievement has to be completed for this tier to be completed.
    amount: int

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`AchievementTier` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`AchievementTier` object.
        """
        return cls(tier=resp["tier"], points=resp["points"], amount=resp["amount"])


@dataclasses.dataclass(frozen=True)
class TieredAchievement(HypixelModel):
    """Represents a tiered achievement on the Hypixel Network."""

    #: Code name returned by the API.
    code_name: str
    #: Pretty name for this achievement.
    name: str
    #: Short description for the achievement.
    description: str
    #: List of tiers for this achievement.
    tiers: typing.List[AchievementTier]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`TieredAchievement` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`TieredAchievement` object.
        """
        name = list(resp)[0]
        return cls(
            code_name=name,
            name=resp[name]["name"],
            description=resp[name]["description"],
            tiers=[AchievementTier.from_api_response(t) for t in resp[name]["tiers"]],
        )


@dataclasses.dataclass(frozen=True)
class OneTimeAchievement(HypixelModel):
    """Represents a one-time achievement on the Hypixel Network."""

    #: Code name returned by the API.
    code_name: str
    #: Pretty name for this achievement.
    name: str
    #: Short description for the achievement.
    description: str
    #: Amount of achievement points gotten from completing this achievement.
    points: int

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`OneTimeAchievement` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`OneTimeAchievement` object.
        """
        # I could maybe iterate through the dict since there's only one key ever,
        # but idk if that would be clearer.
        name = list(resp)[0]
        return cls(
            code_name=name,
            name=resp[name]["name"],
            description=resp[name]["description"],
            points=resp[name]["points"],
        )


@dataclasses.dataclass(frozen=True)
class GamemodeAchievements(HypixelModel):
    """Represents the collection of achievements for a gamemode on the Hypixel Network."""

    #: Collection of one-time achievements for this gamemode.
    one_time: typing.List[OneTimeAchievement]
    #: Collection of tiered achievements for this gamemode.
    tiered: typing.List[TieredAchievement]
    #: Total achievements points for this gamemode.
    total_points: int
    #: Total legacy achievement points for this gamemode.
    total_legacy_points: int

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`GamemodeAchievements` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`GamemodeAchievements` object.
        """
        return cls(
            one_time=[
                OneTimeAchievement.from_api_response(a) for a in resp["one_time"]
            ],
            tiered=[TieredAchievement.from_api_response(a) for a in resp["tiered"]],
            total_points=resp["total_points"],
            total_legacy_points=resp["total_legacy_points"],
        )


@dataclasses.dataclass(frozen=True)
class Achievements(HypixelModel):
    """
    Represents the current achievements on the Hypixel Network.
    """

    #: Time this resource was last modified.
    last_updated_at: datetime.datetime
    #: Arcade achievements.
    arcade: GamemodeAchievements
    #: Arena Brawl achievements.
    arena: GamemodeAchievements
    #: Bed Wars achievements.
    bedwars: GamemodeAchievements
    #: Blitz Survival Games achievements.
    blitz: GamemodeAchievements
    #: Build Battle achievements.
    build_battle: GamemodeAchievements
    #: Christmas achievements.
    xmas: GamemodeAchievements
    #: Halloween achievements.
    halloween: GamemodeAchievements
    #: Cops and Crims achievements.
    cops_and_crims: GamemodeAchievements
    #: Duels achievements.
    duels: GamemodeAchievements
    #: Easter achievements.
    easter: GamemodeAchievements
    #: General achievements.
    general: GamemodeAchievements
    #: Turbo Kart Racers achievements.
    turbo_kart_racers: GamemodeAchievements
    #: Housing achievements.
    housing: GamemodeAchievements
    #: Murder Mystery achievements.
    murder_mystery: GamemodeAchievements
    #: PaintBall achievements.
    paintball: GamemodeAchievements
    #: Quake achievements.
    quake: GamemodeAchievements
    #: SkyBlock achievements.
    skyblock: GamemodeAchievements
    #: SkyClash achievements.
    skyclash: GamemodeAchievements
    #: SkyWars achievements.
    skywars: GamemodeAchievements
    #: Speed UHC achievements.
    speed_uhc: GamemodeAchievements
    #: Smash Heroes achievements.
    smash_heroes: GamemodeAchievements
    #: TNT Games achievements.
    tnt_games: GamemodeAchievements
    #: Crazy Walls achievements.
    crazy_walls: GamemodeAchievements
    #: UHC Champions achievements.
    uhc: GamemodeAchievements
    #: VampireZ achievements.
    vampirez: GamemodeAchievements
    #: Walls achievements.
    walls: GamemodeAchievements
    #: Mega Walls achievements.
    mega_wall: GamemodeAchievements
    #: Warlods achievements.
    warlords: GamemodeAchievements

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`Achievements` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`Achievements` object.
        """
        achievements = resp["achievements"]
        return cls(
            last_updated_at=datetime.datetime.utcfromtimestamp(
                resp["lastUpdated"] / 1000
            ),
            arcade=GamemodeAchievements.from_api_response(achievements["arcade"]),
            arena=GamemodeAchievements.from_api_response(achievements["arena"]),
            bedwars=GamemodeAchievements.from_api_response(achievements["bedwars"]),
            blitz=GamemodeAchievements.from_api_response(achievements["blitz"]),
            build_battle=GamemodeAchievements.from_api_response(
                achievements["buildbattle"]
            ),
            xmas=GamemodeAchievements.from_api_response(achievements["christmas2017"]),
            halloween=GamemodeAchievements.from_api_response(
                achievements["halloween2017"]
            ),
            cops_and_crims=GamemodeAchievements.from_api_response(
                achievements["copsandcrims"]
            ),
            duels=GamemodeAchievements.from_api_response(achievements["duel"]),
            easter=GamemodeAchievements.from_api_response(achievements["easter"]),
            general=GamemodeAchievements.from_api_response(achievements["general"]),
            turbo_kart_racers=GamemodeAchievements.from_api_response(
                achievements["gingerbread"]
            ),
            housing=GamemodeAchievements.from_api_response(achievements["housing"]),
            murder_mystery=GamemodeAchievements.from_api_response(
                achievements["murdermystery"]
            ),
            paintball=GamemodeAchievements.from_api_response(achievements["paintball"]),
            quake=GamemodeAchievements.from_api_response(achievements["quake"]),
            skyblock=GamemodeAchievements.from_api_response(achievements["skyblock"]),
            skyclash=GamemodeAchievements.from_api_response(achievements["skyclash"]),
            skywars=GamemodeAchievements.from_api_response(achievements["skywars"]),
            speed_uhc=GamemodeAchievements.from_api_response(achievements["speeduhc"]),
            smash_heroes=GamemodeAchievements.from_api_response(
                achievements["supersmash"]
            ),
            tnt_games=GamemodeAchievements.from_api_response(achievements["tntgames"]),
            crazy_walls=GamemodeAchievements.from_api_response(
                achievements["truecombat"]
            ),
            uhc=GamemodeAchievements.from_api_response(achievements["uhc"]),
            vampirez=GamemodeAchievements.from_api_response(achievements["vampirez"]),
            walls=GamemodeAchievements.from_api_response(achievements["walls"]),
            mega_wall=GamemodeAchievements.from_api_response(achievements["walls3"]),
            warlords=GamemodeAchievements.from_api_response(achievements["warlords"]),
        )
