import tkinter
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import requests
from bs4 import BeautifulSoup as Soup
from pygame import mixer
'''
pip install pygame bs4 requests tkinter
'''


'''
todo:

mostrar nome do professor
usar enter
alarme padrao

poder selecionar varias trmas



'''

class App():
            
    def __init__(self,master):
        self.master = master
        master.title("Atualizador de Matérias")
        self.createLabels()
        self.createEntries()
        self.createBtns()
        self.createText()
        self.createBox()
        
        self.aux=1

    def createLabels(self):
        self.labelDep=tkinter.Label(self.master, text="Departamento da matéria")
        self.labelDep.grid(columnspan=2,row=0, column=0)
        self.labelMat=tkinter.Label(self.master, text="Número da matéria")
        self.labelMat.grid(columnspan=2,row=1, column=0)
        self.labelTipo=tkinter.Label(self.master, text="Tipo da turma")
        self.labelTipo.grid(columnspan=2,row=2, column=0)
        self.labelTurma=tkinter.Label(self.master, text="Número da turma")
        self.labelTurma.grid(columnspan=2,row=4, column=0)
        self.labelMusica=tkinter.Label(self.master, text="Música para despertar")
        self.labelMusica.grid(columnspan=2,row=5, column=0)
        self.labelSitu=tkinter.Label(self.master, text="Situação das turmas")
        self.labelSitu.grid(columnspan=2,row=0, column=5)

    def createEntries(self):
        dep=tkinter.StringVar()
        dep.set("ABC")
        #self.entryDep=tkinter.Entry(self.master, width=19,textvariable=dep)
        #self.entryDep.grid(columnspan=2,row=0, column=2)
        mat=tkinter.StringVar()
        mat.set("123")
        #self.entryMat=tkinter.Entry(self.master, width=19,textvariable=mat)
        #self.entryMat.grid(columnspan=2,row=1, column=2)
        #self.entryTurma=tkinter.Entry(self.master, width=19)
        #self.entryTurma.grid(columnspan=2,row=4, column=2)
        self.entryMusica=tkinter.Entry(self.master, width=14)
        self.entryMusica.grid(columnspan=1,row=5, column=2)

    def createBtns(self):
        self.btnIr=tkinter.Button(self.master,text="Procurar", command=self.botaoIr)
        self.btnIr.grid(row=6, column=1)
        self.btnCancelar=tkinter.Button(self.master,text="Cancelar",command=self.botaoCancelar)
        self.btnCancelar.grid(row=6, column=2)
        self.btnMusica=tkinter.Button(self.master, text="Abrir",width=3, command=self.botaoMusica)
        self.btnMusica.grid(row=5,column=3)
        self.v = tkinter.StringVar()
        self.v.set("T")
        self.v.trace('w',self.atualizarTurma)
        self.radioB1=tkinter.Radiobutton(self.master, text="T", variable=self.v, value="T", state="disable")
        self.radioB1.grid(row=2,column=2)
        self.radioB2=tkinter.Radiobutton(self.master, text="P", variable=self.v, value="P", state="disable")
        self.radioB2.grid(row=2,column=3)
        
        
    def createText(self):
        self.textSitu=tkinter.Text(self.master, height=10, width=25)
        self.textSitu.grid(row=1,column=5, rowspan=6,columnspan=3)
        self.scroll=tkinter.Scrollbar(self.master,command=self.textSitu.yview)
        self.scroll.grid(row=1, column=8,sticky='nsew',rowspan=6)
        self.textSitu['yscrollcommand'] = self.scroll.set
        self.textSitu.insert(tkinter.END,"Feito em Fevereiro 2019\npor João Anastácio ELT16")

    def createBox(self):
        self.dep1=tkinter.StringVar()
        self.listDep=ttk.Combobox(self.master,state="readonly",textvariable=self.dep1)
        self.listDep.grid(columnspan=2,row=0, column=2)
        self.iniciar()
        self.dep1.trace('w',self.atualizarMat)
        self.mat=tkinter.StringVar()
        self.listMat=ttk.Combobox(self.master,state="readonly",textvariable=self.mat)
        self.listMat.grid(columnspan=2,row=1, column=2)
        self.mat.trace('w',self.atualizarTurma)
        self.turma1=tkinter.StringVar()
        self.listTurma=ttk.Combobox(self.master,state="readonly",textvariable=self.turma1)
        self.listTurma.grid(columnspan=2,row=4, column=2)

    def atualizarMat(self,*args):
        self.radioB1.configure(state="disable")
        self.radioB2.configure(state="disable")
        self.listMat.set("")
        url='http://www.dti.ufv.br/horario/horario.asp?ano=2020&semestre=1&depto=%s'%self.dep1.get()[1:]
        r=self.myRequest(url,"deu ruim")
        soup=Soup(r.text,"html.parser")
        r.close()
        listMat=set()
        for tr in soup.find_all("tr"):
            td=tr.find_all("td")
            if len(td)>0and len(td[0].text)<8:
                listMat.add(td[0].text)
        listMat=list(listMat)
        listMat.sort()
        self.listMat['values'] = listMat

    def atualizarTurma(self,*args):
        self.radioB1.configure(state="normal")
        self.radioB2.configure(state="normal")
        self.listTurma.set("")
        url='http://www.dti.ufv.br/horario/horario.asp?ano=2019&semestre=2&depto=%s'%self.dep1.get()[1:]
        r=self.myRequest(url,"deu ruim")
        soup=Soup(r.text,"html.parser")
        r.close()
        listTurma=set()
        listTurma.add("")
        mate=self.dep1.get()[1:]+" "+self.mat.get()[-3:]
        for tr in soup.find_all("tr"):
            td=tr.find_all("td")
            if len(td)==0:
                continue
            if td[0].text==mate and td[2].text==self.v.get().upper() :
                listTurma.add(td[3].text)
        listTurma=list(listTurma)
        listTurma.sort()
        self.listTurma['values'] = listTurma
        
    def botaoCancelar(self):
        try:
            mixer.music.pause()
        except:
            pass
        finally:
            
            self.btnIr.configure(state="normal")
            self.aux=0
        
        
    def iniciar(self):
        url="http://www.dti.ufv.br/horario/hor.asp?ano=2019&semestre=2"
        r=self.myRequest(url,"deu ruim")
        soup=Soup(r.text,"html.parser")
        r.close()
        k=soup.find_all("table")
        k2=k[2].find_all("td")
        listDep=[]
        for it in k2:
            listDep.append(it.text)
        self.listDep['values'] = listDep
   

    def botaoIr(self):
        self.aux=1
        self.textSitu.delete(1.0,tkinter.END)
        self.dep=self.dep1.get()[1:]
        self.num=self.mat.get()[-3:]
        turma=self.turma1.get()
        if len(turma)==0:
            self.turma=0
        else:
            self.turma=int(turma)
        
        self.tipo=self.v.get()
        self.som=self.entryMusica.get()
        if(len(self.dep)==0 or len(self.num)==0 or len(self.tipo)==0 or len(self.som)==0):
            self.textSitu.insert(tkinter.END,"valor invalido")
            return
        self.btnIr.configure(state="disable")
        
        self.atualizador(self.dep,self.num,self.tipo,self.turma,self.som)
        
    def botaoMusica(self):
        file=askopenfilename()
        self.entryMusica.delete(0,tkinter.END)
        self.entryMusica.insert(0,file)

    def sound(self,nome):
        mixer.init()
        mixer.music.load(nome)
        mixer.music.play()

    def myRequest(self,url,erro):
   
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}
        while True:
                try:
                    r=requests.get(url,headers=headers)
                except Exception:
                    print("\a\n\n\n\n",erro,"\n\n\n\n\a")
                    erros+=1
                else:
                    break
                
        return r

    def argumentos(self):
        self.atualizador(self.dep,self.num,self.tipo,self.turma,self.som)
    
    def atualizador(self,dep,num,tipo,turma,som):

        if(self.aux==0):
            self.aux=1
            return
        materia=dep.upper()+" "+num
        url='http://www.dti.ufv.br/horario/horario.asp?ano=2019&semestre=2&depto=%s'%dep
        
        

        
        self.textSitu.delete(1.0,tkinter.END)
        r=self.myRequest(url,"deu ruim")
        soup=Soup(r.text,"html.parser")
        r.close()
        self.textSitu.insert(tkinter.END,materia)
        if (turma==0):
            for tr in soup.find_all("tr"):
                if self.aux==0:
                    pass
                td=tr.find_all("td")
                if len(td)>0:
                    if td[0].text==materia and td[2].text==tipo.upper():
                        
                        self.textSitu.insert(tkinter.END,"\nNa turma %d tem %d vagas"%(int(td[3].text),int(td[8].text[0:2])))
                        if (int(td[8].text[0:2])>0):
                            self.aux=0
                            self.sound(som)
                            self.textSitu.insert(tkinter.END,"\nAchou")
                            return
                            
                        
        else:
            for tr in soup.find_all("tr"):
                if self.aux==0:
                    pass
                td=tr.find_all("td")
                if len(td)>0:
                    if td[0].text==materia and td[2].text==tipo.upper():
                        print("Looking...")
                        self.textSitu.insert(tkinter.END,"\nNa turma %d tem %d vagas"%(int(td[3].text),int(td[8].text[0:2])))
                        if (int(td[3].text)==turma and int(td[8].text[0:2])>0):
                            self.aux=0
                            self.sound(som)
                            self.textSitu.insert(tkinter.END,"\nAchou")
                            return
                            
                        
        self.master.after(100, self.argumentos)

        


root=tkinter.Tk()
app=App(root)
#root.iconbitmap('download.jpg')
root.mainloop()
