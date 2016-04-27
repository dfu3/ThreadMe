import threading
import time
import pause

# scheduling algorithms--->
def FCFS(procs, pTime):# First Come First Serve

    readyQ = list()
    sched = list() #printing output list
    procNum = 0
    timeU = 0
    running = True
    curProcTime = procs[0][1]

    while (procNum < len(procs)-1):

        if(timeU < len(procs)): #reads input into queue every time unit until out of processes to sim real time input
            readyQ.append(procs[timeU])

        if(not running): #if the last process in the queue has ended- start the next one
            if(procNum < len(readyQ)-1):
                curProcTime = readyQ[procNum+1][1]
            procNum +=1
            running = True

        curProcTime -=1

        if(curProcTime == 0): #checks to see if the last process is done 'running'
            running = False

        if(procNum < len(readyQ)): #adds to list of processes to be printed
            sched.append(readyQ[procNum][0])

        timeU +=1
        pause.until(pTime + timeU) #for synchronizing printing
        print('\nTime Unit ' + str(timeU) + '\n')
        print('INPUTS:   ' + str(readyQ))
        print('FCFS:     ' + str(sched))


def RR(procs, pTime): #Round Robin

    readyQ = list()
    sched = list() #printing output list
    timeQ = 0 #time quantum starts at zero and inc by 1

    while (len(readyQ) > 0) or (len(procs) > timeQ):

        if(timeQ < len(procs)): #reads input into queue every time unit until out of processes to sim real time input
            readyQ.insert(0, procs[timeQ])

        if(len(readyQ) > 0): #adds next process in queue to the print list if queue is not empty

            sched.append(readyQ[0][0])
            temp = (readyQ[0][0], readyQ[0][1], readyQ[0][2]-1)
            readyQ.pop(0)     #\
                               #>removes current process from queue and adds it to the end if burst time not= 0
            if(temp[2] != 0): #/
                readyQ.append(temp)

        timeQ +=1
        pause.until(pTime + (timeQ*1.01)) #for synchronizing printing
        print('RR:       ' + str(sched))

def STR(procs, pTime): #Shortest Time Remaining

    readyQ = list()
    sched = list() #printing output list
    timeU = 0

    while (len(readyQ) > 0) or (len(procs) > timeU):

        if(timeU < len(procs)): #reads input into queue every time unit until out of processes to sim real time input
            readyQ.append(procs[timeU])

        if(len(readyQ) > 0):

            lowTR = min(proc[2] for proc in readyQ) #find process with least time remaining

            for i in readyQ:
                if(i[2] == lowTR): #finds that process in queue

                    sched.append(i[0])
                    temp = (i[0], i[1], i[2]-1)
                    readyQ.remove(i) #\
                                      #>removes current process from queue and adds it back if it has time remaining
                    if(temp[2] > 0): #/
                        readyQ.append(temp)

                    break #breaks free of loop after arbitrary first find

        timeU +=1
        pause.until(pTime + (timeU*1.02)) #for synchronizing printing
        print('STR:      ' + str(sched))

def HRRN(procs, pTime): #Highest Response Ratio Next

    readyQ = list()
    sched = list() #printing output list
    timeU = 0

    while (len(readyQ) > 0) or (len(procs) > timeU):

        if(timeU < len(procs)): #reads input into queue every time unit until out of processes to sim real time input
            readyQ.append(procs[timeU])

        if(len(readyQ) > 0):

            highRR = max( (((proc[2]-proc[1])+proc[1])/proc[1] ) for proc in readyQ) #find process with HRR

            for i in readyQ:
                if( (((i[2]-i[1])+i[1])/i[1]) == highRR): #finds that process in queue

                    sched.append(i[0])
                    temp = (i[0], i[1], i[2]-1)
                    readyQ.remove(i) #\
                                      #>removes current process from queue and adds it back if it has time remaining
                    if(temp[2] > 0): #/
                        readyQ.append(temp)

                    break

        timeU +=1
        pause.until(pTime + (timeU*1.03)) #for synchronizing printing
        print('HHRN:     ' + str(sched))
# <---

#processes to be scheduled | format: (<PROCESS>, <DURATION>, <MUTABLE VALUE FIELD>)
procsList = [('A', 3, 3), ('B', 2, 2), ('C', 2, 2), ('D', 1, 1), ('E', 3, 3), ('F', 2, 2), ('G', 4, 4), ('H', 1, 1)]
#---
def Main():

    printTime = time.time()

    #spawn threads
    t1 = threading.Thread(target= FCFS, args=(procsList, printTime,))
    t2 = threading.Thread(target= RR, args=(procsList, printTime,))
    t3 = threading.Thread(target= STR, args=(procsList, printTime,))
    t4 = threading.Thread(target= HRRN, args=(procsList, printTime,))

    #start threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    #---
    #loops in threads will self terminate after no more input is read
    #---

if __name__ == '__main__':
    Main()
