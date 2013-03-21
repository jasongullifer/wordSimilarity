#!/usr/bin/python

# Jason Gullifer (jason.gullifer@gmail.com) - 2009
#
# Levenshtein Distance algorithm taken from
# http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
#
# This program computes two word similarity measures: 1) a
# modified version of the Van Orden orthographic similarity measure
# (Van Orden, 1987) for a pairs of words, and 2) a normalized
# Levenshtein Distance measure (Schepens, Dijkstra, & Grootjen, 2011).
#
# Van Orden, G. C. (1987). A ROWS is a ROSE: Spelling, sound, and
# reading. Memory & Cognition, 15(3), 181-198. 
#
# Schepens, J., Dijkstra, T., & Grootjen, F. (2011). Distributions of
# cognates in Europe as based on Levenshtein distance. Bilingualism:
# Language and Cognition, 15(01),
# 157-166. doi:10.1017/S1366728910000623
#
# Usage: python wordSimilarity.py
#
# input.csv should be a comma separated file with two columns. Each
# row should contain your target word and the word it should be
# compared with. No column names should be included. The result will
# be an output file called output_wordSim.csv that contains each word
# pair, its normalized Levenshtein Distance, and its orthographic
# similarity.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import codecs

######### Van Orden Measure of Orthographic Similarity ######### 
class ordenPair :
    wordPair = ()
    orderedPairs = {}
    sharedLetters = []
    sharedPairs = []

    def __init__(self, wordPair,flag=True):
        """ 
        Initialize values and calculate measures
        """
        self.wordPair = wordPair
        self.orderedPairs = {}
        self.sharedLetters = []
        self.sharedPairs = []
        self.f = self.F()
        self.v = self.V()
        self.c = self.C()
        self.a = self.A()
        self.t = self.T()
        self.b = self.B()
        self.e = self.E()
        self.gs = 10*((float((50*self.f+30*self.v+10*self.c))/float(self.a))+5*self.t+27*self.b+18*self.e)
        if (flag):
            self.os = self.gs / float(ordenPair((self.wordPair[0],self.wordPair[0]),False).gs)


    def getSharedFeatures(self,input):
        """
        Function that finds shared features between two words, i.e. letters
        """
        featureSet = {}
        sharedFeatures = []

        if len(input) > 1:
            for feature in input[0]:
                featureSet['%s' % feature] = (feature in input[1])

            for key in featureSet.keys():
                if featureSet[key] == True:
                    sharedFeatures.append(key)

            return sharedFeatures

        else:
            for feature in input[0]:
                featureSet['%s' % feature] = (feature in input[0])
            
            for key in featureSet.keys():
                sharedFeatures.append(key)
            return sharedFeatures

    def F(self):
        """
        Computes the number of pairs of adjacent letters in the same order
        """
        
        for word in self.wordPair:
            letterList=[]
            previousLetter = word[0]
            for letter in word[1:len(word)]:
                letterList.append(previousLetter+letter)
                previousLetter = letter
            self.orderedPairs[word] = letterList

    
        self.sharedPairs = self.getSharedFeatures(self.orderedPairs.values())
        return len(self.sharedPairs)

    def V(self):
        """
        Computes the number of pairs of adjacent letters in reverse order
        """
        if len(self.orderedPairs) > 1:
            key1 = self.orderedPairs.keys()[0]
            key2 = self.orderedPairs.keys()[1]
        else:
            key1 = self.orderedPairs.keys()[0]
            key2 = self.orderedPairs.keys()[0]

        pairList = []

        for pair in self.orderedPairs[key1]:
            pairList.append(pair[::-1])

        featureSet = {}
        sharedFeatures = []

        for feature in pairList:
            featureSet['%s'%feature] = (feature in self.orderedPairs[key2])

        for key in featureSet.keys():
            if featureSet[key] == True:
                sharedFeatures.append(key)

        return len(sharedFeatures)


    def C(self):
        """
        Computes the number of single letters shared by word pairs
        """
        cnt_w1 = {}
        cnt_w2 = {}
        count = 0
        for letter in self.wordPair[0]:
            cnt_w1[letter] = cnt_w1.get(letter,0)+1

        for letter in self.wordPair[1]:
            cnt_w2[letter] = cnt_w2.get(letter,0)+1
       

        for letter in cnt_w1:
            if cnt_w2.has_key(letter):
                if cnt_w2[letter] < cnt_w1[letter]:
                    count = count+cnt_w2[letter]
                else:
                    count = count+cnt_w1[letter]

        return count
    def A(self):
        """
        Computes the average number of letters in the pair
        """
        return float(len(self.wordPair[0]) + float(len(self.wordPair[1]))) / float(2)

    def T(self):
        """
        Computes the ratio of number of letters in the shorter to longer pair
        """
        if (len(self.wordPair[0]) < len(self.wordPair[1])):
            return float(len(self.wordPair[0])) / float(len(self.wordPair[1]))
        else:
            return float(len(self.wordPair[1])) / float(len(self.wordPair[0]))

    def B(self):
        """
        1 if letter 1 is the same
        """
        if(self.wordPair[0][0] == self.wordPair[1][0]):
            return 1
        else:
            return 0

    def E(self):
        """
        1 if last letter is the same
        """
        if(self.wordPair[0][len(self.wordPair[0])-1] == self.wordPair[1][len(self.wordPair[1])-1]):
            return 1
        else:
            return 0

######### Normalized Levenshtein Distance #########         
class ldPair:
    wordPair = ()
    lengths = ()
    levdist = None
    normlevdist = None
    maxlength = None
    
    def __init__(self, wordPair):
        self.wordPair = wordPair
        self.levdist = self.levDist(wordPair[0],wordPair[1])
        self.getLengths()
        self.normlevdist = self.normalize()

    def getLengths(self):
        self.lengths = (len(self.wordPair[0]),len(self.wordPair[1]))
        self.maxLength = max(self.lengths)
        
    def levDist(self, seq1, seq2):
        oneago = None
        thisrow = range(1, len(seq2) + 1) + [0]
        for x in xrange(len(seq1)):
            twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
            for y in xrange(len(seq2)):
                delcost = oneago[y] + 1
                addcost = thisrow[y - 1] + 1
                subcost = oneago[y - 1] + (seq1[x] != seq2[y])
                thisrow[y] = min(delcost, addcost, subcost)
        return thisrow[len(seq2) - 1]
    
    def normalize(self):
        return (1-(float(self.levdist) / float(max(len(self.wordPair[0]),len(self.wordPair[1])))))

def main():
    wordpairs = open('input.csv','rU') #U makes cross platform encoding
    lines = []
    for line in wordpairs:
        lines.append(line.decode("utf-8").strip('\n').split(','))

    wordpairs.close()

    for line in lines:
        line.append(ldPair(line[0:2]).normlevdist)
        line.append(ordenPair(line[0:2]).os)

    print lines

    file = codecs.open("output_wordSim.csv",encoding="utf-8",mode="w")
    file.write("Word1,Word2,normlevdist,os\n")
    for line in lines:
        for item in line:
            file.write(unicode(item)+",")
        file.write("\n")
    file.close()

if __name__ == "__main__":
    main()
