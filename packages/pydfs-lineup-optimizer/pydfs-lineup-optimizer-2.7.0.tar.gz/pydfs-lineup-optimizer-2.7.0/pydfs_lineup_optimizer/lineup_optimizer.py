from __future__ import division
from collections import OrderedDict
from itertools import chain
from math import ceil
from typing import FrozenSet, Type, Generator, Tuple, Union, Optional, List, Dict, Set, cast
from pydfs_lineup_optimizer.lineup import Lineup
from pydfs_lineup_optimizer.solvers import Solver, PuLPSolver, SolverException
from pydfs_lineup_optimizer.exceptions import LineupOptimizerException, LineupOptimizerIncorrectTeamName, \
    LineupOptimizerIncorrectPositionName
from pydfs_lineup_optimizer.sites import SitesRegistry
from pydfs_lineup_optimizer.lineup_importer import CSVImporter
from pydfs_lineup_optimizer.settings import BaseSettings, LineupPosition
from pydfs_lineup_optimizer.player import Player, LineupPlayer, GameInfo
from pydfs_lineup_optimizer.utils import ratio, link_players_with_positions, process_percents, get_remaining_positions
from pydfs_lineup_optimizer.rules import *


BASE_RULES = {TotalPlayersRule, LineupBudgetRule, PositionsRule, MaxFromOneTeamRule, LockedPlayersRule,
              RemoveInjuredRule, UniquePlayerRule, UniqueLineupRule, TotalTeamsRule}


class LineupOptimizer(object):
    def __init__(self, settings, solver=PuLPSolver):
        # type: (Type[BaseSettings], Type[Solver]) -> None
        self._settings = settings()
        self._csv_importer = None  # type: Optional[Type[CSVImporter]]
        self._rules = BASE_RULES.copy()  # type: Set[Type[OptimizerRule]]
        self._players = []  # type: List[Player]
        self._lineup = []  # type: List[Player]
        self._available_positions = frozenset(chain.from_iterable(
            position.positions for position in self._settings.positions))
        self._removed_players = []  # type: List[Player]
        self._search_threshold = 0.8
        self._min_deviation = 0.06
        self._max_deviation = 0.12
        self._players_from_one_team = {}  # type: Dict[str, int]
        self._players_with_same_position = {}  # type: Dict[str, int]
        self._positions_stacks_from_same_team = None  # type: Optional[Tuple[List[Tuple[str, ...]], ...]]
        self._min_salary_cap = None  # type: Optional[float]
        self._max_repeating_players = None  # type: Optional[int]
        self._solver_class = solver
        self._max_projected_ownership = None  # type: Optional[float]
        self._min_projected_ownership = None  # type: Optional[float]
        self._team_stacks = None  # type: Optional[List[int]]
        self._opposing_teams_position_restriction = None  # type: Optional[Tuple[List[str], List[str]]]
        self.spacing_positions = None  # type: Optional[List[str]]
        self.spacing = None  # type: Optional[int]
        self.teams_exposures = None  # type: Optional[Dict[str, float]]
        self.team_stacks_for_positions = None  # type: Optional[List[str]]
        self.same_team_restrict_positions = None  # type: Optional[Tuple[Tuple[str, str], ...]]
        self.opposing_team_force_positions = None  # type: Optional[Tuple[Tuple[str, str], ...]]
        self.total_teams = None  # type: Optional[int]

    @property
    def budget(self):
        # type: () -> float
        return self._settings.budget

    @property
    def total_players(self):
        # type: () -> int
        return self._settings.get_total_players()

    @property
    def remaining_budget(self):
        # type: () -> float
        return self.budget - sum(player.salary for player in self.locked_players)

    @property
    def remaining_players(self):
        # type: () -> int
        return self.total_players - len(self.locked_players)

    @property
    def max_from_one_team(self):
        # type: () -> Optional[int]
        return self._settings.max_from_one_team

    @property
    def positions_stacks_from_same_team(self):
        # type: () -> Optional[Tuple[List[Tuple[str, ...]], ...]]
        return self._positions_stacks_from_same_team

    @property
    def players_from_one_team(self):
        # type: () -> Dict[str, int]
        return self._players_from_one_team

    @property
    def players_with_same_position(self):
        # type: () -> Dict[str, int]
        return self._players_with_same_position

    @property
    def available_teams(self):
        # type: () -> FrozenSet[str]
        return frozenset([p.team for p in self._players])

    @property
    def available_positions(self):
        # type: () -> FrozenSet[str]
        return self._available_positions

    @property
    def removed_players(self):
        # type: () -> List[Player]
        return self._removed_players

    @property
    def players(self):
        # type: () -> List[Player]
        return [player for player in self._players if player not in self.removed_players]

    @property
    def locked_players(self):
        # type: () -> List[Player]
        return self._lineup

    @property
    def min_salary_cap(self):
        # type: () -> Optional[float]
        return self._min_salary_cap

    @property
    def max_repeating_players(self):
        # type: () -> Optional[int]
        return self._max_repeating_players

    @property
    def max_projected_ownership(self):
        # type: () -> Optional[float]
        return self._max_projected_ownership

    @property
    def min_projected_ownership(self):
        # type: () -> Optional[float]
        return self._min_projected_ownership

    @property
    def settings(self):
        # type: () -> BaseSettings
        return self._settings

    @property
    def team_stacks(self):
        # type: () -> Optional[List[int]]
        return self._team_stacks

    @property
    def opposing_teams_position_restriction(self):
        # type: () -> Optional[Tuple[List[str], List[str]]]
        return self._opposing_teams_position_restriction

    @property
    def games(self):
        # type: () -> FrozenSet[GameInfo]
        return frozenset(player.game_info for player in self.players if player.game_info)

    def reset_lineup(self):
        self._lineup = []
        self._players_with_same_position = {}
        self._players_from_one_team = {}
        self._positions_stacks_from_same_team = None

    def set_deviation(self, min_deviation, max_deviation):
        # type: (float, float) -> None
        """
        Set deviation ranges for randomness mode
        """
        self._min_deviation = min_deviation
        self._max_deviation = max_deviation

    def set_csv_importer(self, csv_importer):
        # type: (Type[CSVImporter]) -> None
        self._csv_importer = csv_importer

    def get_deviation(self):
        # type: () -> Tuple[float, float]
        return self._min_deviation, self._max_deviation

    def set_min_salary_cap(self, min_salary):
        # type: (float) -> None
        if min_salary > self.budget:
            raise LineupOptimizerException('Min salary greater than max budget')
        self.add_new_rule(MinSalaryCapRule)
        self._min_salary_cap = min_salary

    def load_players_from_csv(self, filename):
        # type: (str) -> None
        """
        Load player list from CSV file with passed filename.
        """
        csv_importer = self._csv_importer
        if not csv_importer:
            csv_importer = SitesRegistry.get_csv_importer(self._settings.site)
        self._players = csv_importer(filename).import_players()

    def load_lineups_from_csv(self, filename):
        # type: (str) -> List[Lineup]
        csv_importer = self._csv_importer
        if not csv_importer:
            csv_importer = SitesRegistry.get_csv_importer(self._settings.site)
        return csv_importer(filename).import_lineups(self.players)

    def load_players(self, players):
        # type: (List[Player]) -> None
        """
        Manually loads player to optimizer
        """
        self._players = players

    def extend_players(self, players):
        # type: (List[Player]) -> None
        """
        Add more players for current optimizer players
        """
        self._players.extend(players)

    def add_new_rule(self, rule):
        # type: (Type[OptimizerRule]) -> None
        self._rules.add(rule)

    def remove_rule(self, rule, silent=True):
        # type: (Type[OptimizerRule], bool) -> None
        try:
            self._rules.remove(rule)
        except KeyError:
            if not silent:
                raise LineupOptimizerException('Rule isn\'t added!')

    def remove_player(self, player):
        # type: (Player) -> None
        """
        Remove player from list for selecting players for lineup.
        """
        self._removed_players.append(player)

    def restore_player(self, player):
        # type: (Player) -> None
        """
        Restore removed player.
        """
        try:
            self._removed_players.remove(player)
        except ValueError:
            raise LineupOptimizerException('Player not removed!')

    def find_players(self, name):
        # type: (str) -> List[Player]
        """
        Return list of players with similar name.
        """
        possibilities = [(player, ratio(name, player.full_name)) for player in self._players]
        filtered_possibilities = filter(lambda pos: pos[1] >= self._search_threshold, possibilities)
        players = sorted(filtered_possibilities, key=lambda pos: -pos[1])
        return list(map(lambda p: p[0], players))

    def get_player_by_name(self, name):
        # type: (str) -> Optional[Player]
        """
        Return closest player with similar name or None.
        """
        players = self.find_players(name)
        return players[0] if players else None

    def get_player_by_id(self, player_id):
        # type: (str) -> Optional[Player]
        for player in self._players:
            if player.id == player_id:
                return player
        return None

    def add_player_to_lineup(self, player):
        # type: (Player) -> None
        """
        Forces adding specified player to lineup.
        Return true if player successfully added to lineup.
        """
        if player.max_exposure == 0:
            raise LineupOptimizerException('Can\'t add this player to line up! Player has max exposure set to 0.')
        if player in self._lineup:
            raise LineupOptimizerException('This player already in your line up!')
        if player.salary > self.remaining_budget:
            raise LineupOptimizerException('Can\'t add this player to line up! Your team is over budget!')
        if self.remaining_players < 1:
            raise LineupOptimizerException('Can\'t add this player to line up! You already select all %s players!' %
                                           len(self.locked_players))
        if self.max_from_one_team:
            from_same_team = len([p for p in self.locked_players if p.team == player.team])
            if from_same_team + 1 > self.max_from_one_team:
                raise LineupOptimizerException('You can\'t set more than %s players from one team.' %
                                               self.max_from_one_team)
        try:
            link_players_with_positions(self.locked_players + [player], self._settings.positions)
        except LineupOptimizerException:
            raise LineupOptimizerException('You\'re already select all %s\'s' % '/'.join(player.positions))
        self._lineup.append(player)

    def remove_player_from_lineup(self, player):
        # type: (Player) -> None
        """
        Removes specified player from lineup.
        """
        try:
            self._lineup.remove(player)
        except ValueError:
            raise LineupOptimizerException('Player not in line up!')

    def set_players_from_one_team(self, teams=None):
        # type: (Optional[Dict[str, int]]) -> None
        if teams is not None:
            teams = {team.upper(): num_of_players for team, num_of_players in teams.items()}
            for team, num_of_players in teams.items():
                self._check_team_constraint(team, num_of_players)
            self.add_new_rule(TeamMatesRule)
        else:
            self.remove_rule(TeamMatesRule)
        self._players_from_one_team = teams or {}

    def set_players_with_same_position(self, positions):
        # type: (Dict[str, int]) -> None
        positions = positions or {}
        positions = {position.upper(): num_of_players for position, num_of_players in positions.items()}
        for pos, val in positions.items():
            self._check_position_constraint(pos)
        self._players_with_same_position = positions

    def set_positions_for_same_team(self, *positions_stacks):
        # type: (*List[Union[str, Tuple[str, ...]]]) -> None
        if positions_stacks and positions_stacks[0] is not None:
            formatted_positions_stacks = tuple(
                [cast(Tuple[str, ...], (position, ) if isinstance(position, str) else tuple(position))
                 for position in stack] for stack in positions_stacks
            )
            for stack in formatted_positions_stacks:
                if not all(stack):
                    raise LineupOptimizerException('Positions stack can\'t be empty')
            total_players = self.settings.get_total_players()
            if sum([len(stack) for stack in formatted_positions_stacks]) > total_players:
                raise LineupOptimizerException('You can\'t set more than %d players' % total_players)
            if self.max_from_one_team and \
                    any(len(stack) > self.max_from_one_team for stack in formatted_positions_stacks):
                raise LineupOptimizerException('You can\'t set more than %s players from one team.' %
                                               self.max_from_one_team)
            for position in set(chain.from_iterable(chain.from_iterable(formatted_positions_stacks))):
                self._check_position_constraint(position)
            self.add_new_rule(FromSameTeamByPositionsRule)
            self._positions_stacks_from_same_team = formatted_positions_stacks
        else:
            self.remove_rule(FromSameTeamByPositionsRule)
            self._positions_stacks_from_same_team = None

    def set_max_repeating_players(self, max_repeating_players):
        # type: (int) -> None
        if max_repeating_players >= self.total_players:
            raise LineupOptimizerException('Maximum repeating players should be smaller than %d' % self.total_players)
        elif max_repeating_players < 1:
            raise LineupOptimizerException('Maximum repeating players should be 1 or greater')
        self._max_repeating_players = max_repeating_players
        self.add_new_rule(MaxRepeatingPlayersRule)

    def set_projected_ownership(self, min_projected_ownership=None, max_projected_ownership=None):
        # type: (Optional[float], Optional[float]) -> None
        if min_projected_ownership and max_projected_ownership and min_projected_ownership >= max_projected_ownership:
            raise LineupOptimizerException('Max projected ownership should be greater than min projected ownership')
        self._max_projected_ownership = max_projected_ownership / 100 if \
            max_projected_ownership and max_projected_ownership > 1 else max_projected_ownership
        self._min_projected_ownership = min_projected_ownership / 100 if \
            min_projected_ownership and min_projected_ownership > 1 else min_projected_ownership
        if max_projected_ownership or min_projected_ownership:
            self.add_new_rule(ProjectedOwnershipRule)
        else:
            self.remove_rule(ProjectedOwnershipRule)

    def set_team_stacking(self, stacks, for_positions=None):
        # type: (Optional[List[int]], Optional[List[str]]) -> None
        if stacks:
            if sum(stacks) > self.settings.get_total_players():
                raise LineupOptimizerException('Sum of stacks should be less than %d' % self.total_players)
            max_from_one_team = self.settings.max_from_one_team
            if max_from_one_team and any([stack > max_from_one_team for stack in stacks]):
                raise LineupOptimizerException(
                    'Stacks should be smaller than max players from one team (%d)' %
                    self.settings.max_from_one_team)   # type: ignore
            self.add_new_rule(TeamStacksRule)
        else:
            self.remove_rule(TeamStacksRule)
        self._team_stacks = stacks
        self.team_stacks_for_positions = for_positions

    def restrict_positions_for_opposing_team(self, first_team_positions, second_team_positions):
        # type: (List[str], List[str]) -> None
        if not self.games:
            raise LineupOptimizerException('Game Info isn\'t specified for players')
        self._opposing_teams_position_restriction = (first_team_positions, second_team_positions)
        self.add_new_rule(RestrictPositionsForOpposingTeam)

    def restrict_positions_for_same_team(self, *restrict_positions):
        # type: (*Tuple[str, str]) -> None
        if not all(len(positions) == 2 for positions in restrict_positions):
            raise LineupOptimizerException('Exactly 2 positions must be specified in restrict positions')
        for position in set(chain.from_iterable(restrict_positions)):
            self._check_position_constraint(position)
        self.same_team_restrict_positions = restrict_positions
        self.add_new_rule(RestrictPositionsForSameTeamRule)

    def force_positions_for_opposing_team(self, *force_positions):
        # type: (*Tuple[str, str]) -> None
        if not all(len(positions) == 2 for positions in force_positions):
            raise LineupOptimizerException('Exactly 2 positions must be specified in force positions')
        for position in set(chain.from_iterable(force_positions)):
            self._check_position_constraint(position)
        self.opposing_team_force_positions = force_positions
        self.add_new_rule(ForcePositionsForOpposingTeamRule)

    def set_spacing_for_positions(self, positions, spacing):
        # type: (List[str], int) -> None
        if spacing < 1:
            raise LineupOptimizerException('Spacing must be 1 or greater')
        available_positions = self.available_positions
        if any(position not in available_positions for position in positions):
            raise LineupOptimizerException('Incorrect positions. Choices are: %s' % available_positions)
        self.spacing_positions = positions
        self.spacing = spacing
        self.add_new_rule(RosterSpacingRule)

    def set_teams_max_exposure(self, teams_exposures):
        # type: (Dict[str, float]) -> None
        processed_exposures = {}  # type: Dict[str, float]
        for team, raw_exposure in teams_exposures.items():
            if team not in self.available_teams:
                raise LineupOptimizerException('Incorrect team: %s' % team)
            if raw_exposure is not None:
                exposure = process_percents(raw_exposure)
                processed_exposures[team] = cast(float, exposure)
        self.teams_exposures = processed_exposures

    def set_total_teams(self, total_teams):
        # type: (int) -> None
        min_teams = self.settings.min_teams
        max_from_one_team = self.settings.max_from_one_team
        total_players = self.settings.get_total_players()
        if not min_teams and max_from_one_team:
            min_teams = ceil(total_players / max_from_one_team)
        if min_teams and total_teams < min_teams:
            raise LineupOptimizerException('Minimum number of teams is %d' % min_teams)
        if total_teams > total_players:
            raise LineupOptimizerException('Maximum number of teams is %d' % total_players)
        self.total_teams = total_teams

    def optimize(self, n, max_exposure=None, randomness=False, with_injured=False):
        # type: (int, Optional[float], bool, bool) -> Generator[Lineup, None, None]
        params = locals().copy()
        rules = self._rules.copy()
        rules.update(self.settings.extra_rules)
        if randomness:
            rules.add(RandomObjective)
        else:
            rules.add(NormalObjective)
        if with_injured:
            rules.remove(RemoveInjuredRule)
        players = [player for player in self.players if player.max_exposure is None or player.max_exposure > 0]
        base_solver = self._solver_class()
        base_solver.setup_solver()
        players_dict = OrderedDict(
            [(player, base_solver.add_variable('Player_%d' % i)) for i, player in enumerate(players)])
        variables_dict = {v: k for k, v in players_dict.items()}
        constraints = [constraint(self, params) for constraint in rules]
        for constraint in constraints:
            constraint.apply(base_solver, players_dict)
        previous_lineup = None
        for _ in range(n):
            solver = base_solver.copy()  # type: Solver
            for constraint in constraints:
                constraint.apply_for_iteration(solver, players_dict, previous_lineup)
            try:
                solved_variables = solver.solve()
                lineup_players = []
                for solved_variable in solved_variables:
                    player = variables_dict.get(solved_variable)
                    if player:
                        lineup_players.append(player)
                lineup = self._build_lineup(lineup_players)
                previous_lineup = lineup
                yield lineup
                if len(self.locked_players) == self.total_players:
                    return
            except SolverException:
                raise LineupOptimizerException('Can\'t generate lineups')

    def optimize_lineups(self, lineups):
        params = {
            'n': len(lineups),
            'lineups': lineups,
        }
        rules = self._rules.copy()
        rules.update(self.settings.extra_rules)
        rules.add(NormalObjective)
        rules.add(LateSwapRule)
        rules.remove(PositionsRule)
        players = [player for player in self.players if player.max_exposure is None or player.max_exposure > 0]
        base_solver = self._solver_class()
        base_solver.setup_solver()
        players_dict = OrderedDict(
            [(player, base_solver.add_variable('Player_%d' % i)) for i, player in enumerate(players)])
        variables_dict = {v: k for k, v in players_dict.items()}
        constraints = [constraint(self, params) for constraint in rules]
        for constraint in constraints:
            constraint.apply(base_solver, players_dict)
        previous_lineup = None
        for lineup in lineups:
            solver = base_solver.copy()  # type: Solver
            for constraint in constraints:
                constraint.apply_for_iteration(solver, players_dict, previous_lineup)
            try:
                solved_variables = solver.solve()
                unswappable_players = lineup.get_unswappable_players()
                lineup_players = []
                for solved_variable in solved_variables:
                    player = variables_dict.get(solved_variable)
                    if player:
                        lineup_players.append(player)
                generated_lineup = self._build_lineup(lineup_players, unswappable_players)
                previous_lineup = generated_lineup
                yield generated_lineup
                if len(self.locked_players) == self.total_players:
                    return
            except SolverException:
                raise LineupOptimizerException('Can\'t generate lineups')

    def _build_lineup(self, players, unswappable_players=None):
        # type: (List[Player], Optional[List[LineupPlayer]]) -> Lineup
        lineup = []
        positions = self._settings.positions[:]
        if unswappable_players:
            players = [player for player in players if player not in unswappable_players]
            positions = get_remaining_positions(positions, unswappable_players)
            lineup.extend(unswappable_players)
        players_with_positions = link_players_with_positions(players, positions)
        for player, position in players_with_positions.items():
            lineup.append(LineupPlayer(player, position.name))
        positions_order = [pos.name for pos in self._settings.positions]
        lineup.sort(key=lambda p: positions_order.index(p.lineup_position))
        return Lineup(lineup, self._settings.lineup_printer)

    def _check_team_constraint(self, team, num_of_players):
        # type: (str, int) -> None
        if team not in self.available_teams:
            raise LineupOptimizerIncorrectTeamName('%s is incorrect team name.' % team)
        if self.max_from_one_team and num_of_players > self.max_from_one_team:
            raise LineupOptimizerException('You can\'t set more than %s players from one team.' %
                                           self.max_from_one_team)

    def _check_position_constraint(self, position):
        # type: (str) -> None
        if position not in self.available_positions:
            raise LineupOptimizerIncorrectPositionName('%s is incorrect position name.' % position)
