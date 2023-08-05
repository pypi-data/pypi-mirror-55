import scipy.sparse as sp
import numpy as np
import math
from copy import deepcopy
from neurec.util import reader
import logging

class HoldOutDataSplitter(object):
    def __init__(self, path, dataset_name, data_format,separator,threshold,splitterRatio=[0.8,0.2]):
        self.path =path
        self.dataset_name = dataset_name
        self.separator = separator
        self.data_format = data_format
        self.splitterRatio = splitterRatio
        self.threshold = threshold
        self.logger = logging.getLogger("neurec.data.HoldOutDataSplitter.HoldOutDataSplitter")
        if float(splitterRatio[0])+ float(splitterRatio[1]) != 1.0:
            raise ValueError("please given a correct splitterRatio")
    def load_data_by_user_time(self):
        logging.info("Loading interaction records from %s "%(self.path))
        pos_per_user={}
        num_ratings=0
        num_items=0
        num_users=0
        #user/item {raw id, inner id} map
        userids = {}
        itemids = {}
        # inverse views of userIds, itemIds,
        idusers = {}
        iditems={}
        data = reader.lines(self.path + '/' + self.dataset_name)
        for line in data:
            if self.data_format == "UIRT":
                useridx, itemidx,rating,time= line.strip().split(self.separator)
                if float(rating) < self.threshold:
                    continue
            elif self.data_format == "UIT":
                useridx, itemidx,time= line.strip().split(self.separator)
                rating = 1
            elif self.data_format == "UIR":
                useridx, itemidx,rating = line.strip().split(self.separator)
                if float(rating) < self.threshold:
                    continue
            elif self.data_format == "UI":
                useridx, itemidx = line.strip().split(self.separator)
                rating = 1

            else:
                print("please choose a correct data format. ")

            num_ratings+=1
            if  itemidx not in itemids:
                iditems[num_items]=itemidx
                itemids[itemidx] = num_items
                num_items+=1

            if useridx not in userids:
                idusers[num_users]=useridx
                userids[useridx]=num_users
                num_users+=1
                pos_per_user[userids[useridx]]=[]
            if  self.data_format == "UIRT" or self.data_format == "UIT":
                pos_per_user[userids[useridx]].append((itemids[itemidx],rating,int(float(time))))

            else:
                pos_per_user[userids[useridx]].append((itemids[itemidx],rating,1))

        if  self.data_format == "UIRT" or self.data_format == "UIT":
            for u in range(num_users):
                pos_per_user[u]=sorted(pos_per_user[u], key=lambda d: d[2])
        self.logger.info("\"num_users\": %d,\"num_items\":%d, \"num_ratings\":%d"%(num_users,num_items,num_ratings))
        userseq = deepcopy(pos_per_user)
        train_dict = {}
        train_matrix = sp.dok_matrix((num_users, num_items), dtype=np.float32)
        test_matrix = sp.dok_matrix((num_users, num_items), dtype=np.float32)
        time_matrix = sp.dok_matrix((num_users, num_items), dtype=np.float32)
        for u in range(num_users):
            num_ratings_by_user = len(pos_per_user[u])
            num_test_ratings = math.floor(float(self.splitterRatio[1])*num_ratings_by_user)
            if len(pos_per_user[u]) >= 2 and num_test_ratings >=1:
                for _ in range(num_test_ratings):
                    test_item=pos_per_user[u][-1]
                    pos_per_user[u].pop()
                    test_matrix[u,test_item[0]] = test_item[1]
                    time_matrix[u,test_item[0]] = test_item[2]
            items = []
            for enlement in pos_per_user[u]:
                items.append(enlement[0])
                train_matrix[u,enlement[0]]=enlement[1]
                time_matrix[u,enlement[0]] = enlement[2]
            train_dict[u]=items
        return train_matrix,train_dict,test_matrix,userseq,userids,itemids,time_matrix
