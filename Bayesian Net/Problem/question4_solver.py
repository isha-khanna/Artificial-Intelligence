from string import ascii_lowercase
class Question4_Solver:
    def __init__(self, cpt):
        self.cpt = cpt;
        self.create_hidden1cpt();
        self.create_hidden2cpt();
    
    
    def create_hidden1cpt(self):
        self.hidden1cpt = [[0.0] * 27 for i in range(27)];
        for i in range(0,26):
            for j in range(0,26):
                self.hidden1cpt[i][j] = self.getHidden1Cp(i+96,j+96);
    
    def create_hidden2cpt(self):
        self.hidden2cpt = [[0.0] * 27 for i in range(27)];
        for i in range(0,26):
            for j in range(0,26):
                self.hidden2cpt[i][j] = self.getHidden2Cp(i+96,j+96);
    
        
    #####################################
    # ADD YOUR CODE HERE
    # Pr(x|y) = self.cpt.conditional_prob(x, y);
    # A word begins with "`" and ends with "`".
    # For example, the probability of word "ab":
    # Pr("ab") = \
    #    self.cpt.conditional_prob("a", "`") * \
    #    self.cpt.conditional_prob("b", "a") * \
    #    self.cpt.conditional_prob("`", "b");
    # query example:`
    #    query: "qu--_--n";
    #    return "t";
    def solve(self,query):
        words = list(query);
        wordList = []
        for word in words :
            wordList.append(list(word))    
        return self.solveSubProblem(wordList);
        
               
                    
    def solveSubProblem(self, words):
        bestProbability =0.0;
        bestCharcter ='a'
        for i in ascii_lowercase :
            currentProbability = 1;
            for word in words : 
                hiddenBefore = self.getNumOfHiddenBefore(word);
                hiddenAfter =  self.getNumOfHiddenAfter(word);
                word.append('`');
                word.insert(0,'`');
                predictPostion = word.index('_')
                if predictPostion-2 >=0 :
                    p1BeforeInt =  ord(word[predictPostion-2]) - 96
                else :
                    p1BeforeInt =0;
                if predictPostion+2 < len(word) :
                    p1AfterInt = ord(word[predictPostion+2]) - 96
                else :
                    p1AfterInt =0;
                if predictPostion-3 >=0:
                    p2BeforeInt =  ord(word[predictPostion-3]) - 96
                else :
                    p2BeforeInt =0;
                if predictPostion+3 < len(word): 
                    p2AfterInt = ord(word[predictPostion+3]) - 96
                else :
                    p2AfterInt =0;
                currentProbability *= self.getCurrentProbability(i,word,hiddenBefore,hiddenAfter,predictPostion,p1BeforeInt,p1AfterInt,p2BeforeInt,p2AfterInt)
            if currentProbability > bestProbability :
                bestProbability = currentProbability
                bestCharcter = i; 
        return bestCharcter;
    
    def getNumOfHiddenBefore(self, word):
        
        predictPostion = word.index('_')
        if predictPostion == 0 :
            return 0
        if(word[predictPostion -1] != '-'):
            return 0
        if predictPostion == 1 :
            return 1
        if(word[predictPostion -2] != '-'):
            return 1
        return 2
    
    def getNumOfHiddenAfter(self, word):
        
        predictPostion = word.index('_')
        if len(word) == predictPostion+1:
            return 0
        if(word[predictPostion +1] != '-'):
            return 0
        if len(word) == predictPostion+2:
            return 1
        if((word[predictPostion +2] != '-') ):
            return 1
        return 2
    
    def getCurrentProbability(self, a,word,hiddenBefore,hiddenAfter,predictPostion,p1BeforeInt,p1AfterInt,p2BeforeInt,p2AfterInt):
        npb =   self.cpt.conditional_prob
        aInt = ord(a)-96
        if hiddenBefore == 0 :
            if hiddenAfter == 0 : 
                return npb(a,word[predictPostion-1])* npb(word[predictPostion+1],a)
            elif hiddenAfter == 1 :
                return npb(a,word[predictPostion-1])* self.hidden1cpt[p1AfterInt][aInt]
            elif hiddenAfter == 2 :
                return npb(a,word[predictPostion-1])* self.hidden2cpt[p2AfterInt][aInt]
        elif hiddenBefore == 1 :
            if hiddenAfter == 0 : 
                return self.hidden1cpt[aInt][p1BeforeInt]* npb(word[predictPostion+1],a)
            elif hiddenAfter == 1 :
                return self.hidden1cpt[aInt][p1BeforeInt]* self.hidden1cpt[p1AfterInt][aInt]
            elif hiddenAfter == 2 :
                return self.hidden1cpt[aInt][p1BeforeInt]* self.hidden2cpt[p2AfterInt][aInt]
        elif hiddenBefore == 2 :
            if hiddenAfter == 0 : 
                return self.hidden2cpt[aInt][p2BeforeInt]* npb(word[predictPostion+1],a)
            elif hiddenAfter == 1 :
                return self.hidden2cpt[aInt][p2BeforeInt]* self.hidden1cpt[p1AfterInt][aInt]
            elif hiddenAfter == 2 :
                return self.hidden2cpt[aInt][p2BeforeInt]* self.hidden2cpt[p2AfterInt][aInt]
                
            
            
                
    def getHidden1Cp(self, a, b):
        sumProbability =0.0
        for i in range(1, 26):
            sumProbability += self.cpt.conditional_prob(chr(a),chr(i+96))*self.cpt.conditional_prob(chr(i+96),chr(b))
        return sumProbability;   
    
    def getHidden2Cp(self,a,b):
        sumProbability =0.0
        for i in range(1, 26):
            sumProbability += self.hidden1cpt[i][a-96]* self.cpt.conditional_prob(chr(b),chr(i+96))
        return sumProbability


    