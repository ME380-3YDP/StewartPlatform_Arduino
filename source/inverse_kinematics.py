from input_output import SeqHandler
import numpy as np
import tkinter
from tkinter.filedialog import askopenfilename
root = tkinter.Tk() #File open dialog
root.withdraw()

class inv_kinematics:
    def __init__(self):
        self.lengthSequence=[]
    
    def run(self):
        self.Vectors=Reader.run() #array of position vectors
        for idx,V in enumerate(self.Vectors):
            #read through each vector
            lengthVector=self.transform(V)
        self.lengthSequence.append()
        
    def transform(self):
       #compute inverse kinematics to create leg lengths, prpbably will be split into multiple functions.
        return lengths

def main(): #runs when we start the script
    try:
        sequence_file =askopenfilename(title = "Select sequence file",filetypes = (("Memes","*.csv"),("all files","*.*")))
    except:
        sequence_file = 0

    print(__doc__)
    Reader=SeqReader(sequence_file)

if __name__ == '__main__':
    main()