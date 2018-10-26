# -*- coding: utf-8 -*
import sys
import numpy as np
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
import random
import os

########################1.1版本
# 加入veciSubject
########################2.0版本
# 输出改成总课表模式
########################2.1版本(working)
# 修改一个老师同一天上一个班两门不同课程会卡死的问题
####################################

iConstEmpty = -10 #定义一个数表示课表上的空时间
iTeacherVoid = -15 #写死的教师
#以学生为父类，对老师进行需要班级的写入
#增加schedule的输入，控制某些学生在某些时间固定上什么课
class Student:
    def __init__(self,strName,veciTeacher,veciSubject,schedule):
        # subject为向量，第i个表示第i门课的课数（需要一个课程编号的表）
        self.strName = strName
        self.veciTeacher = veciTeacher # index 为老师编号，内容为 [老师在这个班的总周课时（多门课程之和）]
        self.veciSubject = veciSubject # index 为老师编号，内容为 [课程编号，周课时]
        self.schedule = schedule #教师编号
        self.subjectSchedule =  np.copy(self.schedule) #课程编号
        self.iSubject = -20 #


    def TimeAvailable(self, time,iTeacher):
        #是否需要传入，课程名字
        #if len(veciSubject[iTeacher]) == 1:
        #这里要等到读入总排课表和去掉上下午班才能做！！！！！！！！！！！！！！！！！！！
        imaxTeacherSubjectLen = 0
        for i in range(0,len(veciSubject)):
            if imaxTeacherSubjectLen < len(veciSubject[i]):
                imaxTeacherSubjectLen = len(veciSubject[i])

        #print 'here'
        #self.iSubjectiSubject = random.randint(0, len(self.veciSubject[iTeacher]) - 1)
        #while self.veciSubject[iTeacher][self.iSubject][1] == 0:
            #self.iSubject = (self.iSubject + 1) % (len(self.veciSubject[iTeacher]))



        for i in range(0,3):
            if self.subjectSchedule[i][time[1]] == self.iSubject and teacherList[iTeacher].strName != u'':
                return False

        for i in range(0,3):
            if self.schedule[i][time[1]] == iTeacher and teacherList[iTeacher].strName != u'':
                # 第一个判断为限定老师一天只上这个班一节课！！！！！！！！！！！！！！！！！！！！！
                # 后期随机生成科目时根据科目判断
                # 所以要记录今天上了哪些科目了
                return False
        if self.schedule[time[0]][time[1]] == iConstEmpty:
            return True
        else:
            return False

    def AssignedTeacher(self, iTeacher, time):
        self.schedule[time[0]][time[1]] = iTeacher
        self.veciTeacher[iTeacher] = self.veciTeacher[iTeacher] - 2
        iSubject = random.randint(0, len(self.veciSubject[iTeacher]) - 1)
        while self.veciSubject[iTeacher][iSubject][1] == 0:
            iSubject = (iSubject + 1) % (len(self.veciSubject[iTeacher]))
        self.subjectSchedule[time[0]][time[1]] = self.veciSubject[iTeacher][iSubject][0]
        return True

    def UnAssignedTeacher(self, iTeacher, time):
        self.veciTeacher[iTeacher] = self.veciTeacher[iTeacher] + 2
        self.schedule[time[0]][time[1]] = iConstEmpty
        for iSubjectPosition in range(0,len(self.veciSubject[iTeacher])):
            if self.veciSubject[iTeacher][iSubjectPosition][0] ==  self.subjectSchedule[time[0]][time[1]]:
                self.veciSubject[iTeacher][iSubjectPosition][1] =  self.veciSubject[iTeacher][iSubjectPosition][1] + 2
        self.subjectSchedule[time[0]][time[1]] = iConstEmpty

    def bComplete(self):
        bTemp = True
        for i in range(0, len(self.veciTeacher)):
            if self.veciTeacher[i] != 0:
                bTemp = False
        return bTemp

class Teacher(Student):
    def __init__(self,strName,veciStudent,veciSubject,schedule):
        # subject为向量，第i个表示第i门课的课数（需要一个课程编号的表）
        # veciStudent为向量，表明老师在第i个班要上的课程数
        # schedule为np.zeros((4, 5), dtype=int)或者其他，放在外面构造的好处可以限制某些老师或某些班不在某时段上课（统一-1为限制成不上课时间）
        self.strName = strName
        self.veciStudent = veciStudent
        self.veciSubject = veciSubject
        self.schedule = schedule
        self.subjectSchedule = []#无用变量，teacher其实不需要课程判断，因为在班级的TimeAvailable中已经判断过了

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

    def bComplete(self):
        bTemp = True
        for i in range(0,len(self.veciStudent)):
            if self.veciStudent[i] != 0:
                bTemp = False
        return bTemp

    def scheduleScore(self):
        #老师时间越集中分数越高
        if True:
            iScoreTemp = 0
            for i in range(0,5):
                iTemp = 0
                for j in range(0,3):
                    if self.schedule[j][i] != -10:
                        iTemp = iTemp + 1
                iScoreTemp = iScoreTemp + iTemp*iTemp
        #后续添加老师不希望课程集中的评分情形
        return iScoreTemp

def colIndex2Time(i):
    #根据总课表中列对应的位置转换出Time结构体
    time = []
    iSessionIndex = (i-1)%8 #每天的第几节相关
    if iSessionIndex>=0 and iSessionIndex<=3: #第一二节
        time.append(0)
    if iSessionIndex>=4 and iSessionIndex<=5: #第三四节
        time.append(1)
    if iSessionIndex>=6 and iSessionIndex<=7: #第五六节
        time.append(2)

    iDayIndex =(i-1)//8 #第几天相关
    time.append(iDayIndex)

    return time




###excel读入等情形构建模块
import xlrd
###常见表转教师学生矩阵
rootdir = '.\input\\'
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
workbookIn = xlrd.open_workbook('.\input\\' + list[0])

workbookTotalTimeTable = xlrd.open_workbook('.\input\\' + list[1]) # 读入已有的总课表，占用掉已经排好的实习和计算机课
sheetTotalTimeTableIn =  workbookTotalTimeTable.sheet_by_index(2)


sheet1In = workbookIn.sheet_by_index(0)
nrows = sheet1In.nrows
ncols = sheet1In.ncols
##第一遍扫描统计班级数量和老师数量并创建teacherNameList和studentNameList和subjectNameList
studentNameList = []
studentStartList = []
studentEndList = []
teacherNameList = []
subjectNameList = []

#列指标
iClassCol = 0
iTeacherCol = 1
iSubjectCol = 2
iPeriodCol = 3
iElseCol = 4
#subjectNameList构造
row_data = sheet1In.col_values(iSubjectCol)
subjectNameList = []
for i in range(1,nrows):
    if row_data[i] not in subjectNameList:
        subjectNameList.append(row_data[i])
#for i in range(0,len(subjectNameList)):
    #print subjectNameList[i]
#判断一个班级的课程安排是从excel的第几行到第几行
i = 1
iStart = i
iEnd = i
while i < nrows:

    row_data = sheet1In.row_values(i)
    if row_data[1] not in teacherNameList:
        teacherNameList.append(row_data[1])
    if row_data[iClassCol] == u'':
        iEnd = i
    else:
        if iStart != iEnd:
            studentStartList.append(iStart)
            studentEndList.append(iEnd)

            iStart = i
            studentNameList.append(row_data[iClassCol])
        else:
            studentNameList.append(row_data[iClassCol])
    i = i + 1

studentStartList.append(iStart)
studentEndList.append(iEnd)

while True:

    # 其实这学生对象LIST和教师对象LIST生成放在每次评分循环外面可以提升速度
    # 留在后期优化，暂时速度能达到要求
    # 生成学生对象LIST
    studentList = []
    for i in range(0, len(studentNameList)):
        veciTeacher = []
        for iTeacherr in range(0, len(teacherNameList)):
            veciTeacher.append(0)

        veciSubject = []
        #veciSubject的结构见如下例子
        #例如5号老师在该班有课程1,4节 课程2,2节
        #则veciSubject[5] 为[[课程1，4]，[课程2，5]]
        for iTeacherr in range(0, len(teacherNameList)):
            tempList = []
            veciSubject.append(tempList)



        # -10表示可以排课的空时间
        timeSchedule = np.linspace(iConstEmpty, iConstEmpty, 15)
        timeSchedule.resize(3, 5)

        #周三下午不排课
        timeSchedule[2, 2] = -1

       # print timeSchedule
        for iRow in range(studentStartList[i], studentEndList[i] + 1):
            row_data = sheet1In.row_values(iRow)
            # 上午班占用Schedule
            if row_data[iElseCol] == "上午班":
                for j in range(0, 2):
                    for k in range(0, 5):
                        timeSchedule[j, k] = -1
            # 下午班占用Schedule
            else:
                if row_data[iElseCol] == "下午班":
                    for k in range(0, 5):
                        timeSchedule[2, k] = -1
                else:
                    veciTeacher[teacherNameList.index(row_data[iTeacherCol])] = veciTeacher[teacherNameList.index(row_data[iTeacherCol])] + int(row_data[3])
                    tempSubjcetList = [subjectNameList.index(row_data[iSubjectCol]),int(row_data[iPeriodCol])]
                    veciSubject[teacherNameList.index(row_data[iTeacherCol])].append(tempSubjcetList)


        studentList.append(Student(studentNameList[i], veciTeacher, veciSubject,timeSchedule))

        # 下午班Schedule

        # 无78节课Schedule

    # 生成教师对象List
    teacherList = []
    for i in range(0, len(teacherNameList)):

        veciStudent = []
        # -10表示可以排课的空时间
        timeSchedule = np.linspace(iConstEmpty, iConstEmpty, 15)
        timeSchedule.resize(3, 5)

        # 周三下午不排课
        timeSchedule[2,2] = -1

        for iTeacherr in range(0, len(studentNameList)):
            veciStudent.append(0)

        veciSubject = []
        # veciSubject的结构见如下例子
        # 例如5号班级在该老师要上课程1,4节 课程2,2节
        # 则veciSubject[5] 为[[课程1，4]，[课程2，5]]
        for iTeacherr in range(0, len(studentNameList)):
            tempList = []
            veciSubject.append(tempList)

        col_data = sheet1In.col_values(iTeacherCol)  # 老师名称列
        col_dataIntern = sheet1In.col_values(iElseCol)  # 实习上下午班
        col_dataCourseNum = sheet1In.col_values(iPeriodCol)  # 周课时列
        col_dataCourseName = sheet1In.col_values(iSubjectCol) #课程名称列

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
                    tempSubjcetList = [subjectNameList.index(col_dataCourseName[iTemp]), int(col_dataCourseNum[iTemp])]
                    veciSubject[iStudentFinded].append(tempSubjcetList)

            col_data[iTemp] = -1

        # timeSchedule加上其他条件

        teacherList.append(Teacher(teacherNameList[i], veciStudent,veciSubject, timeSchedule))

    ###############################################################################################
    #根据已有的总课表给出班级和教师需要占用的时间//现在的输入，去掉这一段就可以运行
    ###############################################################################################
    nrows = sheetTotalTimeTableIn.nrows
    ncols = sheetTotalTimeTableIn.ncols

    for iClassRow in range(4,nrows):
        TempClassRow = sheetTotalTimeTableIn.row_values(iClassRow)
        for iCol in range(1,ncols):
            tempTime = colIndex2Time(iCol)
            if TempClassRow[iCol] != u'':
                if TempClassRow[0] in studentNameList:
                    #tempTime = colIndex2Time(iCol)
                    if iCol%2 == 1: #课程
                            studentList[studentNameList.index(TempClassRow[0])].subjectSchedule[tempTime[0]][tempTime[1]] = -1
                    else: #老师
                            studentList[studentNameList.index(TempClassRow[0])].schedule[tempTime[0]][tempTime[1]] = -1

                if TempClassRow[iCol] in teacherNameList:
                    tempTime = colIndex2Time(iCol)
                    if iCol%2 == 1:
                        print 'error, subject Col should not be here'
                    else:
                        if TempClassRow[0] in studentNameList:
                            teacherList[teacherNameList.index(TempClassRow[iCol])].schedule[tempTime[0]][tempTime[1]] = -1

                #print 'here'
            else:
                x = 1
                #print 'hereeeeeeeee'

    ##############################################################################################
    #随机查找
    ###############################################################################################
    bTotalComplete = False
    while not bTotalComplete:

        iTeacher = random.randint(0, len(teacherList) - 1)
        iStudent = random.randint(0, len(studentList) - 1)
        # iTimeSession = random.randint(0, 2)
        # iTimeDay = random.randint(0, 4)
        # iLTime = [iTimeSession,iTimeDay] #第一个是第几节，第二个是哪一天
        # 以下的while是伪随机(并没有平均分配)
        if not studentList[iStudent].bComplete():
            while teacherList[iTeacher].veciStudent[iStudent] == 0:
                # print teacherList[iTeacher].veciStudent[iStudent]
                iTeacher = (iTeacher + 1) % (len(teacherList))
        else:
            continue

        # print studentList[iStudent].schedule
        re = np.where(studentList[iStudent].schedule == iConstEmpty)
        if len(re[0]) == 0:  #DEBUG;进入这个地方表明学生时间表已经填满，但是学生还有未排上的课
            x = 1
            print 'here'     #常见有78节课，以及写课冲突等

        iTimeRandom = random.randint(0, len(re[0]) - 1)
        iLTime = [re[0][iTimeRandom], re[1][iTimeRandom]]

        # 以下的while也可以改成伪随机形式来提高效率AssignToStudent
        bCourseAssigned = False
        iTempLoopCount = 0
        while bCourseAssigned == False:
            if teacherList[iTeacher].TimeAvailable(iLTime) and studentList[iStudent].TimeAvailable(iLTime, iTeacher):
                bTemp1 = teacherList[iTeacher].AssignToStudent(iStudent, iLTime)
                bTemp2 = studentList[iStudent].AssignedTeacher(iTeacher, iLTime)
                if teacherList[iTeacher].veciStudent[iStudent] == 0 and studentList[iStudent].veciTeacher[iTeacher] == 0:
                    bCourseAssigned = True
                    #print teacherList[iTeacher].strName


            else:
                if teacherList[iTeacher].strName == '' and studentList[iStudent].TimeAvailable(iLTime, iTeacher):
                    bTemp1 = teacherList[iTeacher].AssignToStudent(iStudent, iLTime)
                    bTemp2 = studentList[iStudent].AssignedTeacher(iTeacher, iLTime)
                    bCourseAssigned = True
                else:
                    iTimeRandom = (iTimeRandom + 1) % len(re[0])
                    iLTime = [re[0][iTimeRandom], re[1][iTimeRandom]]
                    iTempLoopCount = iTempLoopCount + 1

            while iTempLoopCount > len(re[0]):
                # 如果这里卡死了 打乱对应教师和班级重新排课
                # 5秒没循环出来，将此老师优先安排并且复原已经安排了的课程。
                print studentList[iStudent].strName
                print teacherList[iTeacher].strName
                #print studentList[iStudent].schedule

                iTimeSession = random.randint(0, 2)
                iTimeDay = random.randint(0, 4)
                iLTime = [iTimeSession, iTimeDay]
                if studentList[iStudent].schedule[iLTime[0]][iLTime[1]] != iConstEmpty and \
                        studentList[iStudent].schedule[iLTime[0]][iLTime[1]] != -1:
                    # 这一句的判断决定了，如果读入总课表时写死不填-1，就会进入取消循环。。所以读入总课表时只能都写-1
                    # 若要改善，需要给出一个写死课程的课程名list进入这里判断。。。
                    iteacherERRNUM = int(studentList[iStudent].schedule[iLTime[0]][iLTime[1]])
                    if iteacherERRNUM != iTeacher:
                       # print 'errrrrrrrrrrrrrr'
                        teacherList[iteacherERRNUM].UnAssignToStudent(iStudent, iLTime)
                        studentList[iStudent].UnAssignedTeacher(iteacherERRNUM, iLTime)
                        iTempLoopCount = 0

                if teacherList[iTeacher].schedule[iLTime[0]][iLTime[1]] != iConstEmpty and \
                        teacherList[iTeacher].schedule[iLTime[0]][iLTime[1]] != -1:
                    istudentERRNUM = int(teacherList[iTeacher].schedule[iLTime[0]][iLTime[1]])
                    if istudentERRNUM != iStudent:
                        teacherList[iTeacher].UnAssignToStudent(istudentERRNUM, iLTime)
                        studentList[istudentERRNUM].UnAssignedTeacher(iTeacher, iLTime)
                        iTempLoopCount = 0


        bTemp1 = len(teacherList)
     #   print bTemp1
        bTeacherComplete = True
        for i in range(0, len(teacherList)):
            if not teacherList[i].bComplete():
                bTeacherComplete = False
                bTemp1 = bTemp1 - 1
       # print bTemp1

        bStudentComplete = True
        for i in range(0, len(studentList)):
            if not studentList[i].bComplete():
                bStudentComplete = False

        if bTeacherComplete and bStudentComplete:
            bTotalComplete = True

    ###############################################################################################
    ###输出
    ###############################################################################################
    import xlwt

    workbookOut = xlwt.Workbook(encoding='utf8')
    sheetTout = workbookOut.add_sheet('总课表')
    sheet1Out = workbookOut.add_sheet('班级课表')
    sheet2Out = workbookOut.add_sheet('教师课表')
    iOutRow = 0

    ###总课表输出
    #表头
    sheetTout.write(iOutRow, 0, label='班级')
    sheetTout.write(iOutRow, 1, label='星期一')
    sheetTout.write(iOutRow, 9, label='星期二')
    sheetTout.write(iOutRow, 17, label='星期三')
    sheetTout.write(iOutRow, 25, label='星期四')
    sheetTout.write(iOutRow, 33, label='星期五')
    iOutRow = 1
    for i in range(0,5):
        sheetTout.write(iOutRow, i*8+1, label='1')
        sheetTout.write(iOutRow, i*8+3, label='2')
        sheetTout.write(iOutRow, i*8+5, label='3,4')
        sheetTout.write(iOutRow, i*8+7, label='5,6')


    iOutRow = 2
    for i in range(0, len(studentList)):
        sheetTout.write(iOutRow, 0, label=studentList[i].strName)
        iOutCol = 1
        for j in range(0, 5):
            for k in range(0, 3):
                if k == 0:#由于原来的excel第一节和第二节有两格，所以要重复输入
                    if studentList[i].schedule[k][j] >= 0:
                        sheetTout.write(iOutRow, iOutCol,     label=subjectNameList[int(studentList[i].subjectSchedule[k][j])])
                        sheetTout.write(iOutRow, iOutCol + 1, label=teacherNameList[int(studentList[i].schedule[k][j])])
                        sheetTout.write(iOutRow, iOutCol + 2, label=subjectNameList[int(studentList[i].subjectSchedule[k][j])])
                        sheetTout.write(iOutRow, iOutCol + 3, label=teacherNameList[int(studentList[i].schedule[k][j])])
                        iOutCol = iOutCol + 2
                    else:
                        #######
                        # 这个else是DEBUG项，规定写不写-1（占用）和-10（空）
                        # 注意取消DEBUG输出时，要保留最后的iOutCol = iOutCol + 2跳格
                        sheetTout.write(iOutRow, iOutCol, label=studentList[i].schedule[k][j])
                        sheetTout.write(iOutRow, iOutCol + 1, label=iTeacherVoid)
                        sheetTout.write(iOutRow, iOutCol + 2, label=studentList[i].schedule[k][j])
                        sheetTout.write(iOutRow, iOutCol + 3, label=iTeacherVoid)
                        #######
                        iOutCol = iOutCol + 2
                else:
                    if studentList[i].schedule[k][j] >= 0:
                        sheetTout.write(iOutRow, iOutCol, label=subjectNameList[int(studentList[i].subjectSchedule[k][j])])
                        sheetTout.write(iOutRow, iOutCol+1, label=teacherNameList[int(studentList[i].schedule[k][j])])
                    else:
                    # 这个else是DEBUG项，规定写不写-1（占用）和-10（空）
                        sheetTout.write(iOutRow, iOutCol, label=studentList[i].schedule[k][j])
                        sheetTout.write(iOutRow, iOutCol + 1, label=iTeacherVoid)


                iOutCol = iOutCol + 2


        iOutRow = iOutRow + 1


    #班级课表输出
    iOutRow = 0
    for i in range(0, len(studentList)):
        sheet1Out.write(iOutRow, 0, label=studentList[i].strName)
        iOutRow = iOutRow + 1
        for k in range(0, 3):
            for j in range(0, 5):
                if studentList[i].schedule[k][j] >= 0:
                    sheet1Out.write(iOutRow, j, label=teacherNameList[int(studentList[i].schedule[k][j])])
                else:
                    sheet1Out.write(iOutRow, j, label=studentList[i].schedule[k][j])

            iOutRow = iOutRow + 1
        iOutRow = iOutRow + 2

    iOutRow = 0
    iScore = 0
    for i in range(0, len(teacherList)):

        iScore = iScore + teacherList[i].scheduleScore()

        sheet2Out.write(iOutRow, 0, label=teacherList[i].strName)
        #print teacherList[i].strName
        #print teacherList[i].schedule
        iOutRow = iOutRow + 1
        for k in range(0, 3):
            for j in range(0, 5):
                if teacherList[i].schedule[k][j] >= 0:
                    sheet2Out.write(iOutRow, j, label=studentNameList[int(teacherList[i].schedule[k][j])])
                else:
                    sheet2Out.write(iOutRow, j, label=teacherList[i].schedule[k][j])
            iOutRow = iOutRow + 1
        iOutRow = iOutRow + 2

    print iScore
    strTemp = u"课表" + str(iScore) + ".xls"
    workbookOut.save(strTemp)




