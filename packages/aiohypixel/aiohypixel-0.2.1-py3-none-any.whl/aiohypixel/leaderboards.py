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
Leaderboards dataclasses
"""

__all__ = ("Leaderboards",)

from dataclasses import dataclass
import enum
import typing
import uuid

from .shared import HypixelModel, APIResponse
from .player import Player


class LeaderboardType(enum.Enum):
    """Represents the type of a leaderboard."""
    OVERALL = enum.auto()
    MONTHLY = enum.auto()
    WEEKLY = enum.auto()
    DAILY = enum.auto()


@dataclass(frozen=True)
class Leaderboard(HypixelModel):
    """Represents a single leaderboard for a gamemode on the Hypixel Network."""

    #: Code name given by the API.
    code_name: str
    #: Leaderboard type
    type: LeaderboardType
    size: int
    location: typing.Tuple[int, int, int]
    leaders: typing.List[typing.Union[uuid.UUID, Player]]

    @classmethod
    def from_api_response(cls, resp: APIResponse, cast_leaders_to_player: bool = False):
        """
        Processes the raw API response into a :class:`GuildTag` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`GuildTag` object.
        """
        if cast_leaders_to_player:
            leaders = ...
            raise NotImplementedError
        else:
            leaders = [uuid.UUID(l) for l in resp["leaders"]]

        return cls(
            code_name=resp["path"],
            type=LeaderboardType[resp["prefix"].upper()],
            size=resp["count"],
            location=tuple(int(i) for i in resp["location"].split(",")),
            leaders=leaders,
        )


# NOTE: Should I remove 'cast_leaders_to_player'?
@dataclass(frozen=True)
class Leaderboards(HypixelModel):
    """Represents the current state of the leaderboards on the Hypixel Network."""

    #: Arcade leaderboards.
    arcade: typing.List[Leaderboard]
    #: Arena Brawl leaderboards.
    arena: typing.List[Leaderboard]
    #: Bed Wars leaderboards.
    bedwars: typing.List[Leaderboard]
    #: Blitz Survival Games leaderboards.
    blitz: typing.List[Leaderboard]
    #: Build Battle leaderboards.
    build_battle: typing.List[Leaderboard]
    #: Cops and Crims leaderboards.
    cops_and_crims: typing.List[Leaderboard]
    #: Duels leaderboards.
    duels: typing.List[Leaderboard]
    #: Turbo Kart Racers leaderboards.
    turbo_kart_racers: typing.List[Leaderboard]
    #: Housing leaderboards.
    housing: typing.List[Leaderboard]
    #: Murder Mystery leaderboards.
    murder_mystery: typing.List[Leaderboard]
    #: PaintBall leaderboards.
    paintball: typing.List[Leaderboard]
    #: Quake leaderboards.
    quake: typing.List[Leaderboard]
    #: SkyClash leaderboards.
    skyclash: typing.List[Leaderboard]
    #: SkyWars leaderboards.
    skywars: typing.List[Leaderboard]
    #: Speed UHC leaderboards.
    speed_uhc: typing.List[Leaderboard]
    #: Smash Heroes leaderboards.
    smash_heroes: typing.List[Leaderboard]
    #: TNT Games leaderboards.
    tnt_games: typing.List[Leaderboard]
    #: Crazy Walls leaderboards.
    crazy_walls: typing.List[Leaderboard]
    #: UHC Champions leaderboards.
    uhc: typing.List[Leaderboard]
    #: VampireZ leaderboards.
    vampirez: typing.List[Leaderboard]
    #: Walls leaderboards.
    walls: typing.List[Leaderboard]
    #: Mega Walls leaderboards.
    mega_wall: typing.List[Leaderboard]
    #: Warlods leaderboards.
    warlords: typing.List[Leaderboard]
    #: Prototype Lobby games leaderboards.
    prototype: typing.List[Leaderboard]

    @classmethod
    def from_api_response(cls, resp: APIResponse, cast_leaders_to_player: bool = False):
        """
        Processes the raw API response into a :class:`Leaderboards` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`Leaderboards` object.
        """
        leaderboards = resp["leaderboards"]
        return cls(
            arcade=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["ARCADE"]
            ],
            arena=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["ARENA"]
            ],
            bedwars=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["BEDWARS"]
            ],
            blitz=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["SURVIVAL_GAMES"]
            ],
            build_battle=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["BUILD_BATTLE"]
            ],
            cops_and_crims=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["MCGO"]
            ],
            duels=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["DUELS"]
            ],
            turbo_kart_racers=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["GINGERBREAD"]
            ],
            murder_mystery=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["MURDER_MYSTERY"]
            ],
            paintball=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["PAINTBALL"]
            ],
            quake=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["QUAKE"]
            ],
            skyclash=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["SKYCLASH"]
            ],
            skywars=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["SKYWARS"]
            ],
            speed_uhc=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["SPEED_UHC"]
            ],
            smash_heroes=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["SUPER_SMASH"]
            ],
            tnt_games=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["TNTGAMES"]
            ],
            crazy_walls=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["TRUE_COMBAT"]
            ],
            uhc=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["UHC"]
            ],
            vampirez=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["VAMPIREZ"]
            ],
            walls=[Leaderboard.from_api_response(l) for l in leaderboards["WALLS"]],
            mega_wall=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["WALLS3"]
            ],
            battleground=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["BATTLEGROUND"]
            ],
            prototype=[
                Leaderboard.from_api_response(l, cast_leaders_to_player)
                for l in leaderboards["PROTOTYPE"]
            ],
        )
