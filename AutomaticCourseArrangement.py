# -*- coding: utf-8 -*
import sys
import numpy as np
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
import random


class Teacher:
    def __init__(self,strName,veciSubject):
        # subject为向量，第i个表示第i门课的课数（需要一个课程编号的表）
        self.strName = strName
        self.veciSubject = veciSubject
        self.schedule = np.zeros((4,5),dtype= int)
        self.scheduleStudent = np.zeros((4, 5), dtype=int)

    def TimeAvailable(self,time):
        if self.schedule[time[0]][time[1]] == 0:
            return True
        else:
            return False

    def SubjectAvailable(self,iSubjectNum):
        if self.veciSubject[iSubjectNum] > 0:
            return True
        else:
            return False

    def AssignToClass(self,iSubjectNum,iStudent,time):
        self.schedule[time[0]][time[1]] = iSubjectNum
        self.scheduleStudent[time[0]][time[1]] = iStudent
        self.veciSubject[iSubjectNum] = self.veciSubject[iSubjectNum] - 1
        return True

    def bComplete(self):
        bTemp = True
        for i in range(0,len(self.veciSubject)):
            if self.veciSubject[i] != 0:
                bTemp = False
        return bTemp


class Student(Teacher):
    def __init__(self,strName,veciSubject):
        # subject为向量，第i个表示第i门课的课数（需要一个课程编号的表）
        self.strName = strName
        self.veciSubject = veciSubject
        self.schedule = np.zeros((4,5),dtype = int)
        self.scheduleTeacher = np.zeros((4, 5), dtype=int)

    def AssignedTeacher(self, iSubjectNum, iTeacher, time):
        self.schedule[time[0]][time[1]] = iSubjectNum
        self.scheduleTeacher[time[0]][time[1]] = iTeacher
        self.veciSubject[iSubjectNum] = self.veciSubject[iSubjectNum] - 1
        return True



Subelist2 = [0,5,3]
Subelist3 = [0,3,5]
SubeList4 = [0,8,8]
t1 = Teacher("教师1",Subelist2)
t2 = Teacher("教师2",Subelist3)
teacherList = [t1,t2]
s = Student("学生1",SubeList4)
studentList = [s]

bTotalComplete = False
while not bTotalComplete:
    iTeacher = random.randint(0, len(teacherList)-1)
    iStudent = random.randint(0, len(studentList)-1)
    iTimeSession = random.randint(0, 3)
    iTimeDay = random.randint(0, 4)
    iLTime = [iTimeSession,iTimeDay]
    iSubject = random.randint(1, 2)
    if teacherList[iTeacher].TimeAvailable(iLTime) and studentList[iStudent].TimeAvailable(iLTime) and teacherList[iTeacher].SubjectAvailable(iSubject) and studentList[iStudent].SubjectAvailable(iSubject):
        bTemp1 = teacherList[iTeacher].AssignToClass(iSubject,iStudent,iLTime)
        bTemp2 = studentList[iStudent].AssignedTeacher(iSubject,iTeacher,iLTime)
        print studentList[iStudent].schedule
    else:
        xxxxx =1
        #print 'pass'

    #print bTemp1
    #print bTemp2
    #全部完成的判断
    bTeacherComplete = True
    for i in range(0,len(teacherList)):
        if not teacherList[i].bComplete():
            bTeacherComplete = False


    bStudentComplete = True
    for i in range (0,len(studentList)):
        if not studentList[i].bComplete():
            bStudentComplete = False

    if bTeacherComplete and bStudentComplete:
        bTotalComplete = True







