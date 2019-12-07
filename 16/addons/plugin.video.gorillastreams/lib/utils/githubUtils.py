from github import Github
from hashlib import sha1
from cStringIO import StringIO
import datetime
import datetimeUtils   


class GitHubAPI:
    
    def __init__(self):
        self.__g = Github()
        self.__user = None
        self.__repo = None
        self.__branch = None
        self.__tree = None
        
    # max. 60 API calls per hour
    # ATM at least 15 * getEntries per hour
    
    ###########################################################################
    #            new  |  sameUser  |  sameRepo  |  sameBranch  |  sameTree    #
    #    A       1       -            -            -              -           #
    #    B       2       1            -            -              -           #
    #    C       3       2            1            -              -           #  
    #    D       4       3            2            1              -           # 
    ###########################################################################
    
    def getEntries(self, userName, repoName, branchName, folderName=None):
        try:
            if not self.__user or self.__user.login != userName:
                self.__user = self.__g.get_user(userName)                                                         # call A
                if self.__user:
                    self.__repo = self.__user.get_repo(repoName)                                                  # call B
                    if self.__repo:
                        self.__branch = self.__repo.get_branch(branchName)                                        # call C

            if self.__user:
                
                if not self.__repo or self.__repo.name != repoName:
                    self.__repo = self.__user.get_repo(repoName)                                                  # call B
                    if self.__repo:
                        self.__branch = self.__repo.get_branch(branchName)                                        # call C
                    
                if self.__repo:
                    
                    if not self.__branch or self.__branch.name != branchName:
                        self.__branch = self.__repo.get_branch(branchName)                                        # call C
                    
                    if self.__branch:
                        
                        recursive = True
                        commitSha = self.__branch.commit.sha
                        if not self.__tree or self.__tree.sha != commitSha:
                            self.__tree = self.__repo.get_git_tree(commitSha, recursive)                          # call D
                        
                        if self.__tree:
                            
                            entries = self.__tree.tree
                            if folderName:
                                entries = filter(lambda x : x.path.startswith(folderName), entries)
                            return entries
        except:
            pass
        
        return None



# returns UTC datetime
def getUpdatedAtFromString(dateStr):
    format = "%Y-%m-%d %H:%M:%S"
    result = datetimeUtils.strToDatetime(dateStr, format)
    return result + datetime.timedelta(hours=8) # PST -> UTC



# Hash

class githash(object):
    def __init__(self):
        self.buf = StringIO()

    def update(self, data):
        self.buf.write(data)

    def hexdigest(self):
        data = self.buf.getvalue()
        h = sha1()
        h.update("blob %u\0" % len(data))
        h.update(data)

        return h.hexdigest()

def githash_data(data):
    h = githash()
    h.update(data)
    return h.hexdigest()

def getGithash(filename):
    fileobj = file(filename)
    return githash_data(fileobj.read())

