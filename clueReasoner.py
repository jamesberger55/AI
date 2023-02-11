'''ClueReasoner.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant

Copyright (C) 2019 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import SATSolver

# Initialize important variables
caseFile = "cf"
players = ["sc", "mu", "wh", "gr", "pe", "pl"]
extendedPlayers = players + [caseFile]
suspects = ["mu", "pl", "gr", "pe", "sc", "wh"]
weapons = ["kn", "ca", "re", "ro", "pi", "wr"]
rooms = ["ha", "lo", "di", "ki", "ba", "co", "bi", "li", "st"]
cards = suspects + weapons + rooms

def getPairNumFromNames(player,card):
    return getPairNumFromPositions(extendedPlayers.index(player),
                                   cards.index(card))

def getPairNumFromPositions(player,card):
    return player*len(cards) + card + 1

# TO BE IMPLEMENTED AS AN EXERCISE
def initialClauses():
    clauses = []

    # Each card is in at least one place (including case file).
    for c in cards:
        clauses.append([getPairNumFromNames(p,c) for p in extendedPlayers])

    # A card cannot be in two places.
    for person1 in extendedPlayers:
        for person2 in extendedPlayers:
            if person1 != person2:
                for c in cards:
                    clauses.append([-1 * getPairNumFromNames(person1, c), -1 * getPairNumFromNames(person2, c)])


    # At least one card of each category is in the case file.
    for category in [suspects, weapons, rooms]:
        clause = [getPairNumFromNames(caseFile, c) for c in category]
        clauses.append(clause)

    # No two cards in each category can both be in the case file.
    for category in [suspects, weapons, rooms]:
        for i in range(len(category)):
            for j in range(i + 1, len(category)):
                clauses.append([-1 * getPairNumFromNames(caseFile, category[i]), -1 * getPairNumFromNames(caseFile, category[j])])

# TO BE IMPLEMENTED AS AN EXERCISE  
def hand(player, player_cards):
    clauses = []
    for c in player_cards:
        clauses.append(getPairNumFromNames(player, c))
    return clauses

# TO BE IMPLEMENTED AS AN EXERCISE  
def suggest(suggester,card1,card2,card3,refuter,cardShown):
    suggesterIndex = players.index(suggester)
    clauses = []
    for i in range(len(players)):
        playerIndex = (suggesterIndex + i) % len(players)
        player = players[playerIndex]
        if player == refuter:
            # Add clause for refuter
            clauses.append([-getPairNumFromNames(caseFile, card) for card in [card1, card2, card3]] + [getPairNumFromNames(caseFile, cardShown)])
            break
        elif player != suggester:
            # Add clause for players who couldn't refute the suggestion
            clauses.append([-getPairNumFromNames(caseFile, card) for card in [card1, card2, card3]])
    # Add clause for players who don't have any of the suggested cards
    if refuter is None:
        for player in players:
            if player != suggester:
                clauses.append([-getPairNumFromNames(caseFile, card) for card in [card1, card2, card3]])
    return clauses




# TO BE IMPLEMENTED AS AN EXERCISE  
def accuse(accuser,card1,card2,card3,isCorrect):
    """
    This function makes an accusation of the murderer, weapon and location.
    If the accusation is incorrect, the player loses the game.
    """
    clauses = []
    if isCorrect:
        clauses.append([getPairNumFromNames(accuser, card1)])
        clauses.append([getPairNumFromNames(accuser, card2)])
        clauses.append([getPairNumFromNames(accuser, card3)])
    else:
        clauses.append([-getPairNumFromNames(accuser, card1)])
        clauses.append([-getPairNumFromNames(accuser, card2)])
        clauses.append([-getPairNumFromNames(accuser, card3)])
    return clauses


def query(player,card,clauses):
    return SATSolver.testLiteral(getPairNumFromNames(player,card),clauses)

def queryString(returnCode):
    if returnCode == True:
        return 'Y'
    elif returnCode == False:
        return 'N'
    else:
        return '-'

def printNotepad(clauses):
    for player in players:
        print('\t', player, end=' ')
    print('\t', caseFile)
    for card in cards:
        print(card,'\t', end=' ')
        for player in players:
            print(queryString(query(player,card,clauses)),'\t', end=' ')
        print(queryString(query(caseFile,card,clauses)))

def playClue():
    clauses = initialClauses()
    clauses.extend(hand("sc",["wh", "li", "st"]))
    clauses.extend(suggest("sc", "sc", "ro", "lo", "mu", "sc"))
    clauses.extend(suggest("mu", "pe", "pi", "di", "pe", None))
    clauses.extend(suggest("wh", "mu", "re", "ba", "pe", None))
    clauses.extend(suggest("gr", "wh", "kn", "ba", "pl", None))
    clauses.extend(suggest("pe", "gr", "ca", "di", "wh", None))
    clauses.extend(suggest("pl", "wh", "wr", "st", "sc", "wh"))
    clauses.extend(suggest("sc", "pl", "ro", "co", "mu", "pl"))
    clauses.extend(suggest("mu", "pe", "ro", "ba", "wh", None))
    clauses.extend(suggest("wh", "mu", "ca", "st", "gr", None))
    clauses.extend(suggest("gr", "pe", "kn", "di", "pe", None))
    clauses.extend(suggest("pe", "mu", "pi", "di", "pl", None))
    clauses.extend(suggest("pl", "gr", "kn", "co", "wh", None))
    clauses.extend(suggest("sc", "pe", "kn", "lo", "mu", "lo"))
    clauses.extend(suggest("mu", "pe", "kn", "di", "wh", None))
    clauses.extend(suggest("wh", "pe", "wr", "ha", "gr", None))
    clauses.extend(suggest("gr", "wh", "pi", "co", "pl", None))
    clauses.extend(suggest("pe", "sc", "pi", "ha", "mu", None))
    clauses.extend(suggest("pl", "pe", "pi", "ba", None, None))
    clauses.extend(suggest("sc", "wh", "pi", "ha", "pe", "ha"))
    clauses.extend(suggest("wh", "pe", "pi", "ha", "pe", None))
    clauses.extend(suggest("pe", "pe", "pi", "ha", None, None))
    clauses.extend(suggest("sc", "gr", "pi", "st", "wh", "gr"))
    clauses.extend(suggest("mu", "pe", "pi", "ba", "pl", None))
    clauses.extend(suggest("wh", "pe", "pi", "st", "sc", "st"))
    clauses.extend(suggest("gr", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(suggest("pe", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(suggest("pl", "pe", "pi", "ki", "gr", None))
    print('Before accusation: should show a single solution.')
    printNotepad(clauses)
    print()
    clauses.extend(accuse("sc", "pe", "pi", "bi", True))
    print('After accusation: if consistent, output should remain unchanged.')
    printNotepad(clauses)

if __name__ == '__main__':
    playClue()
