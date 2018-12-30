'''
Created on Oct 31, 2011

@author: ajju
'''
class Action(object):
    
    def __init__(self, action_id):
        self.__action_id = action_id
        self.__next_action_map = {}
        self.__redirect_action_map = {}
        self.__moves = []

    def get_redirect_action_map(self):
        return self.__redirect_action_map


    def addRedirectAction(self, action_name, action_id):
        self.__redirect_action_map[action_name] = action_id


    def set_redirect_action_map(self, value):
        self.__redirect_action_map = value


    def del_redirect_action_map(self):
        del self.__redirect_action_map


    def set_next_action_map(self, value):
        self.__next_action_map = value
        
    
    def get_next_action_map(self):
        return self.__next_action_map


    def addNextAction(self, action_name, action_id):
        self.__next_action_map[action_name] = action_id


    def del_next_action_map(self):
        del self.__next_action_map


    def get_action_id(self):
        return self.__action_id


    def get_moves(self):
        return self.__moves


    def set_action_id(self, value):
        self.__action_id = value


    def set_moves(self, value):
        self.__moves = value


    def del_action_id(self):
        del self.__action_id


    def del_moves(self):
        del self.__moves

    
    def addMove(self, move):
        self.__moves.append(move)
        
    action_id = property(get_action_id, set_action_id, del_action_id, "action_id's docstring")
    moves = property(get_moves, set_moves, del_moves, "moves's docstring")
    next_action_map = property(get_next_action_map, set_next_action_map, del_next_action_map, "next_action_map's docstring")
    redirect_action_map = property(get_redirect_action_map, set_redirect_action_map, del_redirect_action_map, "redirect_action_map's docstring")
    
    
class Move(object):
    
    def __init__(self, modulePath, functionName, pmessage):
        self.__module_path = modulePath
        self.__function_name = functionName
        self.__pmessage = pmessage

    def get_pmessage(self):
        return self.__pmessage


    def set_pmessage(self, value):
        self.__pmessage = value


    def del_pmessage(self):
        del self.__pmessage


    def get_module_path(self):
        return self.__module_path


    def get_function_name(self):
        return self.__function_name


    def set_module_path(self, value):
        self.__module_path = value


    def set_function_name(self, value):
        self.__function_name = value


    def del_module_path(self):
        del self.__module_path


    def del_function_name(self):
        del self.__function_name

    module_path = property(get_module_path, set_module_path, del_module_path, "module_path's docstring")
    function_name = property(get_function_name, set_function_name, del_function_name, "function_name's docstring")
    pmessage = property(get_pmessage, set_pmessage, del_pmessage, "pmessage's docstring")
    
    
class Service(object):
    
    def __init__(self, name, action_id):
        self.__service_name = name
        self.__action_id = action_id

    def get_service_name(self):
        return self.__service_name


    def get_action_id(self):
        return self.__action_id


    def set_service_name(self, value):
        self.__service_name = value


    def set_action_id(self, value):
        self.__action_id = value


    def del_service_name(self):
        del self.__service_name


    def del_action_id(self):
        del self.__action_id

    service_name = property(get_service_name, set_service_name, del_service_name, "service_name's docstring")
    action_id = property(get_action_id, set_action_id, del_action_id, "action_id's docstring")
    
    
