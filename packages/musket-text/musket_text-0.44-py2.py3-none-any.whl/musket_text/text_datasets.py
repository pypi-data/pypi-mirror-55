import os
import re
import numpy as np
from musket_core import image_datasets,datasets,preprocessing,context
import pandas as pd

class BinaryTextClassificationDataSet(image_datasets.BinaryClassificationDataSet):
    
    def __init__(self,csvPath,textColumn,clazzColumn):
        super().__init__(None, csvPath, textColumn, clazzColumn)
    
    def _id(self,item):
        return item
    
    def _encode_x(self, item):
        return self[item.id].x    
        
    def get_value(self,t):
        return t
    
class CategoryTextClassificationDataSet(image_datasets.CategoryClassificationDataSet):
    
    def __init__(self,csvPath,textColumn,clazzColumn):
        super().__init__(None, csvPath, textColumn, clazzColumn)
    
    def _encode_x(self, item):
        return self[int(item.id)].x    
        
    def get_value(self,t):
        return t        

class MultiClassTextClassificationDataSet(image_datasets.MultiClassClassificationDataSet):
    
    def __init__(self,csvPath,textColumn,clazzColumn):
        super().__init__(None, csvPath, textColumn, clazzColumn)
    
    def _encode_x(self, item):
        return self[int(item.id)].x    
        
    def get_value(self,t):
        return t 
    
class Doc:
    
    def __init__(self):
        self.sentences=[]
        pass
    
    def __str__(self):
        return "\n".join([str(x) for x in self.sentences])
    
    def __repr__(self):
        return str(self)
    
class Sentence:
    
    def __init__(self):
        self.tokens=[]
        pass    
    
    
    
    def __repr__(self):
        return " ".join([str(x) for x in self.tokens])
    
class Token:
    
    def __init__(self,text,fields):
        self.text=text
        self.fields=fields
        pass
    
    def __repr__(self):
        return self.text    

import tqdm        

class SequenceLabelingColumnDataSet(datasets.DataSet):
    
    def __process(self, line: str) :
        sentence_completed = line.isspace()
        doc_completed=False
        fields=[]
        if self.document_separator_token:
            fields: List[str] = re.split("\s+", line)
            if len(fields) >= self.text_column:
                if fields[self.text_column] == self.document_separator_token:
                    sentence_completed = True
                    doc_completed=True
        return sentence_completed,doc_completed,fields

    def _encode_dataset(self,ds,encode_y=False,treshold=0.5):
        res=[]            
        for i in tqdm.tqdm(range(len(ds)),"Encoding dataset"):
            docId=None
            if not self.byDoc:
                docId=self.sentences[i].doc.num
            
            q=ds[i]    
            tags,tokens=self.encode(q,encode_y,treshold)
            if docId is not None:
                for v in range(len(tags)):
                    res.append({"doc_id":docId,"sentence_id":i,"token":tokens[v],"tag":tags[v]})
            else:    
                for v in range(len(tags)):
                    res.append({"sentence_id":i,"token":tokens[v],"tag":tags[v]})
                
        return self._create_dataframe(res)
    
    def _create_dataframe(self, items):
        if not self.byDoc:
            return pd.DataFrame(items,columns=["doc_id","sentence_id","token","tag"])
        return pd.DataFrame(items,columns=["sentence_id","token","tag"])
    
    def _encode_item(self, item:datasets.PredictionItem, encode_y=False, treshold=0.5):
        if encode_y:
            v=item.y
        else:
            v=item.prediction
        
        txt=self[int(item.id)].x
        res=self.decode(v,len(txt))
        
        return res,txt
                

    def build_classes(self, num2Class):
        self.num2Class = {}
        for c in num2Class:
            ww = sorted(list(num2Class[c]))
            rs = {}
            rs1 = {}
            num = 0
            for x in ww:
                val = np.zeros((len(ww) + 1), dtype=np.bool)
                val[num] = 1
                rs[x] = val
                rs1[num] = x
                num = num + 1
            
            rs2 = np.zeros((len(ww) + 1), dtype=np.bool)
            rs2[len(ww)] = 1
            self.num2Class[c] = rs, rs1, rs2


    def load_docs(self, path, encoding,  num2Class):
        fp = os.path.join(context.get_current_project_data_path(), path)
        csen=Sentence()
        cdoc=Doc()
        csen.doc=cdoc
        cdoc.num=0
        dnum=0
        with open(fp, encoding=encoding) as file:
            line = file.readline()
            while line:
                sc, dc, fields = self.__process(line)
                if len(fields) > 0 and len(fields[0]) > 0:
                    if not sc and not dc:
                        tc = Token(fields[0], fields[1:])
                        for x in range(len(tc.fields)):
                            vm = tc.fields[x]
                            if not x in num2Class:
                                num2Class[x] = set()
                            num2Class[x].add(vm)
                        
                        csen.tokens.append(tc)
                if sc:
                    if len(csen.tokens) > 0:
                        self.sentences.append(csen)
                        cdoc.sentences.append(csen)
                        csen = Sentence()
                        csen.doc=cdoc
                if dc:
                    if len(cdoc.sentences) > 0:
                        self.docs.append(cdoc)
                        dnum=dnum+1
                        cdoc = Doc()
                        cdoc.num=dnum
                line = file.readline()
        
        if len(csen.tokens) > 0:
            self.sentences.append(csen)
            cdoc.sentences.append(csen)
        if len(cdoc.sentences) > 0:
            self.docs.append(cdoc)

    def __init__(self,path,clazzColumn=2,encoding="utf8",byDoc=False):
        
        self.sentences=[]
        self.docs=[]
        self.clazzColumn=clazzColumn
        self.byDoc=byDoc
        self.text_column=0
        self.document_separator_token="-DOCSTART-"
        
        num2Class={}
        self.load_docs(path, encoding, num2Class)    
        
        self.build_classes(num2Class)        
                
    def __len__(self):
        if self.byDoc:
            return len(self.docs)
        return len(self.sentences)
    
    def __getitem__(self, item)->datasets.PredictionItem:
        tokenText=[]
        tokenClazz=[]
        
        if self.byDoc:
            d=self.docs[item]
            for sent in d.sentences:
                tokenText=tokenText+[x.text for x in sent.tokens]
                tokenClazz=tokenClazz+[self.num2Class[self.clazzColumn][0][x.fields[self.clazzColumn]] for x in sent.tokens]            
        else:
            sent=self.sentences[item]
            tokenText=tokenText+[x.text for x in sent.tokens]
            tokenClazz=tokenClazz+[self.num2Class[self.clazzColumn][0][x.fields[self.clazzColumn]] for x in sent.tokens]
            
        return datasets.PredictionItem(item,np.array(tokenText),np.array(tokenClazz))
    
    
    def decode(self,vals,vm=None):
            vs=self.num2Class[self.clazzColumn]
            rs=np.argmax(vals,axis=1)
            
            res=[]
            if vm is not None:
                for i in range(vm):
                    q=rs[i]
                    if q in vs[1]:
                        res.append(vs[1][q])
                    else:
                        res.append("O")
                        
                return res
            for q in rs:
                if q in vs[1]:
                    res.append(vs[1][q])
                else:
                    break    
            return res
        
            
    def _encode_sentence(self,s:Sentence):    
        pass                

       