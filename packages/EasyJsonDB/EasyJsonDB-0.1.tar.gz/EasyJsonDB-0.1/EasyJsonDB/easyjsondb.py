from json import loads as jsonLoad, dumps as jsonDump
from os.path import exists as fileExists
from base64 import b64encode, b64decode

class EasyJsonDBEntry:
    def __init__(self, queries, db):
        self.queries = queries
        self.db = db

    def __str__(self):
        return self.get()

    def get(self, key=None):
        result = self.db.search(queries=self.queries, limit=1, dictWay=True)
        return result[key] if key else result

    def set(self, key, content):
        self.queries = self.db.update(self.queries, updates={key: content}, limit=1)

        return self

    def remove(self):
        self.queries = self.db.remove(self.queries, limit=1)

        return self
    
    def update(self, updates=None, **updateKwargs):
        if not updates:
            updates = updateKwargs
        
        self.queries = self.db.update(self.queries, updates=updates, limit=1)

        return self

class EasyJsonDB:
    def __init__(self, filePath: str):
        self.__fileInit(filePath)

    def insert(self, insertion=None, **insertionKwargs):
        self.__reloadFile()

        num = self.__generateKey()

        if not insertion:
            insertion = insertionKwargs

        if 'id' in insertion:
            raise Exception("Cannot insert an id attribute")
        else:
            insertion['id'] = num

            self.db[num] = insertion

            self.__pushFile()

            return EasyDBEntry(self.db[num], self)

    def search(self, queries=None, limit=None, dictWay=False, **queriesKwargs):
        self.__reloadFile()

        if not queries:
            queries = queriesKwargs
        
        results = []

        for num in self.db:
            valid = True
            for query in queries:
                try:
                    if self.db[num][query] != queries[query]:
                        valid = False
                        break
                except:
                    valid = False
                    break
            
            if valid:
                if dictWay:
                    result = self.db[num]
                    result.pop('id')
                else:
                    result = EasyDBEntry(self.db[num], self)

                results.append(result)
            
                if limit and len(results) == limit:
                    break
        
        if len(results) == 0:
            return None
        else:
            return tuple(results) if len(results) > 1 else results[0]

    def exists(self, queries=None, **queriesKwargs):
        self.__reloadFile()

        if not queries:
            queries = queriesKwargs

        for num in self.db:
            valid = True
            for query in queries:
                try:
                    if self.db[num][query] != queries[query]:
                        valid = False
                        break
                except:
                    valid = False
                    break
            
            if valid:
                return True

        return False

    def update(self, queries, updates=None, limit=None, **updateKwargs):
        self.__reloadFile()

        if not queries:
            queries = queriesKwargs
        
        if not updates:
            updates = updateKwargs

        results = []

        for num in self.db:
            valid = True
            for query in queries:
                try:
                    if self.db[num][query] != queries[query]:
                        valid = False
                        break
                except:
                    valid = False
                    break
            
            if valid:
                for update in updates:
                    self.db[num][update] = updates[update]

                results.append(self.db[num])
            
                if limit and len(results) == limit:
                    break
        
        if len(results) > 0:
            self.__pushFile()

        if limit == 1:
            return results[0]

        return

    def remove(self, queries, limit=None, **queriesKwargs):
        self.__reloadFile()

        if not queries:
            queries = queriesKwargs

        results = []

        for num in self.db:
            valid = True
            for query in queries:
                try:
                    if self.db[num][query] != queries[query]:
                        valid = False
                        break
                except:
                    valid = False
                    break
            
            if valid:
                results.append(self.db[num])

                del self.db[num]
            
                if limit and len(results) == limit:
                    break
        
        if len(results) > 0:
            self.__pushFile()

        if limit == 1:
            return results[0]

        return

    def __idExists(self, num):
        return str(num) in self.db

    def __generateKey(self):
        maxNum = len(self.db) + int("10" + "0" * (int(len(str(len(self.db)))) - 1)) - len(self.db)

        for num in range(maxNum + 1):
            if not self.__idExists(num):
                return num
        
    def __reloadFile(self):
        try:
            with open(self.filePath, 'r') as file:
                self.file = self.__decode(file.read())
                self.db = self.file['data']
        except:
            self.__fileInit()

    def __pushFile(self):
        try:
            with open(self.filePath, 'w') as file:
                self.file['data'] = self.db
                file.write(self.__encode(self.file))
        except:
            self.__fileInit()

    def __encode(self, data):
        return b64encode(jsonDump(data).encode()).decode()

    def __decode(self, data):
        return jsonLoad(b64decode(data).decode())

    def __fileExists(self, filePath):
        self.filePath = filePath
        if fileExists(filePath):
            return True
        else:
            return False

    def __createFile(self):
        with open(self.filePath, 'w') as file:
            file.write(self.__encode({'data': {}}))

    def __checkFile(self):
        with open(self.filePath, 'r') as file:
            try:
                self.file = self.__decode(file.read())
            except:
                return False
            else:
                try:
                    self.db = self.file['data']
                except:
                    self.db = {}
                return True

    def __recoveryFile(self):
        with open(self.filePath, 'rb') as file:
            data = file.read()
        recoveryPath = "_Recovery.".join(self.filePath.split("."))
        with open(recoveryPath, 'wb') as file:
            file.write(data)
        self.__createFile()
 
    def __fileInit(self, filePath):
        if not self.__fileExists(filePath):
            self.__createFile()
        else:
            if not self.__checkFile():
                self.__recoveryFile()
            else:
                self.__reloadFile()
