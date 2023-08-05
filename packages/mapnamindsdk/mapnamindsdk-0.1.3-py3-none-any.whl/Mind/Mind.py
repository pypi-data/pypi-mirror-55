import json
import urllib

from mapnamindsdk.Mapper import Mapper as mapper
from mapnamindsdk.WS import WS as WS
import mapnamindsdk.Constants as Constants
import cherrypy
from threading import Thread


class Mind(object):

    def __init__(self):
        pass

    def removeSignal(signalName, userId):
        pass


    def createSignal(signalName, signaldescription, userId):
        #TODO Check Signal duplication with performance signals
        pass


    def setValue(signalName, value, dateAndTime, userId):
        '''
        Insert data into ONLINE table
        :param signalName:
        :param value:
        :param dateAndTime:
        :param userId:
        :return:
        '''
        pass

    @staticmethod
    def getValue(signalNames):
        '''
        Get value from ONLINE table
        :return:
        '''

        f = mapper.Mapper.getInstance()

        # Get signalId for given signalName from the Mapper
        signalID = int(f.SignalMapper[signalNames])

        # Request Body
        body = {'ids': [signalID], 'type': "TIMESERIES"}

        target_url = "http://" + Constants.DATASERVICE_SERVER_IP + ":" + Constants.DATASERVICE_PORT + "/online/get"

        req = urllib.request.Request(target_url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')

        json_data = json.dumps(body)
        json_data_as_bytes = json_data.encode('utf-8')  # needs to be bytes
        req.add_header('Content-Length', len(json_data_as_bytes))

        response = urllib.request.urlopen(req, json_data_as_bytes)
        return response.read()
        # pass
