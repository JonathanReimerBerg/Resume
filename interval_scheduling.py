# Jonathan Reimer-Berg

#Inputs for parts a-c
lyst = [[1,2,4],[2,5,1],[2,6,3],[5,9,4],[6,10,4]]
lyst = sorted(lyst, key=lambda tup: tup[1])
M = [None] * len(lyst)

#Helper function for (a) through (c)
def p(j):
    count = 0
    start = lyst[j][0]
    for i in range(0, len(lyst) - 1):
        if lyst[i][1] <= lyst[j][0]:
            count += 1
        else:
            return (count - 1)
        
#Part a: Works for all test cases
def M_Compute_Opt(j, M):    
    if j == -1:
        return 0
    elif M[j] != None:
        return M[j]
    else:
        M[j] = max(lyst[j][2] + M_Compute_Opt(p(j), M), M_Compute_Opt(j - 1, M))
        return M[j]

print(M_Compute_Opt(len(lyst) - 1, M))

#Part b: Seems to be fairly close...
def find_solution(j):
    if j != 0:
        if (lyst[j][2] + M[p(j)]) >= M[j-1]:
            print(j, "is part of the solution")
            find_solution(p(j))
        else:
            find_solution(j - 1)

find_solution(len(lyst)-1)

#Part c: Works for all the test cases
def Iterative_Compute_Opt(j):
    M = [None]*(len(lyst) + 1)
    M[0] = 0
    for i in range(1, j + 2):
        if (p(i - 1)) == -1:
            M[i] = max(lyst[i - 1][2] + M[p(i - 1) + 1], M[i - 1])
        else:
            M[i] = max(lyst[i - 1][2] + M[p(i - 1)+1], M[i - 1])
    return M[-1]

print(Iterative_Compute_Opt(len(lyst) - 1))

# Q6.2 Works for all the test cases
def computer_projects(h, l):
    values = []
    values.append(max(h[0], l[0]))
    i = 0
    while i < len(h):
        values.append(max(l[i] + values[-1], h[i] + values[-2]))
        i += 1
    print(values[-1])


# Q 6.4: Based off of your code. I understand all of the lines (and is much
#shorter than what I was doing before).
def locations(n, M, N, S):
    endN = [0] * len(N)
    endS = [0] * len(S)
    endN[0] = N[0]
    endS[0] = S[0]
    for i in range(1, n):
        endN[i](min(N[i] + endN[i-1], endS[i-1] + M + N[i]))
        endS[i](min(S[i] + endS[i-1], endN[i-1] + M + S[i]))
    print(min(endN[-1], endS[-1]))
            
