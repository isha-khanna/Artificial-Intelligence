from string import ascii_lowercase
class Question1_Solver:
    def __init__(self, cpt):
        self.cpt = cpt;
        return;

    #####################################
    # ADD YOUR CODE HERE
    # Pr(x|y) = self.cpt.conditional_prob(x, y);
    # A word begins with "`" and ends with "`".
    # For example, the probability of word "ab":
    # Pr("ab") = \
    #    self.cpt.conditional_prob("a", "`") * \
    #    self.cpt.conditional_prob("b", "a") * \
    #    self.cpt.conditional_prob("`", "b");
    # query example:
    #    query: "ques_ion";
    #    return "t";
    def solve(self, query):
        file_name = "question1.txt";
        word = list(query)
        word.append('`');
        word.insert(0,'`');
        predictPostion = word.index('_')
        bestProbability =0;
        bestCharcter ='a'
        for i in ascii_lowercase :
#             currentPredictionWord = word
#             currentPredictionWord[predictPostion] = i;
            currentProbability = self.cpt.conditional_prob(i,word[predictPostion-1])
            currentProbability *= self.cpt.conditional_prob(word[predictPostion+1],i)            
#             for j in range(1, len(currentPredictionWord)) :
#                 currentProbability *= self.cpt.conditional_prob(currentPredictionWord[j],currentPredictionWord[j-1])
            
            if currentProbability > bestProbability :
                bestProbability = currentProbability
                bestCharcter = i;
            
        return bestCharcter;
        
         
        


