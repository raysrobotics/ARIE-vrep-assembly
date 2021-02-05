try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import sys,os
import json
import time
import numpy as np

class SimManager():
    def __init__(self, remoteIP = '127.0.0.1', remotePort = 19997) -> None:
        super().__init__()
        self.__ip = remoteIP
        self.__port = remotePort

        self.__emptybuf = bytearray()

        vrep.simxFinish(-1)
        # number clientID=simxStart(string connectionAddress,
        #           number connectionPort,
        #           boolean waitUntilConnected,
        #           boolean doNotReconnectOnceDisconnected,
        #           number timeOutInMs,
        #           number commThreadCycleInMs)
        self.__id = vrep.simxStart(self.__ip, self.__port, True, True, 5000, 5) # Connect to V-REP

        self.__peg = None
        self.__hole = None

    def clearObjects(self):
        '''
        Remove all imported objects in the scene
        '''
        res,_,_,_,_=vrep.simxCallScriptFunction(
            self.__id,
            'remoteApiCommandServer',
            vrep.sim_scripttype_customizationscript,
            'clearObjects_function',
            [],[],[],self.__emptybuf,
            vrep.simx_opmode_blocking)

        if res==vrep.simx_return_ok:
            print ('All scene objects cleared.')
        else:
            print ('Remote API clearObjects_function Error. Code: {}'.format(res))

    def loadParts(self, model_path, scale=1.0):
        '''
        Load the peg and hole mesh into the scene

        model_path = [hole_path, peg_path]
        '''
        res,retInts,_,_,_=vrep.simxCallScriptFunction(
            self.__id,
            'remoteApiCommandServer',
            vrep.sim_scripttype_customizationscript,
            'loadModel_function',
            [4, 0],[0.0001, 0.001],[model_path[0]],self.__emptybuf,
            vrep.simx_opmode_blocking)
        if res==vrep.simx_return_ok:
            h_hole = retInts[0]
            print ('Hole model loaded, handle: {0}'.format(h_hole))
        else:
            h_hole = -1
            print ('Cannot load hole model. Error code: {0}'.format(res))
            exit(-2)

        res,retInts,_,_,_=vrep.simxCallScriptFunction(
            self.__id,
            'remoteApiCommandServer',
            vrep.sim_scripttype_customizationscript,
            'loadModel_function',
            [4, 0],[0.0001, 0.001],[model_path[1]],self.__emptybuf,
            vrep.simx_opmode_blocking)
        if res==vrep.simx_return_ok:
            h_peg = retInts[0]
            print ('Peg model loaded, handle: {0}'.format(h_peg))
        else:
            h_peg = -1
            print ('Cannot load peg model. Error code: {0}'.format(res))
            exit(-2)

        res,retInts,_,_,_=vrep.simxCallScriptFunction(
            self.__id,
            'remoteApiCommandServer',
            vrep.sim_scripttype_customizationscript,
            'setObjectName_function',
            [h_hole],[],['hole'],self.__emptybuf,
            vrep.simx_opmode_blocking)
        if res==vrep.simx_return_ok:
            print ('Hole name set!') 

        res,retInts,_,_,_=vrep.simxCallScriptFunction(
            self.__id,
            'remoteApiCommandServer',
            vrep.sim_scripttype_customizationscript,
            'setObjectName_function',
            [h_peg],[],['peg'],self.__emptybuf,
            vrep.simx_opmode_blocking)   
        if res==vrep.simx_return_ok:
            print ('Peg name set!') 
        
        self.__peg = h_peg
        self.__hole = h_hole

        return [h_hole, h_peg]

    def setObjectPosition(self, obj_handle, rel_handle, position):
        # number returnCode=simxSetObjectPosition(number clientID,number objectHandle,number relativeToObjectHandle,array position,number operationMode)

        # clientID: the client ID. refer to simxStart.
        # objectHandle: handle of the object
        # relativeToObjectHandle: indicates relative to which reference frame the position is specified. Specify -1 to set the absolute position, sim_handle_parent to set the position relative to the object's parent, or an object handle relative to whose reference frame the position is specified.
        # position: the position values (x, y and z)
        # operationMode: a remote API function operation mode. Recommended operation mode for this function is simx_opmode_oneshot
        res = vrep.simxSetObjectPosition(self.__id,
            obj_handle, rel_handle,
            position,
            vrep.simx_opmode_oneshot)

        if res==vrep.simx_return_ok or res==vrep.simx_return_novalue_flag:
            print ('Position set for {}.'.format(obj_handle))
        else:
            print ('Regular API simxSetObjectPosition Error. Code: {}'.format(res))
    
    def setObjectOrientation(self, obj_handle, rel_handle, orientation):
        # number returnCode=simxSetObjectOrientation(number clientID,number objectHandle,number relativeToObjectHandle,array eulerAngles,number operationMode)

        # clientID: the client ID. refer to simxStart.
        # objectHandle: handle of the object
        # relativeToObjectHandle: indicates relative to which reference frame the orientation is specified. Specify -1 to set the absolute orientation, sim_handle_parent to set the orientation relative to the object's parent, or an object handle relative to whose reference frame the orientation is specified.
        # eulerAngles: Euler angles (alpha, beta and gamma)
        # operationMode: a remote API function operation mode. Recommended operation mode for this function is simx_opmode_oneshot
        res = vrep.simxSetObjectOrientation(self.__id,
            obj_handle, rel_handle,
            orientation,
            vrep.simx_opmode_oneshot)

        if res==vrep.simx_return_ok or res==vrep.simx_return_novalue_flag:
            print ('Orientation set for {}.'.format(obj_handle))
        else:
            print ('Regular API simxSetObjectOrientation Error. Code: {}'.format(res))

    def getObjectOrientation(self, obj_handle, rel_handle):
        retCode,curr_pos = vrep.simxGetObjectOrientation(self.__id,
                                obj_handle, rel_handle,
                                vrep.simx_opmode_blocking)
        return retCode,curr_pos

    def findLowestPoint(self, x, y, z_init, downward_depth, downward_precision):
        res,retInts,retFloats,_,_=vrep.simxCallScriptFunction(
            self.__id,
            'remoteApiCommandServer',
            vrep.sim_scripttype_customizationscript,
            'findLowestPoint2_function',
            [self.__peg, self.__hole],[downward_depth, downward_precision, x, y, z_init],[],self.__emptybuf,
            vrep.simx_opmode_blocking)   
        if res==vrep.simx_return_ok:
            if retInts[0] == 0:
                #fprintf(h_file,'%f, %f, %f\n',retFloats(1), retFloats(2), retFloats(3))
                result = '{0[0]:.5f}, {0[1]:.5f}, {0[2]:.5f}\n'.format(retFloats)
                z_init = retFloats[2]
            elif retInts[0] == -1:
                #fprintf(h_file,'%f, %f, Inf\n',retFloats(1), retFloats(2))
                result = '{0[0]:.5f}, {0[1]:.5f}, Inf\n'.format(retFloats)
                z_init = None
            else:
                result = '{:.5f}, {:.5f}, NaN\n'.format(x, y)
                z_init = None
                print('Find Lowest Point Error!\n')
                sys.exit(-1)
        else:
            result = '{:.5f}, {:.5f}, NaN\n'.format(x, y)
            z_init = None

        return retInts[0], result, z_init

    def setCameraFitToView(self):
        res = vrep.simxCallScriptFunction(self.__id,
            'remoteApiCommandServer',
            vrep.sim_scripttype_customizationscript, 
            'setCameraFitToView_function',
            [self.__peg, self.__hole],[],[],self.__emptybuf,
            vrep.simx_opmode_blocking)


