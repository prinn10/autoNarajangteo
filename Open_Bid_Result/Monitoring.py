class monitoring(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__ is called\n")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__ is called\n")
            cls._init = True

            self.keys = ['bid_ann', 'bid_res', 'pre_pri', 'lis_cra', 'tot_cou']
            self.moni_dic = {}
            for key in self.keys:
                self.moni_dic[key] = {'processing_time': 0, 'count': 0}

    def update(self, keys, processing_times, print_type='none'):
        # 1. element update
        if type(keys) is list: # 리스트
            for key,processing_time in zip(keys, processing_times):
                self.moni_dic[key]['processing_time'] += processing_time
                self.moni_dic[key]['count'] += 1
        else: # 스칼라
            self.moni_dic[keys]['processing_time'] += processing_times
            self.moni_dic[keys]['count'] += 1

        # 2. element print
        # 2.1 print_type is none :
        if print_type == 'none':
            pass
        elif print_type == 'updated_element':
            print(keys, 'Average Processing Time : ', self.moni_dic[keys]['processing_time']/self.moni_dic[keys]['count'], 'Count :', self.moni_dic[keys]['count'])
        elif print_type == 'all_element':
            for key in self.keys:
                print(key, 'Average Processing Time : ', self.moni_dic[key]['processing_time']/self.moni_dic[key]['count'], 'Count :', self.moni_dic[key]['count'])
        else:
            print('not exist print type')

if __name__ == '__main__':
    pass

