# -*- coding: utf-8 -*
import sys
import numpy as np
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
import random
import os

iConstEmpty = -10 #定义一个数表示课表上的空时间
#以学生为父类，对老师进行需要班级的写入
#增加schedule的输入，控制某些学生在某些时间固定上什么课
class Student:
    def __init__(self,strName,veciTeacher,schedule):
        # subject为向量，第i个表示第i门课的课数（需要一个课程编号的表）
        self.strName = strName
        self.veciTeacher = veciTeacher
        self.schedule = schedule

    def TimeAvailable(self, time,iTeacher):

        for i in range(0,3):
            if self.schedule[i][time[1]] == iTeacher and teacherList[iTeacher].strName != u'':
                return False
        if self.schedule[time[0]][time[1]] == iConstEmpty:
            return True
        else:
            return False

    def AssignedTeacher(self, iTeacher, time):
        self.schedule[time[0]][time[1]] = iTeacher
        self.veciTeacher[iTeacher] = self.veciTeacher[iTeacher] - 2
        return True

    def UnAssignedTeacher(self, iTeacher, time):
        self.schedule[time[0]][time[1]] = iConstEmpty
        self.veciTeacher[iTeacher] = self.veciTeacher[iTeacher] + 2

    def CourseLeft(self, iTeacher):
        return self.veciTeacher[iTeacher]

    def bComplete(self):
        bTemp = True
        for i in range(0, len(self.veciTeacher)):
            if self.veciTeacher[i] != 0:
                bTemp = False
        return bTemp

class Teacher(Student):
    def __init__(self,strName,veciStudent,schedule):
        # subject为向量，第i个表示第i门课的课数（需要一个课程编号的表）
        # veciStudent为向量，表明老师在第i个班要上的课程数
        # schedule为np.zeros((4, 5), dtype=int)或者其他，放在外面构造的好处可以限制某些老师或某些班不在某时段上课（统一-1为限制成不上课时间）
        self.strName = strName
        self.veciStudent = veciStudent
        self.schedule = schedule

    def AssignToStudent(self,iStudent,time):
        self.schedule[time[0]][time[1]] = iStudent
        self.veciStudent[iStudent] = self.veciStudent[iStudent] - 2
        return True

    def UnAssignToStudent(self,iStudent,time):
        self.schedule[time[0]][time[1]] = iConstEmpty
        self.veciStudent[iStudent] = self.veciStudent[iStudent] + 2
        return True

    def TimeAvailable(self, time):
        if self.schedule[time[0]][time[1]] == iConstEmpty:
            return True
        else:
            return False

    def CourseLeft(self, iStudent):
        return self.veciStudent[iStudent]

    def bComplete(self):
        bTemp = True
        for i in range(0,len(self.veciStudent)):
            if self.veciStudent[i] != 0:
                bTemp = False
        return bTemp




###excel读入等情形构建模块
import xlrd
###1.常见表转教师学生矩阵
rootdir = '.\input\\'
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件

workbookIn = xlrd.open_workbook('.\input\\' + list[0])
sheet1In = workbookIn.sheet_by_index(0 )
nrows = sheet1In.nrows
ncols = sheet1In.ncols
##第一遍扫描统计班级数量和老师数量并创建teacherNameList和studentNameList
studentNameList = []
studentStartList = []
studentEndList = []
teacherNameList = []

i = 1
iStart = i
iEnd = i
while i < nrows:

    row_data = sheet1In.row_values(i)
    if row_data[1] not in teacherNameList:
        teacherNameList.append(row_data[1])
    if row_data[0] == u'':
        iEnd = i
    else:
        if iStart != iEnd:
            studentStartList.append(iStart)
            studentEndList.append(iEnd)

            iStart = i
            studentNameList.append(row_data[0])
        else:
            studentNameList.append(row_data[0])
    i = i + 1

studentStartList.append(iStart)
studentEndList.append(iEnd)



#生成学生对象LIST
studentList = []
for i in range(0,len(studentNameList)):
    veciTeacher = []
    for iTeacherr in range(0,len(teacherNameList)):
        veciTeacher.append(0)

    #-10表示可以排课的空时间
    timeSchedule = np.linspace(iConstEmpty, iConstEmpty, 15)
    timeSchedule.resize(3, 5)
    print timeSchedule
    for iRow in range(studentStartList[i],studentEndList[i]+1):
        row_data = sheet1In.row_values(iRow)
        # 上午班占用Schedule
        if row_data[2] == "上午班":
            for j in range(0, 2):
                for k in range(0, 5):
                    timeSchedule[j, k] = -1
        # 下午班占用Schedule
        else:
            if row_data[2] == "下午班":
                for k in range(0, 5):
                    timeSchedule[2, k] = -1
            else:
                veciTeacher[teacherNameList.index(row_data[1])] = veciTeacher[teacherNameList.index(row_data[1])]+ int(row_data[3])



    studentList.append(Student(studentNameList[i],veciTeacher,timeSchedule))
    #下午班Schedule

    #无78节课Schedule

#生成教师对象List
teacherList = []
for i in range(0,len(teacherNameList)):

    veciStudent = []
    # -10表示可以排课的空时间
    timeSchedule = np.linspace(iConstEmpty, iConstEmpty, 15)
    timeSchedule.resize(3, 5)

    for iTeacherr in range(0, len(studentNameList)):
        veciStudent.append(0)



    col_data = sheet1In.col_values(1) #老师名称列
    col_dataIntern  = sheet1In.col_values(2) #实习上下午班
    col_dataCourseNum = sheet1In.col_values(3) #周课时列

    while teacherNameList[i] in col_data:
        iTemp = col_data.index(teacherNameList[i])

        if col_dataIntern[iTemp] == "上午班":
            for j in range(0, 2):
                for k in range(0, 5):
                    timeSchedule[j, k] = -1
            # 下午班占用Schedule
        else:
            if col_dataIntern[iTemp] == "下午班":
                for k in range(0, 5):
                    timeSchedule[2, k] = -1
            else:
                iTemp = col_data.index(teacherNameList[i])
                # 找到班级
                for iFindStudent in range(0, len(studentNameList)):
                    if studentStartList[iFindStudent] <= iTemp and iTemp <= studentEndList[iFindStudent]:
                        iStudentFinded = iFindStudent
                        break

                veciStudent[iStudentFinded] = veciStudent[iStudentFinded] + int(col_dataCourseNum[iTemp])
        col_data[iTemp] = -1

    teacherList.append(Teacher(teacherNameList[i],veciStudent,timeSchedule))

bTemp1 = len(teacherList)
print bTemp1
bTeacherComplete = True
for i in range(0,len(teacherList)):
    if not teacherList[i].bComplete():
        bTeacherComplete = False
        bTemp1 = bTemp1 -1
print bTemp1
print 'fffffffffff'

bTotalComplete = False
while not bTotalComplete:

    iTeacher = random.randint(0, len(teacherList)-1)
    iStudent = random.randint(0, len(studentList)-1)
    #iTimeSession = random.randint(0, 2)
    #iTimeDay = random.randint(0, 4)
    #iLTime = [iTimeSession,iTimeDay] #第一个是第几节，第二个是哪一天
    # 以下的while是伪随机(并没有平均分配)
    if not studentList[iStudent].bComplete():
        while teacherList[iTeacher].veciStudent[iStudent] == 0:
            # print teacherList[iTeacher].veciStudent[iStudent]
            iTeacher = (iTeacher + 1) % (len(teacherList))
    else:
        continue

    #print studentList[iStudent].schedule
    re = np.where(studentList[iStudent].schedule == iConstEmpty)
    iTimeRandom = random.randint(0, len(re[0])-1)
    iLTime = [re[0][iTimeRandom],re[1][iTimeRandom]]

    #以下的while也可以改成伪随机形式来提高效率
    bCourseAssigned = False
    iTempLoopCount = 0
    while bCourseAssigned == False:
        if teacherList[iTeacher].TimeAvailable(iLTime) and studentList[iStudent].TimeAvailable(iLTime,iTeacher):
            bTemp1 = teacherList[iTeacher].AssignToStudent(iStudent, iLTime)
            bTemp2 = studentList[iStudent].AssignedTeacher(iTeacher, iLTime)
            if teacherList[iTeacher].CourseLeft(iStudent) == 0 and studentList[iStudent].CourseLeft(iTeacher) == 0:
                bCourseAssigned = True
                print studentList[iStudent].strName
                print studentList[iStudent].schedule
                print teacherList[iTeacher].strName
                print teacherList[iTeacher].schedule
                print 'ggggg'

        else:
            if teacherList[iTeacher].strName == ''and studentList[iStudent].TimeAvailable(iLTime,iTeacher):
                bTemp1 = teacherList[iTeacher].AssignToStudent(iStudent, iLTime)
                bTemp2 = studentList[iStudent].AssignedTeacher(iTeacher, iLTime)
                print studentList[iStudent].strName
                print studentList[iStudent].schedule
                print teacherList[iTeacher].strName
                print teacherList[iTeacher].schedule
                print 'here'
                bCourseAssigned = True
            else:
                iTimeRandom = (iTimeRandom + 1)%len(re[0])
                iLTime = [re[0][iTimeRandom], re[1][iTimeRandom]]
                iTempLoopCount = iTempLoopCount + 1
                print 'llllll'


                #print iLTime
                #print studentList[iStudent].strName
                #print studentList[iStudent].schedule
              #  print teacherList[iTeacher].strName
               # print teacherList[iTeacher].schedule




        while iTempLoopCount > len(re[0]):
            #如果这里卡死了 打乱对应教师和班级重新排课
            #5秒没循环出来，将此老师优先安排并且复原已经安排了的课程。
           # print studentList[iStudent].strName
            #print studentList[iStudent].schedule
            if teacherList[iTeacher].strName == u'':
                print 'here'
            if iTempLoopCount> 1000:
                print 'sdklfjlsdkjf'
            iTimeSession = random.randint(0, 2)
            iTimeDay = random.randint(0, 4)
            iLTime = [iTimeSession, iTimeDay]
            if studentList[iStudent].schedule[iLTime[0]][iLTime[1]] != iConstEmpty and studentList[iStudent].schedule[iLTime[0]][iLTime[1]] != -1:
                iteacherERRNUM = int(studentList[iStudent].schedule[iLTime[0]][iLTime[1]])
                if iteacherERRNUM != iTeacher:
                    print 'errrrrrrrrrrrrrr'
                    teacherList[iteacherERRNUM].UnAssignToStudent(iStudent, iLTime)
                    studentList[iStudent].UnAssignedTeacher(iteacherERRNUM, iLTime)
                    iTempLoopCount = 0

            if teacherList[iTeacher].schedule[iLTime[0]][iLTime[1]] != iConstEmpty and teacherList[iTeacher].schedule[iLTime[0]][iLTime[1]] != -1:
                istudentERRNUM = int(teacherList[iTeacher].schedule[iLTime[0]][iLTime[1]])
                if istudentERRNUM != iStudent:
                    teacherList[iTeacher].UnAssignToStudent(istudentERRNUM, iLTime)
                    studentList[istudentERRNUM].UnAssignedTeacher(iTeacher, iLTime)
                    iTempLoopCount = 0
                    print 'eeee'

            print teacherList[iTeacher].strName

            print 'enddddddddddddddddddddd'
            iTempLoopCount = iTempLoopCount + 1





               # print 'starttttttttttttttt'
                #print studentList[iStudent].strName
               # print studentList[iStudent].schedule
               # print teacherList[iTeacher].strName
               # print teacherList[iTeacher].schedule
              #  print 'midddddddddddddddddddd'

                #print studentList[iStudent].strName
                # print studentList[iStudent].schedule
              #  print teacherList[iTeacher].strName
               # print teacherList[iTeacher].schedule




    bTemp1 = len(teacherList)
    print bTemp1
    bTeacherComplete = True
    for i in range(0,len(teacherList)):
        if not teacherList[i].bComplete():
            bTeacherComplete = False
            bTemp1 = bTemp1 -1
    print bTemp1


    bStudentComplete = True
    for i in range (0,len(studentList)):
        if not studentList[i].bComplete():
            bStudentComplete = False

    if bTeacherComplete and bStudentComplete:
        bTotalComplete = True

print "complete"

###输出模块
import xlwt
workbookOut = xlwt.Workbook(encoding='utf8')
sheet1Out = workbookOut.add_sheet('班级课表')
sheet2Out = workbookOut.add_sheet('教师课表')
iOutRow = 0
for i in range (0,len(studentList)):
    sheet1Out.write(iOutRow, 0, label= studentList[i].strName)
    iOutRow = iOutRow + 1
    for k in range(0,3):
        for j in range(0, 5):
            if studentList[i].schedule[k][j] >= 0:
                sheet1Out.write(iOutRow, j, label=teacherNameList[int(studentList[i].schedule[k][j])])
            else:
                sheet1Out.write(iOutRow, j, label=studentList[i].schedule[k][j])


        iOutRow = iOutRow + 1
    iOutRow = iOutRow + 2


strTemp = u"课表.xls"
workbookOut.save(strTemp)

