# -*- coding: utf-8 -*-

"""Main module."""

import re
from datetime import datetime, timedelta
from itertools import chain
from os.path import expanduser
from typing import List, Union

from orgparse import load, loads
from orgparse.node import OrgNode, OrgRootNode
from starlette.config import Config

from .datastructures import ListTagGroup

config = Config(expanduser("~") + "/.org_todo_metrics.conf")
settings = {
    "WORK_TASK_CONTAINS_DEFAULT": config("WORK_TASK_CONTAINS", default="IN PROGRESS")
}


def debug_settings():
    for k, v in settings.items():
        print(f"{k}: {v}")


class WorkTask(object):
    """
    """

    def __init__(self, work_task_string: str):
        """
        :param work_task_string: the string representing the state transition of a work task
                                 example:
                                 '- State "IN PROGRESS" from "TODO"    [2019-10-26 Sat 21:01]'
        """
        self.work_task_string = work_task_string

    @property
    def timestamp(self) -> datetime:
        """
        `work_task_string`\`s timestamp represented as a python datetime object
        uses https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        """
        time_stamp_string = string_between("[", "]", self.work_task_string)
        return datetime.strptime(time_stamp_string, "%Y-%m-%d %a %H:%M")

    @property
    def from_state(self):
        """
        """
        m = re.search('from\ "(.+)"', self.work_task_string)
        return m.group(1)

    @property
    def begin_state(self):
        m = re.search('State\ "(.+)"\ +from', self.work_task_string)
        return m.group(1)


class WorkTaskPair(object):
    """
    """

    def __init__(self, first: WorkTask, second: WorkTask):
        self.first = first
        self.second = second

    @property
    def delta(self):
        return self.first.timestamp - self.second.timestamp


def average_time_spent_working(
    org_file: str, tags: Union[List[List[str]], None] = None, is_file: bool = False
):
    """
    returns the average time spent working on all tasks, filtered by tags given the path to an org file
    AKA mean time to completion

    :param org_file: path to the org file in question
    :param tags: tags to filter the average timespent working on
    :returns: average time spent working on all tasks AKA mean_time_to_completion, in seconds
    """
    # use load if file, use loads if string
    load_function = [loads, load][is_file]
    org_tree = load_function(org_file)
    closed_todos = all_closed_todos(org_tree=org_tree, tags=tags)
    return get_mean_time_to_completion(closed_todos)


def flatten(mylist: list):
    return list(chain.from_iterable(mylist))


def get_mean_time_to_completion(todos: List[OrgNode]):
    """

    """
    work_tasks = [get_work_tasks(todo) for todo in todos]
    work_task_pairs = flatten(
        [to_work_task_pair(work_task) for work_task in work_tasks]
    )
    delta_list = [work_task_pair.delta for work_task_pair in work_task_pairs]
    mean_time_to_completion = sum(delta_list, timedelta()) / len(delta_list)
    return mean_time_to_completion.total_seconds()


def to_work_task_pair(work_tasks: List[WorkTask]) -> List[WorkTaskPair]:
    if len(work_tasks) % 2 != 0:
        raise Exception("work task clusters must come in pairs")
    # https://stackoverflow.com/a/2990281
    return [
        create_work_task_pair(i, i + 1, work_tasks)
        for i in range(0, len(work_tasks), 2)
    ]


def create_work_task_pair(
    index_first: int, index_second: int, work_tasks: List[WorkTask]
) -> WorkTaskPair:
    return WorkTaskPair(first=work_tasks[index_first], second=work_tasks[index_second])


def get_work_tasks(
    org_node: OrgNode, contains: str = settings["WORK_TASK_CONTAINS_DEFAULT"]
) -> List[WorkTask]:
    """
    a work task only wants task whose state transition contains `contains`.  a state transition is defined by the
    function `state_transition_filter`.

    :param org_node: the org node to get work tasks from
    :param contains: defines string is contained in work tasks
    :returns: a list of work tasks from a todo org node

    Example Usage:

        >>> todos = all_closed_todos(org_tree, tags)
        >>> work_tasks = [get_work_tasks(todo) for todo in todos]
    """
    return [
        WorkTask(work_task_string=task)
        for task in state_transition_filter(org_node._lines)
        if contains in task
    ]


def state_transition_filter(org_node_lines: List[str]):
    return [line for line in org_node_lines if re.search("-\ State", line)]


def all_org_nodes(org_tree: OrgRootNode) -> List[OrgNode]:
    """given a loaded org file, return all of its nodes excluding the useless root node

        :param org_tree: the 'loaded' org file
        :returns: list of all nodes

        Example Usage:

        >>> org_tree = loads(org_file_string)
        >>> node_list = all_org_nodes(org_tree)
    """
    return [node for node in org_tree[1:]]  # [1:] for skipping root itself


def string_between(first: str, second: str, string: str):
    """
    https://stackoverflow.com/a/16835195
    """
    return string[string.find(first) + 1 : string.find(second)]


def all_closed_todos(
    org_node_list: List[OrgNode] = None,
    org_tree: OrgRootNode = None,
    tags: Union[ListTagGroup, None] = None,
) -> List[OrgNode]:
    """
    returns all org nodes with closed todos for a either a list of OrgNodes or an OrgRootNode. one of either
    `org_node_list` or `org_tree` must be specified.

    :param org_node_list: either this or `org_tree` must be set.
    :param org_tree: either this or `org_node_list` must be set.
    :param tags: NOT IMPLEMENTED a list of tag groups to filter `org_node_list` or `org_tree` closed todo `OrgNode`\s
                 by
    :returns: all closed `OrgNode`\s matching tags

    Example Usage:
        >>> org_tree = loads(org_file_string)
        >>> closed_todo_nodes = all_closed_todos(org_tree=org_tree)
    """
    if org_node_list is None and org_tree is None:
        raise Exception(
            "function all_closed_todos requires either org_node_list or org_tree to be set"
        )
    if org_tree:
        return [
            node for node in all_org_nodes(org_tree) if node.closed.start is not None
        ]
    if org_node_list:
        return [node for node in org_node_list if node.closed.start is not None]
    raise Exception("should never happen")
