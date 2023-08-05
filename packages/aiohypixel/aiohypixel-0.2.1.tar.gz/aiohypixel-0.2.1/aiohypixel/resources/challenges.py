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
Challenge models.
"""

__all__ = ("ChallengeReward", "Challenge", "Challenges")

import dataclasses
import datetime
import typing

from ..shared import HypixelModel, APIResponse


@dataclasses.dataclass(frozen=True)
class ChallengeReward(HypixelModel):
    """Represents a challenge reward on the Hypixel Network."""

    #: Type of this reward.
    type: str
    #: Amount of :attr:`type` the player gets.
    amount: int

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`ChallengeReward` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`ChallengeReward` object.
        """
        return cls(type=resp["type"], amount=resp["amount"])


@dataclasses.dataclass(frozen=True)
class Challenge(HypixelModel):
    """Represents a challenge on the Hypixel Network."""

    #: ID for this challenge.
    id: str
    #: Pretty challenge name.
    name: str
    #: Rewards gotten upon completing the challenge.
    rewards: typing.List[ChallengeReward]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`Challenge` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`Challenge` object.
        """
        return cls(
            id=resp["id"],
            name=resp["name"],
            rewards=[ChallengeReward.from_api_response(r) for r in resp["rewards"]],
        )


@dataclasses.dataclass(frozen=True)
class Challenges(HypixelModel):
    """Represent the currently available challenges on the Hypixel Network."""

    #: Time this resource was last modified.
    last_updated_at: datetime.datetime
    #: Arcade challenges.
    arcade: typing.List[Challenge]
    #: Arena Brawl challenges.
    arena: typing.List[Challenge]
    #: Bed Wars challenges.
    bedwars: typing.List[Challenge]
    #: Blitz Survival Games challenges.
    blitz: typing.List[Challenge]
    #: Build Battle challenges.
    build_battle: typing.List[Challenge]
    #: Cops and Crims challenges.
    cops_and_crims: typing.List[Challenge]
    #: Duels challenges.
    duels: typing.List[Challenge]
    #: Turbo Kart Racers challenges.
    turbo_kart_racers: typing.List[Challenge]
    #: Housing challenges.
    housing: typing.List[Challenge]
    #: Murder Mystery challenges.
    murder_mystery: typing.List[Challenge]
    #: PaintBall challenges.
    paintball: typing.List[Challenge]
    #: Quake challenges.
    quake: typing.List[Challenge]
    #: SkyBlock challenges.
    skyblock: typing.List[Challenge]
    #: SkyClash challenges.
    skyclash: typing.List[Challenge]
    #: SkyWars challenges.
    skywars: typing.List[Challenge]
    #: Speed UHC challenges.
    speed_uhc: typing.List[Challenge]
    #: Smash Heroes challenges.
    smash_heroes: typing.List[Challenge]
    #: TNT Games challenges.
    tnt_games: typing.List[Challenge]
    #: Crazy Walls challenges.
    crazy_walls: typing.List[Challenge]
    #: UHC Champions challenges.
    uhc: typing.List[Challenge]
    #: VampireZ challenges.
    vampirez: typing.List[Challenge]
    #: Walls challenges.
    walls: typing.List[Challenge]
    #: Mega Walls challenges.
    mega_wall: typing.List[Challenge]
    #: Warlods challenges.
    warlords: typing.List[Challenge]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`Challenges` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`Challenges` object.
        """
        challenges = resp["challenges"]
        return cls(
            last_updated_at=datetime.datetime.utcfromtimestamp(
                resp["lastUpdated"] / 1000
            ),
            arcade=[Challenge.from_api_response(q) for q in challenges["arcade"]],
            arena=[Challenge.from_api_response(q) for q in challenges["arena"]],
            bedwars=[Challenge.from_api_response(q) for q in challenges["bedwars"]],
            hungergames=[
                Challenge.from_api_response(q) for q in challenges["hungergames"]
            ],
            build_battle=[
                Challenge.from_api_response(q) for q in challenges["buildbattle"]
            ],
            cops_and_crims=[Challenge.from_api_response(q) for q in challenges["mcgo"]],
            duels=[Challenge.from_api_response(q) for q in challenges["duel"]],
            turbo_kart_racers=[
                Challenge.from_api_response(q) for q in challenges["gingerbread"]
            ],
            murder_mystery=[
                Challenge.from_api_response(q) for q in challenges["murdermystery"]
            ],
            paintball=[Challenge.from_api_response(q) for q in challenges["paintball"]],
            quake=[Challenge.from_api_response(q) for q in challenges["quake"]],
            skyblock=[Challenge.from_api_response(q) for q in challenges["skyblock"]],
            skyclash=[Challenge.from_api_response(q) for q in challenges["skyclash"]],
            skywars=[Challenge.from_api_response(q) for q in challenges["skywars"]],
            speed_uhc=[Challenge.from_api_response(q) for q in challenges["speeduhc"]],
            smash_heroes=[
                Challenge.from_api_response(q) for q in challenges["supersmash"]
            ],
            tnt_games=[Challenge.from_api_response(q) for q in challenges["tntgames"]],
            crazy_walls=[
                Challenge.from_api_response(q) for q in challenges["truecombat"]
            ],
            uhc=[Challenge.from_api_response(q) for q in challenges["uhc"]],
            vampirez=[Challenge.from_api_response(q) for q in challenges["vampirez"]],
            walls=[Challenge.from_api_response(q) for q in challenges["walls"]],
            mega_wall=[Challenge.from_api_response(q) for q in challenges["walls3"]],
            battleground=[
                Challenge.from_api_response(q) for q in challenges["battleground"]
            ],
        )
