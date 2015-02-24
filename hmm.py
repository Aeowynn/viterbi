'''
 Assignment 5: Hidden Markov Models
 CSCI 3202: Arificial Intelligence
 
 Kara James and Joshua Weaver
 '''

# Print to output file
    # Robot: Conditional probabilities, viterbi path, and average accuracy for all test sequences of 200 steps each
# Read output file for correct command prompt
    # Robot, 1st order hmm & 2d order hmm
    # Typos, 1st order hmm & 2d order hmm

""" Imports """
import sys
import math
import getopt

""" Globals """
problem = sys.argv[-1]
#Check line immediately below:
'''hmm_order = sys.argv[0] # nonfunctional for 2d order'''

colorStates = {}
emission_typos = {}
observationr = ['' for x in xrange(40000)]
realpathr = ['' for x in xrange(40000)]
observationt = ['' for x in xrange(16691)]
realpatht = ['' for x in xrange(16691)]
""" HMM Function """
def robot():
    #make a file to print to
    #output = open("outputr.txt",'w')
    # Read in data from file
    pastState = "none"
    states = ('1:2', '1:3', '2:1', '2:3', '2:4', '3:1', '3:2', '3:3', '3:4', '4:1', '4:2', '4:4')
    start_probability = {   '1:2' : .083,
                            '1:3' : .083,
                            '2:1' : .083,
                            '2:3' : .083,
                            '2:4' : .083,
                            '3:1' : .083,
                            '3:2' : .083,
                            '3:3' : .083,
                            '3:4' : .083,
                            '4:1' : .083,
                            '4:2' : .083,
                            '4:4' : .083
                        }
    #make a viewedstates array that's 4x4 # 4 because smoothing
    viewedStates = [[4 for x in xrange(4)] for x in xrange(4)]
    #make a colorstates dictionary that's as big as needed #1 because smoothing
    #emission_probability
    colorStates = { '1:2' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '1:3' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '2:1' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '2:3' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '2:4' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '3:1' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '3:2' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '3:3' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '3:4' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '4:1' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '4:2' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1},
                    '4:4' : {'r' : 1, 'g' : 1, 'b' : 1, 'y' : 1}
                    }
    #make a transitions array that's each state -> state possibility
    #transition_probability
    transitions = { '1:2' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '1:3' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '2:1' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '2:3' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '2:4' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '3:1' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '3:2' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '3:3' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '3:4' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '4:1' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '4:2' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1},
                    '4:4' : {'1:2' : 1, '1:3' : 1, '2:1' : 1, '2:3' : 1, '2:4' : 1, '3:1' : 1, '3:2' : 1, '3:3' : 1, '3:4' : 1, '4:1' : 1, '4:2' : 1, '4:4' : 1}
                  }
    #while still reading stuff
    testing = False
    with open('Assignment5DataSets/robot_no_momemtum.data') as f:
        i=-1
        j=-1
        for line in f:
            d = line[:5]
           # print "i=",i
            if '..' in d:
                pastState = "none"
                testing = True
                #print "testing"
                #break
                continue
            if d[:1] is '.':
                pastState = "none"
                #break
                continue
            i+=1
            if testing:
                #print "in training j= ",j
                #if j >= 199:
                    #break
                j+=1
                observationr[j] = d[4:]        #Should be reading in testing data's observations
                realpathr[j] = d[:3]           #Should be reading in testing data's actual states
            else:
                #read in line, increment counter for seen that state
                viewedStates[int(d[:1])-1][int(d[2:3])-1] += 1
                #increment counter for seen color at that state
                colorStates[d[:3]][d[4:]] += 1
                #look at past state
                currentState = d[:3]
                if pastState is not 'none':
                    #increment proper state -> state transition for past state to current state
                    transitions[pastState][currentState] += 1
                #set past state to currently veiwed state
                pastState = currentState
    #print "colorStates= ",colorStates 
    #print "transitions= ",transitions
# Overwrite colorStates with the conditional probabilities:
    # For each state, calculate the conditional probability of that color/letter occuring
    # value = colorStates[thing]/viewedStates[thing]
#print "observations = ",observationr
#print "realpath= ",realpathr
    for i in colorStates:
        for j in colorStates[i]:
            #print "i= ",i 
            #print "colorStates[i]= ",colorStates[i]," viewedStates= ",viewedStates[int(i[:1])-1][int(i[2:3])-1]
            colorStates[i][j] = (float(colorStates[i][j])/int(viewedStates[int(i[:1])-1][int(i[2:3])-1]))
            #print "math= ",float(colorStates[i])/float(viewedStates[int(i[:1])-1][int(i[2:3])-1])
            #print "colorStates[i] now= ",colorStates[i]
           
    #print "Conditionals = ",colorStates
    # For each state, calculate the cond prob of moving to any other state in one time step
        # value = transitions[thing]/viewedStates[current]
    for i in transitions:
        for j in transitions[i]:
            transitions[i][j] = (float(transitions[i][j])/int(viewedStates[int(i[:1])-1][int(i[2:3])-1]))
    #print "Observations=", observationr
    (prob,path) =  viterbi(observationr, states, start_probability, transitions, colorStates)
    #output.write("prob: ")
    #output.write(str(prob))
    #output.write("\npath: ")
    #output.write(str(path))
    #output.close()
    #print "viterbi returns: ", (prob, path)   
    #print "Path:", path
    #print "RealPath:", realpathr
    i = 0
    correct = 0
    for item in path:
        #print "path:", path[i]
        #print "realpath:", realpathr[i]
        if path[i] == realpathr[i]:
            #print "incrementing"
            correct += 1
            i+=1
        else:
            i+=1
    print "Num Correct:", correct
    correct = correct/float(40000)
    print "Rate:", correct
    print "For path check outputr.txt"
        
    

def typos():
    #make a file to print to
    output = open("output_typos.txt",'w')
    # Read in data from file
    pastState = "none"
    #Comes from the data file
    states = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
    start_probability = {   'a' : .03846, 'b' : .03846, 'c' : .03846, 'd' : .03846, 'e' : .03846, 'f' : .03846,
                        'g' : .03846, 'h' : .03846, 'i' : .03846, 'j' : .03846, 'k' : .03846, 'l' : .03846, 'm' : .03846,
                        'n' : .03846, 'o' : .03846, 'p' : .03846, 'q' : .03846, 'r' : .03846, 's' : .03846,
                        't' : .03846, 'u' : .03846, 'v' : .03846, 'w' : .03846, 'x' : .03846, 'y' : .03846, 'z' : .03846
                    }
    #make a viewedstates array # 26 because smoothing
    viewedStates = {   'a' : 0, 'b' : 0, 'c' : 0, 'd' : 0, 'e' : 0, 'f' : 0, 'g' : 0, 'h' : 0, 'i' : 0, 'j' : 0, 'k' : 0, 'l' : 0, 'm' : 0,
                       'n' : 0, 'o' : 0, 'p' : 0, 'q' : 0, 'r' : 0, 's' : 0, 't' : 0, 'u' : 0, 'v' : 0, 'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0
                   }
    #make an emission probability dictionary # 1 because smoothing
    # probability next letter will be [] given current correct letter
    #emission_probability
    emission_typos = {
        'q' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'w' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'e' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'r' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        't' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'y' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'u' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'i' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'o' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'p' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'a' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        's' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'd' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'f' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'g' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'h' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'j' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'k' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'l' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'z' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'x' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'c' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'v' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'b' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'n' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'm' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1}
        }
    #make a transitions array that's each state -> state possibility
    transition_typos = {
        'q' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'w' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'e' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'r' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        't' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'y' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'u' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'i' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'o' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'p' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'a' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        's' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'd' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'f' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'g' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'h' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'j' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'k' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'l' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'z' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'x' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'c' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'v' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'b' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'n' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1},
        'm' : {'a' : 1, 'b' : 1, 'c' : 1, 'd' : 1, 'e' : 1, 'f' : 1, 'g' : 1, 'h' : 1, 'i' : 1, 'j' : 1, 'k' : 1, 'l' : 1, 'm' : 1,
                'n' : 1, 'o' : 1, 'p' : 1, 'q' : 1, 'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'v' : 1, 'w' : 1, 'x' : 1, 'y' : 1, 'z' : 1}
        }
    #while still reading stuff
    testing = False
    with open('Assignment5DataSets/typos10.data') as f:
        count = -1  
        for line in f: 
            d = line[:3]
            #print "D=", d
            
            if '..' in d:
                pastState = "none"
                testing = True
                #break
                continue
            #print "D[:1]", d[:1]
            if d[:1] is '_':
                pastState = "none"
                #break
                continue
            if testing:
                count +=1 
                #print "testing"
                observationt[count] = d[2:3]
            else:
                #read in line, increment counter for seen that state
                viewedStates[d[2:3]] += 1
                #increment counter for seen color at that state
                emission_typos[d[:1]][d[2:3]] += 1
                #look at past state
                currentState = d[:1]
                if pastState is not 'none':
                    #increment proper state -> state transition for past state to current state
                    transition_typos[pastState][currentState] += 1
                #set past state to currently veiwed state
                pastState = currentState
        #print "emissions= ",emission_typos
        #print "transitions= ",transition_typos
    
    # Overwrite emissions with the conditional probabilities:
    # For each state, calculate the conditional probability of that letter occuring
    for i in emission_typos:
        for j in emission_typos[i]:
            #print "d[2:3]= ",d[2:3]
            emission_typos[i][j] = (float(emission_typos[i][j])/int(viewedStates[i[:1]]))
            #print "math= ",(float(emission_typos[i][j])/int(viewedStates[d[2:3]]))
           
    #print "Conditionals = ",emission_typos
    # For each state, calculate the cond prob of moving to any other state in one time step
    for i in transition_typos:
        for j in transition_typos[i]:
            transition_typos[i][j] = (float(transition_typos[i][j])/int(viewedStates[i[:1]]))
    #print "observations:", observationt
    #print "length:", len(observationt)
    (prob, path) = viterbi(observationt, states, start_probability, transition_typos, emission_typos)
    #output.write("prob: ")
    #output.write(str(prob))
    #output.write("\npath: ")
    #output.write(str(path))
    #output.close()
    print "For path check output_typos.txt"





"""Viterbi Algorithm"""
#Modified from algorithm on Wikipedia page: http://en.wikipedia.org/wiki/Viterbi_algorithm
def viterbi(observation, states, start_p, TransProb, EmitProb):
    V = [{}]
    #where we save the predicted path
    Path = {}
 
    # Initialize base cases (t == 0)
    for y in states:
        #2d array of 
        #print "start_p[y]= ",start_p[y]," EmitProb[y][observation[0]]= ",EmitProb[y][observation[0]]
        V[0][y] = (math.log10(start_p[y]) + math.log10(EmitProb[y][observation[0]]))
        Path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1, len(observation)):
        V.append({})
        NewPath = {}
 
        for y in states:
            #print "y= ",y," t= ",t," t-1= ",t-1
            (prob, state) = max((V[t-1][y0] + math.log10(TransProb[y0][y]) + math.log10(EmitProb[y][observation[t]]), y0) for y0 in states)
            V[t][y] = prob
            NewPath[y] = Path[state] + [y]
 
        # Don't need to remember the old paths
        Path = NewPath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(observation) != 1:
        n = t
    #print_dptable(V)
    (prob, state) = max((V[n][y], y) for y in states)
    return (10**prob, Path[state])

options, remainder = getopt.getopt(sys.argv[1:], 'p:o:', 
                                                ['problem',
                                                 'order'])
#print 'OPTIONS   :', options

robott = False
typost = False
for opt, arg in options:
    #print "opt= ",opt
    #print "arg= ",arg
    
    if opt in ('-p'):
        if arg in '1':
            robott = True
        elif arg in '2':
            typost = True
        else:
            print "Functionality not implemented"
    elif opt in ('-o'):
        if arg in '1':
            if robott:
                #print "calling robot"
                robot()
            elif typost:
                #print "calling typos"
                typos()
            else:
                print "Functionality not implemented"
        else:
            print "Functionality not implemented"
    
#robot()
#typos()
'''
"""

#Reading the output file
if problem == 1 and hmm_order == 1:
    #output robot stuff
else if problem == 1 and hmm_order == 2:
    #output unimplemented message
else if problem == 2 and hmm_order == 1:
    #output typos stuff
else if problem == 2 and hmm_order == 2:
    #output unimplemented message
else:
    #Output error: bad syntax message

"""
'''




