from ctypes import *
dll = cdll.LoadLibrary('Proposed.dll')
def enOpen(Inpfile,rtpfile,f3):
    inp=(c_char * 100)(*bytes(Inpfile,'utf-8'))
    rtp=(c_char * 100)(*bytes(rtpfile,'utf-8'))
    f_3=(c_char * 100)(*bytes(f3,'utf-8'))
    errcode=dll.ENopen(inp,rtp, f_3)
    return errcode

def enClose():
    errcode=dll.ENclose()
    return errcode

def enInput(Obsfile,GPU_CODE=0,numThreads_CPU=1):
    obs=(c_char * 100)(*bytes(Obsfile,'utf-8'))
    errcode = dll.ENinput(obs,c_int(GPU_CODE),c_int(numThreads_CPU))
    return errcode

def enCloseInput():
    errcode = dll.ENcloseInput()
    return errcode

def enInitDemandCalibration():
    errcode=dll.ENinitDemandCalibration()
    return errcode

def enDemandCalibration(NumIters=20,Step=0.25):
    obj=dll.ENdemandCalibration(c_int(NumIters),c_float(Step))
    return obj

def enGetdemandCOV(row,col):
    cov = pointer(c_float(0))#传入指针
    errcode=dll.ENgetDemandCOV(c_int(row),c_int(col),cov)
    cov = cov.contents.value
    return [errcode,cov]

def enGetroughnessCOV(row,col):
    cov = pointer(c_double(0))#传入指针
    errcode=dll.ENgetRoughnessdCOV(c_int(row),c_int(col),cov)
    cov = cov.contents.value
    return [errcode,cov]

def enCloseDemandCalibration():
    errcode=dll.ENcloseDemandCalibration()
    return errcode

def enCalculatedemandJacobian_one(jacobianCode=1,index=1, numNode=8):
    enOpenH()
    enInitH()
    enRunH()
    dll.ENcalculatedemandJacobian_one(c_int(jacobianCode),c_int(index))
    jacobian=[]
    for i in range(numNode):
        index=i+1
        value=pointer(c_float(0))
        dll.ENgetdemandJacobian_one(c_int(index), value)
        jacobian.append(value.contents.value)
    dll.ENclosedemandJacobian_one()
    enCloseH()
    return jacobian





def enInitRoughnessCalibration():
    errcode=dll.ENinitRoughnessCalibration()
    return errcode

def enRoughnessCalibration(NumIters=20,Step=0.25):
    obj=dll.ENroughnessCalibration(c_int(NumIters),c_float(Step))
    return obj

def enCloseRoughnessCalibration():
    errcode=dll.ENcloseRoughnessCalibration()
    return errcode

def enSaveinpfile(Inpfile):
    inp=(c_char * 10000)(*bytes(Inpfile,'utf-8'))
    errcode=dll.ENsaveinpfile(inp)
    return errcode
def enSolveH():
    errcode=dll.ENsolveH()
    return errcode

def enOpenH():
    errcode=dll.ENopenH()
    return errcode

def enInitH(int_var=0):
    errcode=dll.ENinitH(c_int(int_var))
    return errcode

def enRunH(time=0):
    T = pointer(c_long(time))
    errcode=dll.ENrunH(T)
    return errcode

def enNextH(tstep):
    t=pointer(c_long(tstep))
    errcode=dll.ENnextH(t )
    t=t.contents.value
    return errcode,t

def enCloseH():
    errcode=dll.ENcloseH()
    return errcode

def enSaveH():
    errcode=dll.ENsaveH()
    return errcode

def enSolveQ():
    errcode=dll.ENsolveQ()
    return errcode

def enOpenQ():
    errcode=dll.ENopenQ()
    return errcode

def enInitQ(int_saveflag):
    errcode=dll.ENinitQ(c_int(int_saveflag))
    return errcode

def enRunQ(time=0):
    T = pointer(c_long(time))
    errcode=dll.ENrunQ(T)
    return errcode

def enNextQ(tstep):
    t=pointer(c_long(tstep))
    errcode=dll.ENnextQ(t)
    t=t.contents.value
    return errcode,t

def enStepQ(tleft):
    t=pointer(c_long(tleft))
    errcode=dll.ENstepQ(t)
    t=t.contents.value
    return errcode,t

def enCloseQ():
    errcode=dll.ENcloseQ()
    return errcode



def enGetnodeIndex(ID):
    id=(c_char * 100)(*bytes(ID,'utf-8'))
    index = pointer(c_int(0))
    errcode=dll.ENgetnodeindex(id, index )
    index = index.contents.value
    return errcode,index

def enGetnodeID(index):
    id=(c_char * 1000)(*bytes("",'utf-8'))#创建bytes 类型
    errcode=dll.ENgetnodeid(c_int(index),id)
    id=str(id.value, encoding = "utf-8")#bytes转string
    return errcode,id

def enGetnodeType(index):
    typecode = pointer(c_int(0))
    errcode=dll.ENgetnodetype( c_int(index), typecode)
    typecode= typecode.contents.value
    return errcode,typecode

def enGetnodevalue(index,paramcode):
    value = pointer(c_float(0))
    errcode=dll.ENgetnodevalue( c_int(index),c_int(paramcode),value )
    value=value.contents.value
    return errcode,value



def enGetlinkIndex(ID):
    id=(c_char * 100)(*bytes(ID,'utf-8'))
    index = pointer(c_int(0))
    errcode=dll.ENgetlinkindex(id, index )
    index = index.contents.value
    return errcode,index

def enGetlinkID(index):
    id=(c_char * 1000)(*bytes("",'utf-8'))#创建bytes 类型
    errcode=dll.ENgetlinkid(c_int(index),id)
    id=str(id.value, encoding = "utf-8")#bytes转string
    return errcode,id

def enGetlinkType(index):
    typecode = pointer(c_int(0))
    errcode=dll.ENgetlinktype( c_int(index), typecode)
    typecode= typecode.contents.value
    return errcode,typecode

def enGetlinkNodes(linkindex):
    fromnode= pointer(c_int(0))
    tonode = pointer(c_int(0))
    errcode=dll.ENgetlinknodes(linkindex, fromnode, tonode )
    fromnode=fromnode.contents.value
    tonode=tonode.contents.value
    return errcode,fromnode,tonode

def enGetlinkvalue(index,paramcode):
    value = pointer(c_float(0))
    errcode=dll.ENgetlinkvalue( c_int(index),c_int(paramcode),value )
    value=value.contents.value
    return errcode,value

def enGetpatternid(index):
    id=(c_char * 1000)(*bytes("",'utf-8'))#创建bytes 类型
    errcode=dll.ENgetpatternid(c_int(index),id)
    id=str(id.value, encoding = "utf-8")#bytes转string
    return errcode,id


def enGetpatternindex(ID):
    id=(c_char * 100)(*bytes(ID,'utf-8'))
    index = pointer(c_int(0))
    errcode=dll.ENgetpatternindex(id, index )
    index = index.contents.value
    return errcode,index

def enGetpatternlen(index):
    len= pointer(c_int(0))
    errcode=dll.ENgetpatternlen(index, len)
    len=len.contents.value
    return errcode,len


def enGetpatternvalue(index,period):
    value = pointer(c_float(0))
    errcode=dll.ENgetpatternvalue(c_int(index),c_int(period),value )
    value =value.contents.value
    return errcode,value

def enGetcount(countcode):
    count= pointer(c_int(0))
    errcode=dll.ENgetcount( c_int(countcode), count)
    count=count.contents.value
    return errcode,count

def enGetflowunits():
    unitscode=pointer(c_int(0))
    errcode=dll.ENgetflowunits(unitscode)
    unitscode=unitscode.contents.value
    return errcode,unitscode

def enGettimeparam(paramcode):
    timevalue=pointer(c_long(0))
    errcode=dll.ENgettimeparam(paramcode,timevalue)
    timevalue=timevalue.contents.value
    return errcode,timevalue

def enGetqualtype(qualcode,tracenode):#是否需要输入，需进一步确认
    qual_code=pointer(c_long(qualcode))
    trace_node=pointer(c_long(tracenode))
    errcode=dll.ENgetqualtype(qual_code,trace_node )
    qual_code=qual_code.contents.value
    trace_node=trace_node.value
    return errcode,qual_code,trace_node

def enGetoption(optioncode):
    value=pointer(c_float(0))
    errcode=dll.ENgetoption( c_int(optioncode), value)
    value=value.contents.value
    return errcode,value
def enGetUcf(ucfcode):
    ucf=pointer(c_float(0))
    errcode=dll.ENgetUcf( c_int(ucfcode),ucf)
    ucf=ucf.contents.value
    return errcode,ucf

def enSetnodevalue(index,paramcode,value):
    errcode=dll.ENsetnodevalue( c_int(index), c_int(paramcode), c_float(value))
    return errcode

def enSetlinkvalue(index,paramcode,value):
    errcode=dll.ENsetlinkvalue(  c_int(index), c_int(paramcode), c_float(value))
    return errcode

def enSetpattern(index,factors,nfactors):
    factors=(c_float * nfactors)(*factors)#把列表传入变长
    errcode=dll.ENsetpattern(c_int(index), factors, c_int(nfactors ))
    return errcode

def enSetpattern(index,period,value):
    errcode=dll.ENsetpatternvalue(c_int(index),c_int(period), c_float(value ))
    return errcode

def enSetqualtype(qualcode,chemname,chemunits,tracenode):
    chemname=(c_char * 100)(*bytes(chemname,'utf-8'))
    chemunits=(c_char * 100)(*bytes(chemunits,'utf-8'))
    tracenode=(c_char * 100)(*bytes(tracenode,'utf-8'))
    errcode=dll.ENsetqualtype( c_int(qualcode),chemname,chemunits,tracenode )
    return errcode

def enSettimeparam(paramcode, timevalue):
    errcode=dll.ENsettimeparam( c_int(paramcode), c_long(timevalue)  )
    return errcode

def enSetoption(optioncode,value):
    errcode=dll.ENsetoption(c_int(optioncode), c_float(value ))
    return errcode

