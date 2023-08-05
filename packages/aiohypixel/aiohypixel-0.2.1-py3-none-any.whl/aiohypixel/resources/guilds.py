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
Guild achievements and permissions models.
"""

__all__ = ("GuildAchievementTier", "TieredGuildAchievement", "GuildAchievements", "GuildPermission", "GuildPermissions")

import dataclasses
import datetime
import typing

from ..shared import HypixelModel, APIResponse


@dataclasses.dataclass(frozen=True)
class GuildAchievementTier(HypixelModel):
    """Represents a guild achievement tier on the Hypixel Network."""

    #: Tier position.
    tier: int
    #: Amount of times the achievement has to be completed for this tier to be completed.
    amount: int

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`GuildAchievementTier` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`GuildAchievementTier` object.
        """
        return cls(tier=resp["tier"], amount=resp["amount"])


@dataclasses.dataclass(frozen=True)
class TieredGuildAchievement(HypixelModel):
    """Represents a tiered guild achievement on the Hypixel Network."""

    #: Code name returned by the API.
    code_name: str
    #: Pretty name for this achievement.
    name: str
    #: Short description for the achievement.
    description: str
    #: List of tiers for this achievement.
    tiers: typing.List[GuildAchievementTier]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`TieredGuildAchievement` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`TieredGuildAchievement` object.
        """
        name = list(resp)[0]
        return cls(
            code_name=name,
            name=resp[name]["name"],
            description=resp[name]["description"],
            tiers=[GuildAchievementTier.from_api_response(t) for t in resp[name]["tiers"]],
        )


## The API returns an empty map for one-time guild achievements, so I don't know how they are structured.
## Until that changes, this will be commented out.
# @dataclasses.dataclass(frozen=True)
# class OneTimeGuildAchievement(HypixelModel):
#     """Represents a one-time guild achievement on the Hypixel Network."""

#     #: Code name returned by the API.
#     code_name: str
#     #: Pretty name for this achievement.
#     name: str
#     #: Short description for the achievement.
#     description: str
#     #: Amount of achievement points gotten from completing this achievement.
#     points: int

#     @classmethod
#     def from_api_response(cls, resp: APIResponse):
#         """
#         Processes the raw API response into a :class:`OneTimeGuildAchievement` object.

#         Args:
#             resp:
#                 The API response to process.

#         Returns:
#             The processed :class:`OneTimeGuildAchievement` object.
#         """

#         # I could maybe iterate through the dict since there's only one key ever,
#         # but idk if that would be clearer.
#         name = list(resp)[0]
#         return cls(
#             code_name=name,
#             name=resp[name]["name"],
#             description=resp[name]["description"],
#             points=resp[name]["points"],
#         )


@dataclasses.dataclass(frozen=True)
class GuildAchievements(HypixelModel):
    """Represents the guild achievements on the Hypixel Network."""

    #: Time this resource was last modified.
    last_updated_at: datetime.datetime
    #: Collection of one-time guild achievements.
    # one_time: typing.List[OneTimeGuildAchievement]
    one_time: typing.List
    #: Collection of tiered guild achievements.
    tiered: typing.List[TieredGuildAchievement]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`GuildAchievements` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`GuildAchievements` object.
        """
        return cls(
            last_updated_at=datetime.datetime.utcfromtimestamp(
                resp["lastUpdated"] / 1000
            ),
            one_time=resp["one_time"],
            # one_time=[
            #     OneTimeGuildAchievement.from_api_response(a) for a in resp["one_time"]
            # ],
            tiered=[
                TieredGuildAchievement.from_api_response(a) for a in resp["tiered"]
            ],
        )

@dataclasses.dataclass(frozen=True)
class GuildPermission(HypixelModel):
    """Represents a guild permission on the Hypixel Network."""

    #: Language code for this permission.
    language: str
    #: Permission name.
    name: str
    #: Short description for the permission.
    description: str
    #: Name of the item to use for the permission in the in-game UI.
    item: str

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`GuildPermission` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`GuildPermission` object.
        """
        lang = list(resp)[0]  # TODO: Fix up this behaviour
        return cls(
            language=lang,
            name=resp[lang]["name"],
            description=resp[lang]["description"],
            item=resp[lang]["item"]["name"],
        )


@dataclasses.dataclass(frozen=True)
class GuildPermissions(HypixelModel):
    """Represents the guild permissions on the Hypixel Network."""

    #: Time this resource was last modified.
    last_updated_at: datetime.datetime
    #: Collection of guild permissions.
    permissions: typing.List[GuildPermission]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`GuildPermissions` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`GuildPermissions` object.
        """
        return cls(
            last_updated_at=datetime.datetime.utcfromtimestamp(
                resp["lastUpdated"] / 1000
            ),
            permissions=[
                GuildPermission.from_api_response(p) for p in resp["permissions"]
            ],
        )
