#%%
import hashlib

#%%
def hash(string):
    """
        Generate hash from string

        Args: 
            - string
        Return:
            - hash
    """
    return hashlib.md5(string.encode('utf-8')).hexdigest()

#%%
def hd(row_list):
    """
        Generate hash diff from list

        Args: 
            - row_list : list
        Return:
            - hash
    """
    string = ""
    for i in range(2, len(row_list)):
        string = string + str(row_list[i])

    return hash(string)

#%%
def hk(row_list, index_list):
    """
        Generate hash key from list

        Args: 
            - row_list : list
            - index_list : index for row_list that to be hashed
        Return:
            - hash
    """
    string = ""
    for index in index_list:
        string = string + str(row_list[index])

    return hash(string)