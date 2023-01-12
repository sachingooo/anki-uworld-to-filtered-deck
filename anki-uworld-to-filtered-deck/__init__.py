# UWorld Question IDs to Filtered Decks
#
# Copyright (C) 2022  Sachin Govind
# This is not my idea. There are existing addons that perform similar functionality - this addon is my implementation of that idea.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip
from aqt import mw

from anki.collection import DYN_DUE, SearchNode
from anki.tags import TagTreeNode

from typing import Iterable

import re

config = mw.addonManager.getConfig(__name__)
uworldTags = {}


def updateUworldTags():
    # if we already gathered them, we're done
    if len(uworldTags) > 0:
        return

    col = collection()
    tagTree = col.tags.tree()
    leafNodes = []

    def findLeafNodes(nodes: Iterable[TagTreeNode], baseName):
        for node in nodes:
            if node.children and len(node.children) > 0:
                findLeafNodes(node.children, baseName + "::" +
                              node.name if len(baseName) > 0 else node.name)
            else:
                leafNodes.append((node, baseName + "::" + node.name))

    findLeafNodes(tagTree.children, "")

    for nodePair in leafNodes:
        tagName = nodePair[1]
        if "::#UWorld::" in tagName:
            # parse qid
            qid = tagName.split("::")[-1]
            if not qid.isnumeric():
                continue
            qid = int(qid)
            uworldTags[str(qid)] = tagName


def collection():
    collection = mw.col
    if collection is None:
        raise Exception('collection is not available')

    return collection


def _createFilteredDeckForUWorldQuestion(qid, fullTagName, parentDeckPath):
    if not fullTagName or len(fullTagName) < 2:
        return

    col = collection()
    search = col.build_search_string(SearchNode(tag=fullTagName))
    deckName = "UWorld #%s" % qid
    if len(parentDeckPath) > 0:
        deckName = parentDeckPath + "::" + deckName
    numberCards = 300

    # modifications based on config
    if config:
        if config["supplementalSearchText"]:
            search += " " + config["supplementalSearchText"]
        if config["numCards"] > 0:
            numberCards = config["numCards"]

    did = col.decks.new_filtered(deckName)
    deck = col.decks.get(did)

    deck["terms"] = [[search, numberCards, DYN_DUE]]
    col.decks.save(deck)
    col.sched.rebuildDyn(did)


def _addUWorldFilteredDecks():
    qids, ok = QInputDialog.getText(
        mw, "UWorld Questions", "Enter a comma-separated list of UWorld question IDs: ")

    # canceled
    if not ok:
        return

    parsedQids = re.split('\W+', qids)
    if len(parsedQids) == 0:
        return

    parsedQids = [qid for qid in parsedQids if len(
        qid) > 0 and qid.isnumeric()]

    # build the UWorld tags array if it hasn't already been done
    updateUworldTags()

    missedQids = []
    for qid in parsedQids:
        if str(qid) not in uworldTags:
            missedQids.append(str(qid))
            continue
        tag = uworldTags[qid]
        if not tag:
            missedQids.append(str(qid))
            continue

        _createFilteredDeckForUWorldQuestion(qid, tag, "UWorld")

    mw.reset()
    if len(missedQids) > 0:
        tooltip("No UWorld Tags for %s" % ",".join(missedQids), 10000)
    else:
        tooltip("Created filtered decks for all UWorld questions")


def _addUWorldFilteredDecksToTools():
    # Add our functions to the tools menu
    action = QAction("UWorld Filtered Decks", mw)
    qconnect(action.triggered, _addUWorldFilteredDecks)
    mw.form.menuTools.addAction(action)


_addUWorldFilteredDecksToTools()
