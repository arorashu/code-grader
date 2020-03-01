import os
import json
import filecmp

# UNAME="aroras"

# BTB_URL="https://" + UNAME + "@agile.bu.edu/bitbucket/scm"

BTB_URL="https://agile.bu.edu/bitbucket/scm/"


# Add all the students here or collect them some other way
STUDENTS=["stud1","stud2"]

# Put your tests here
TESTS=[
    "test1.txt", "test2.txt"
]


foundDir = ["stud1","stud2"]

## clone repositories
## idempotent operation, can be rerun
#example repository
#https://agile.bu.edu/bitbucket/users/andoliv/repos/hw04d_stud/browse


for stud in STUDENTS:
    # Clone each students repository
    STUD_SL=BTB_URL + "/~" + stud + "/hw04d_stud.git"
    os.system('echo \"==========Cloning $STUD_SL==========\"')
    cloneCommand = "git clone " + STUD_SL + " " + stud + "_hw0p4"
    os.system(cloneCommand)

print("clone complete")

errorStudents = []

# compile and run code
# output produced in files, {studName_test1.txt, studName_test1.txt}
# files that cannot be compiled output to {cannot-compile.txt}
# check code
for stud in foundDir:
    try:
        changeDirCommand = f"cd {stud}_hw0p4/src"
        print(changeDirCommand)
        # os.system(changeDirCommand)
        os.chdir(f"{stud}_hw0p4/src")
        print("can change dir")
        print("cur dir: ")
        os.system("pwd")
        javaCompileCommand = "javac edu/bu/ec504/hw0p4/*.java"
        os.system(javaCompileCommand)
        echoCommand =  f' echo("----------For student {stud}:----------")'
        os.system(echoCommand)

        for test in TESTS:
            runJavaClassCommand = f"java edu.bu.ec504.hw0p4.Main < ../../{test} > ../../{stud}_{test}"
            os.system(runJavaClassCommand)

        # os.system("cd ../../")
        os.chdir("../../")
    except:
        errorStudents.append(stud)

with open('cannot-compile.txt', 'w') as outfile:
    json.dump(errorStudents, outfile, indent=2, sort_keys=True)

print("output files generated")


## compare output files with input files
graderFile1 = "grader-test1.txt"
graderFile2 = "grader-test2.txt"

for stud in foundDir:
    studentOutFile1 = f"{stud}_test1.txt"
    studentOutFile2 = f"{stud}_test2.txt"

    try:
        if filecmp.cmp(studentOutFile1, graderFile1, shallow=False):
            print(f"{stud} test1 pass")
        else:
            print(f"{stud} test1 fail")

        if filecmp.cmp(studentOutFile2, graderFile2, shallow=False):
            print(f"{stud} test2 pass")
        else:
            print(f"{stud} test2 fail")
    except:
        print(f"{stud} test1 fail")
        print(f"{stud} test2 fail")

print("grading complete")

