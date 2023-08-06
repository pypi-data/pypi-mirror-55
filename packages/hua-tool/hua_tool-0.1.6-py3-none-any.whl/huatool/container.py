import huatool as HT

from pymongo import MongoClient

class EndOfBatchException(Exception):
    def __init__(self):
        super().__init__()

class MongoBatch(object):
    '''把 MongoDB 当成 Batch。'''
    def __init__(self, url, database, train_collection, test_collection):
        self.connection = MongoClient(url)
        self.database = self.connection.get_database(database)
        self.trainCollection = self.database.get_collection(train_collection)
        self.testCollection = self.database.get_collection(test_collection)

    def dataRandomBatches(self, test=False, batch_size=32, times=150000):
        '''随机抽取匹样本'''
        collection = self.trainCollection if not test else self.testCollection
        for t in range(times):
            data_batch = []
            label_batch = []
            for d in collection.aggregate([
                {
                    '$sample': {
                        'size': batch_size
                    }
                }
            ]):
                data_batch.append(d['data'])
                label_batch.append(d['label'])
            yield (HT.Numpy.asarray(data_batch, dtype=float), HT.Numpy.asarray(label_batch))

    def dataBatches(self, test=False, batch_size=32):
        '''依序抽取匹样本'''
        collection = self.trainCollection if not test else self.testCollection
        data_batch = []
        label_batch = []
        for d in collection.find():
            data_batch.append(d['data'])
            label_batch.append(d['label'])
            if len(data_batch) >= batch_size:
                yield (HT.Numpy.asarray(data_batch, dtype=float), HT.Numpy.asarray(label_batch))
                data_batch.clear()
                label_batch.clear()
        if len(data_batch) > 0:
            yield (HT.Numpy.array(data_batch), HT.Numpy.array(label_batch))

    def datas(self, test=False):
        '''一个一个抽取样本'''
        collection = self.trainCollection if not test else self.testCollection
        for d in collection.find():
            yield d['data'], d['label']

    def data(self, _id=0, test=False):
        '''抽取一个样本'''
        collection = self.trainCollection if not test else self.testCollection
        f = collection.find_one({
            '_id': _id
        })
        return f['data'], f['label']

    def dataRange(self, _id_start=0, _id_end=0, test=False):
        '''抽取范围内样本'''
        collection = self.trainCollection if not test else self.testCollection
        for d in collection.find({
            '_id': {
                '$gte': _id_start,
                '$lte': _id_end
            }
        }):
            yield d['data'], d['label']

    def clearDatas(self, test=False):
        '''清空集合。'''
        collection = self.trainCollection if not test else self.testCollection
        collection.drop()

    def insertDatas(self, datas, test=False, batch_size=64):
        '''新增数据。'''
        collection = self.trainCollection if not test else self.testCollection
        print(collection)
        def pre_insert_iters():
            for i, d in enumerate(datas):
                d = {
                    '_id': i,
                    'data': d[0],
                    'label': d[1]
                }
                yield d
        batches = []
        for d in pre_insert_iters():
            batches.append(d)
            if len(batches) >= batch_size:
                collection.insert_many(batches)
                batches.clear()
        if len(batches) > 0:
            collection.insert_many(batches)
            
    def close(self):
        '''关闭连接'''
        self.connection.close()

class Batch(object):
    '''数据 Batch 处理'''
    def __init__(self, datas, batch_size, d0=True):
        self.datas = list(datas)
        self.batchSize = batch_size
        self.d0 = d0
        self.index = 0
        if self.d0:
            self.datas = tuple(map(lambda x: HT.Numpy.array(x), self.datas))

    def reset(self):
        '''刷新 Batch'''
        self.index = 0

    @property
    def shape(self):
        '''数据形状'''
        return self.datas.shape
    
    @property
    def size(self):
        '''数据长度'''
        return len(self.datas[0]) if self.d0 else len(self.datas)

    @property
    def hasNext(self):
        '''是否还有下一批数据'''
        return self.index < self.size

    def getNext(self, random=False):
        '''获取下一批数据'''
        indexes = [i for i in range(self.index, self.index + self.batchSize) if i < self.size]
        if random:
            indexes = [i for i in range(self.size)]
            HT.Random.shuffle(indexes)
            indexes = indexes[0:self.batchSize if self.batchSize <= self.size else self.size]
        self.index += self.batchSize
        if indexes:
            if self.d0:
                return tuple(map(lambda x: x[indexes], self.datas))
            else:
                return self.datas[indexes]
        else:
            raise EndOfBatchException()