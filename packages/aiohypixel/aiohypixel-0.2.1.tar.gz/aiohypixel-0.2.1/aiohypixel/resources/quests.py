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
Quest models.
"""

__all__ = ("QuestObjective", "QuestReward", "Quest", "Quests")

import dataclasses
import datetime
import enum
import typing

from ..shared import HypixelModel, APIResponse


class QuestObjectiveType(enum.Enum):
    """Represents the type of a quest objective."""

    #: Represents 'IntegerObjective'
    INTEGER_OBJECTIVE = enum.auto()
    # Represents 'BooleanObjective'
    BOOLEAN_OBJECTIVE = enum.auto()


@dataclasses.dataclass(frozen=True)
class QuestObjective(HypixelModel):
    """Represents a quest objective on the Hypixel Network."""

    #: ID for this objective.
    id: str
    type: QuestObjectiveType
    integer: typing.Optional[int] = None

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`QuestObjective` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`QuestObjective` object.
        """
        # I could maybe write this another way with a dict, but for now I'll leave it like this,
        # as there are only two objective types.
        type_ = QuestObjectiveType[resp["type"]]
        if type_ is QuestObjectiveType.INTEGER_OBJECTIVE:
            return cls(id=resp["id"], type=type_, integer=resp["integer"])

        return cls(id=resp["id"], type=type_)


@dataclasses.dataclass(frozen=True)
class QuestReward(HypixelModel):
    """Represents a quest reward on the Hypixel Network."""

    #: Type of this reward.
    type: str
    #: Amount of :attr:`type` the player gets.
    amount: int

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`QuestReward` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`QuestReward` object.
        """
        return cls(type=resp["type"], amount=resp["amount"])


@dataclasses.dataclass(frozen=True)
class Quest(HypixelModel):
    """Represents a quest on the Hypixel Network."""

    #: ID for this quest.
    id: str
    #: Pretty quest name.
    name: str
    #: Short description for the quest.
    description: str
    #: Rewards gotten upon completing the quest.
    rewards: typing.List[QuestReward]
    #: The goals a player has to reach to complete the quest.
    objectives: typing.List[QuestObjective]
    #: The pre-requisites for completing the quest.
    requirements: typing.List[str]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`Quest` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`Quest` object.
        """
        return cls(
            id=resp["id"],
            name=resp["name"],
            description=resp["description"],
            rewards=[QuestReward.from_api_response(r) for r in resp["rewards"]],
            objectives=[
                QuestObjective.from_api_response(r) for r in resp["objectives"]
            ],
            requirements=resp["requirements"],
        )


@dataclasses.dataclass(frozen=True)
class Quests(HypixelModel):
    """
    Represents the currently available quests on the Hypixel Network.
    """

    #: Time this resource was last modified.
    last_updated_at: datetime.datetime
    #: Arcade quests.
    arcade: typing.List[Quest]
    #: Arena Brawl quests.
    arena: typing.List[Quest]
    #: Bed Wars quests.
    bedwars: typing.List[Quest]
    #: Blitz Survival Games quests.
    blitz: typing.List[Quest]
    #: Build Battle quests.
    build_battle: typing.List[Quest]
    #: Cops and Crims quests.
    cops_and_crims: typing.List[Quest]
    #: Duels quests.
    duels: typing.List[Quest]
    #: Turbo Kart Racers quests.
    turbo_kart_racers: typing.List[Quest]
    #: Housing quests.
    housing: typing.List[Quest]
    #: Murder Mystery quests.
    murder_mystery: typing.List[Quest]
    #: PaintBall quests.
    paintball: typing.List[Quest]
    #: Quake quests.
    quake: typing.List[Quest]
    #: SkyBlock quests.
    skyblock: typing.List[Quest]
    #: SkyClash quests.
    skyclash: typing.List[Quest]
    #: SkyWars quests.
    skywars: typing.List[Quest]
    #: Speed UHC quests.
    speed_uhc: typing.List[Quest]
    #: Smash Heroes quests.
    smash_heroes: typing.List[Quest]
    #: TNT Games quests.
    tnt_games: typing.List[Quest]
    #: Crazy Walls quests.
    crazy_walls: typing.List[Quest]
    #: UHC Champions quests.
    uhc: typing.List[Quest]
    #: VampireZ quests.
    vampirez: typing.List[Quest]
    #: Walls quests.
    walls: typing.List[Quest]
    #: Mega Walls quests.
    mega_wall: typing.List[Quest]
    #: Warlods quests.
    warlords: typing.List[Quest]
    #: Prototype Lobby games quests.
    prototype: typing.List[Quest]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`Quests` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`Quests` object.
        """
        quests = resp["quests"]
        return cls(
            last_updated_at=datetime.datetime.utcfromtimestamp(
                resp["lastUpdated"] / 1000
            ),
            arcade=[Quest.from_api_response(q) for q in quests["arcade"]],
            arena=[Quest.from_api_response(q) for q in quests["arena"]],
            bedwars=[Quest.from_api_response(q) for q in quests["bedwars"]],
            hungergames=[Quest.from_api_response(q) for q in quests["hungergames"]],
            build_battle=[Quest.from_api_response(q) for q in quests["buildbattle"]],
            cops_and_crims=[Quest.from_api_response(q) for q in quests["mcgo"]],
            duels=[Quest.from_api_response(q) for q in quests["duel"]],
            turbo_kart_racers=[
                Quest.from_api_response(q) for q in quests["gingerbread"]
            ],
            murder_mystery=[
                Quest.from_api_response(q) for q in quests["murdermystery"]
            ],
            paintball=[Quest.from_api_response(q) for q in quests["paintball"]],
            quake=[Quest.from_api_response(q) for q in quests["quake"]],
            skyblock=[Quest.from_api_response(q) for q in quests["skyblock"]],
            skyclash=[Quest.from_api_response(q) for q in quests["skyclash"]],
            skywars=[Quest.from_api_response(q) for q in quests["skywars"]],
            speed_uhc=[Quest.from_api_response(q) for q in quests["speeduhc"]],
            smash_heroes=[Quest.from_api_response(q) for q in quests["supersmash"]],
            tnt_games=[Quest.from_api_response(q) for q in quests["tntgames"]],
            crazy_walls=[Quest.from_api_response(q) for q in quests["truecombat"]],
            uhc=[Quest.from_api_response(q) for q in quests["uhc"]],
            vampirez=[Quest.from_api_response(q) for q in quests["vampirez"]],
            walls=[Quest.from_api_response(q) for q in quests["walls"]],
            mega_wall=[Quest.from_api_response(q) for q in quests["walls3"]],
            battleground=[Quest.from_api_response(q) for q in quests["battleground"]],
            prototype=[Quest.from_api_response(q) for q in quests["prototype"]],
        )
