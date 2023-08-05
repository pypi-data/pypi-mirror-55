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
Skyblock resources models.
"""

__all__ = (
    "SkyblockCollectionItemTier",
    "SkyblockCollectionItem",
    "SkyblockCollection",
    "SkyblockCollections",
    "SkyblockSkillLevel",
    "SkyblockSkill",
    "SkyblockSkills",
)

import dataclasses
import datetime
import typing

from ..shared import HypixelModel, APIResponse


@dataclasses.dataclass(frozen=True)
class SkyblockCollectionItemTier(HypixelModel):
    """Represents a Skyblock collection item tier on the Hypixel Network."""

    #: Tier position.
    tier: int
    #: Amount of the item required for the tier to be completed.
    amount_required: int
    #: Collection of items that are unlocked once the tier is completed.
    unlocks: typing.List[str]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`SkyblockCollectionItemTier` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`SkyblockCollectionItemTier` object.
        """
        return cls(
            tier=resp["tier"],
            amount_required=resp["amountRequired"],
            unlocks=resp["unlocks"],
        )


@dataclasses.dataclass(frozen=True)
class SkyblockCollectionItem(HypixelModel):
    """Represents a Skyblock collection item on the Hypixel Network."""

    #: API code name.
    code_name: str
    #: Pretty item name.
    name: str
    #: Total number of tiers available.
    max_tiers: int
    #: List of tiers for the item.
    tiers: typing.List[SkyblockCollectionItemTier]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`SkyblockCollectionItem` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`SkyblockCollectionItem` object.
        """
        name = list(resp)[0]
        return cls(
            code_name=name,
            name=resp[name]["name"],
            max_tiers=resp[name]["maxTiers"],
            tiers=[
                SkyblockCollectionItemTier.from_api_response(i)
                for i in resp[name]["tiers"]
            ],
        )


@dataclasses.dataclass(frozen=True)
class SkyblockCollection(HypixelModel):
    """Represents a Skyblock collection on the Hypixel Network."""

    #: API code name.
    code_name: str
    #: Pretty name.
    name: str
    #: List of items that belong to this collection.
    items: typing.List[SkyblockCollectionItem]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`SkyblockCollection` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`SkyblockCollection` object.
        """
        name = list(resp)[0]
        return cls(
            code_name=name,
            name=resp[name]["name"],
            items=[
                SkyblockCollectionItem.from_api_response(i) for i in resp[name]["items"]
            ],
        )


@dataclasses.dataclass(frozen=True)
class SkyblockCollections(HypixelModel):
    """Represents the collections for a Skyblock version on the Hypixel Network."""

    #: Time this resource was last modified.
    last_updated_at: datetime.datetime
    #: Skyblock version this resource corresponds to.
    version: str
    #: List of collections.
    collections: typing.List[SkyblockCollection]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`SkyblockCollections` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`SkyblockCollections` object.
        """
        return cls(
            last_updated_at=datetime.datetime.utcfromtimestamp(
                resp["lastUpdated"] / 1000
            ),
            version=resp["version"],
            collections=[
                SkyblockCollection.from_api_response(c) for c in resp["collections"]
            ],
        )


@dataclasses.dataclass(frozen=True)
class SkyblockSkillLevel(HypixelModel):
    """Represents a Skyblock skill level on the Hypixel Network."""

    #: Level position.
    level: int
    #: Amount of the item required for the level to be completed.
    amount_required: int
    #: Collection of items that are unlocked once the level is completed.
    unlocks: typing.List[str]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`SkyblockSkillLevel` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`SkyblockSkillLevel` object.
        """
        return cls(
            level=resp["level"],
            amount_required=resp["amountRequired"],
            unlocks=resp["unlocks"],
        )


@dataclasses.dataclass(frozen=True)
class SkyblockSkill(HypixelModel):
    """Represents a Skyblock skill on the Hypixel Network."""

    #: API code name.
    code_name: str
    #: Pretty skill name.
    name: str
    #: Total number of levels available.
    max_levels: int
    #: List of levels for the skill.
    levels: typing.List[SkyblockSkillLevel]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`SkyblockSkill` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`SkyblockSkill` object.
        """
        name = list(resp)[0]
        return cls(
            code_name=name,
            name=resp[name]["name"],
            max_levels=resp[name]["maxLevels"],
            levels=[
                SkyblockSkillLevel.from_api_response(i) for i in resp[name]["levels"]
            ],
        )


@dataclasses.dataclass(frozen=True)
class SkyblockSkills(HypixelModel):
    """Represents the skills for a Skyblock version on the Hypixel Network."""

    #: Time this resource was last modified.
    last_updated_at: datetime.datetime
    #: Skyblock version this resource corresponds to.
    version: str
    #: List of skills.
    skills: typing.List[SkyblockSkill]

    @classmethod
    def from_api_response(cls, resp: APIResponse):
        """
        Processes the raw API response into a :class:`SkyblockSkills` object.

        Args:
            resp:
                The API response to process.

        Returns:
            The processed :class:`SkyblockSkills` object.
        """
        return cls(
            last_updated_at=datetime.datetime.utcfromtimestamp(
                resp["lastUpdated"] / 1000
            ),
            version=resp["version"],
            collections=[
                SkyblockSkills.from_api_response(c) for c in resp["collections"]
            ],
        )
