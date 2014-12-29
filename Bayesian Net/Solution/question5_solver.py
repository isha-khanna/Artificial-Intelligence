class Question5_Solver:
    def __init__(self, cpt2):
        self.cpt2 = cpt2;
        return;

    #####################################
    # ADD YOUR CODE HERE
    #         _________
    #        |         v
    # Given  z -> y -> x
    # Pr(x|z,y) = self.cpt2.conditional_prob(x, z, y);
    #
    # A word begins with "``" and ends with "``".
    # For example, the probability of word "ab":
    # Pr("ab") = \
    #    self.cpt2.conditional_prob("a", "`", "`") * \
    #    self.cpt2.conditional_prob("b", "`", "a") * \
    #    self.cpt2.conditional_prob("`", "a", "b") * \
    #    self.cpt2.conditional_prob("`", "b", "`");
    # query example:
    #    query: "ques_ion";
    #    return "t";
    def solve(self, query):
        aplhabets ="abcdefghijklmnopqrstuvwxyz"
        str = "`" + "`" + query + "`" + "`"
        pos = 0 

        for i in range(2,len(str)):
            if str[i]=='_':
                pos=i
                break
        max=0
        char = 0;
        "Computing the maximum conditional probability"
        for x in range(0,26):
             temp = self.cpt2.conditional_prob(str[pos+2], aplhabets[x],str[pos+1]) * \
                    self.cpt2.conditional_prob(str[pos+1], str[pos-1], aplhabets[x]) *\
                    self.cpt2.conditional_prob(aplhabets[x], str[pos-2], str[pos-1])
             if temp > max:
                 max = float(temp)
                 char = x
        
        return aplhabets[char]
    