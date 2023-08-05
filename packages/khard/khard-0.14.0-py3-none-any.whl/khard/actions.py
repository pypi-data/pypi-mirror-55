# -*- coding: utf-8 -*-


class Actions:

    """A class to manage the names and aliases of the command line
    subcommands."""

    action_map = {
        "add-email":    [],
        "addressbooks": ["abooks"],
        "birthdays":    ["bdays"],
        "copy":         ["cp"],
        "email":        [],
        "export":       [],
        "filename":     ["file"],
        "list":         ["ls"],
        "merge":        [],
        "edit":         ["modify", "ed"],
        "move":         ["mv"],
        "new":          ["add"],
        "phone":        [],
        "postaddress":  ["post", "postaddr"],
        "remove":       ["delete", "del", "rm"],
        "show":         ["details"],
        "source":       ["src"],
        "template":     [],
    }

    @classmethod
    def get_action(cls, alias):
        """Find the name of the action for the supplied alias.  If no action is
        asociated with the given alias, None is returned.

        :param alias: the alias to look up
        :type alias: str
        :rturns: the name of the corresponding action or None
        :rtype: str or NoneType

        """
        for action, alias_list in cls.action_map.items():
            if alias in alias_list:
                return action
        return None

    @classmethod
    def get_aliases(cls, action):
        """Find all aliases for the given action.  If there is no such action,
        None is returned.

        :param action: the action name to look up
        :type action: str
        :returns: the list of aliases corresponding to the action or None
        :rtype: list(str) or NoneType

        """
        return cls.action_map.get(action)

    @classmethod
    def get_actions(cls):
        """Find the names of all defined actions.

        :returns: all action names
        :rtype: iterable(str)
        """
        return cls.action_map.keys()

    @classmethod
    def get_all(cls):
        """Find the names of all defined actions and their aliases.

        :returns: the names of all actions and aliases
        :rtype: generator(str)

        """
        for key, value in cls.action_map.items():
            yield key
            yield from value
