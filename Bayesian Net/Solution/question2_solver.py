from string import ascii_lowercase
class Question2_Solver:
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
    #    query: "que__ion";
    #    return ["s", "t"];
    def solve(self, query):
        file_name = "question1.txt";
        word = list(query)
        word.append('`');
        word.insert(0,'`');
        predictPostion = word.index('_')
        bestProbability =0;
        bestCharcter1 ='a'
        bestCharcter2 ='a'
        for i in ascii_lowercase :
            for j in ascii_lowercase :
                currentProbability = self.cpt.conditional_prob(i,word[predictPostion-1])
                currentProbability *= self.cpt.conditional_prob(j,i)
                currentProbability *= self.cpt.conditional_prob(word[predictPostion+2],j)                     
                if currentProbability > bestProbability :
                    bestProbability = currentProbability
                    bestCharcter1 = i;
                    bestCharcter2 = j;
            
        return [bestCharcter1,bestCharcter2] ;


