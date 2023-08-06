from __future__ import print_function
import logging
import configparser
import os
import vtpl_api
import json
from vtpl_api.rest import ApiException
from pprint import pprint
import requests
import urllib3
import time
import uuid

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class VtplApiWrapper(object):

    def __init__(self, capability, user_level_config_file_dir="./"):
        self.__capability = capability
        self.__read_config(user_level_config_file_dir)
        self.__init_engines_api_network()

    """
    This method is only responsible to read multi layer configurations
    of the required configs.
    No other thing should be written inside it.
    """

    def __read_config(self, user_level_config_file_dir="./"):
        tmp_config = configparser.ConfigParser()
        self.__config_file_abs_path = os.path.abspath(
            os.path.join(user_level_config_file_dir, "engine.ini"))
        LOGGER.debug(
            "Loading configuration from[%s]", self.__config_file_abs_path)
        tmp_config.read(self.__config_file_abs_path)
        ret = 0

        '''
        Handling UniqueID.my_id
        '''
        if not 'UniqueID' in tmp_config:
            tmp_config['UniqueID'] = {}
            ret += 1
        self.__my_id = str(uuid.uuid1())  # getmac.get_mac_address()
        if not tmp_config.has_option('UniqueID', 'my_id'):
            tmp_config.set('UniqueID', 'my_id', self.__my_id)
            LOGGER.debug("File[%s] does not contain [UniqueID.my_id]. Using the system UUID[%s]",
                         self.__config_file_abs_path, self.__my_id)
            ret += 1
        self.__my_id = tmp_config.get(
            'UniqueID', 'my_id', fallback=self.__my_id)
        LOGGER.debug("Final[UniqueID.my_id]=[%s]", self.__my_id)

        '''
        Handling camera.http_host
        '''
        if not 'camera' in tmp_config:
            tmp_config['camera'] = {}
            ret += 1
        self.__http_host = 'api.iot-videonetics.com:5000'
        if not tmp_config.has_option('camera', 'http_host'):
            tmp_config.set('camera', 'http_host', self.__http_host)
            LOGGER.debug("File[%s] does not contain [camera.http_host]. Using http_host[%s]",
                         self.__config_file_abs_path, self.__http_host)
            ret += 1
        self.__http_host = tmp_config.get(
            'camera', 'http_host', fallback=self.__http_host)
        LOGGER.debug("Final[camera.http_host]=[%s]", self.__http_host)

        '''
        Handling camera.http_host_protocol_scheme
        '''
        self.__http_host_protocol_scheme = 'http'
        if not tmp_config.has_option('camera', 'http_host_protocol_scheme'):
            tmp_config.set('camera', 'http_host_protocol_scheme',
                           self.__http_host_protocol_scheme)
            LOGGER.debug("File[%s] does not contain [camera.http_host_protocol_scheme]. Using http_host_protocol_scheme[%s]",
                         self.__config_file_abs_path, self.__http_host_protocol_scheme)
            ret += 1
        self.__http_host_protocol_scheme = tmp_config.get(
            'camera', 'http_host_protocol_scheme', fallback=self.__http_host_protocol_scheme)
        if ('http' != self.__http_host_protocol_scheme and 'https' != self.__http_host_protocol_scheme):
            LOGGER.debug("File[%s] contains [camera.http_host_protocol_scheme][%s] Not supported. Using http_host_protocol_scheme[http]",
                         self.__config_file_abs_path, self.__http_host_protocol_scheme)
            self.__http_host_protocol_scheme = 'http'
        LOGGER.debug("Final[camera.http_host_protocol_scheme]=[%s]",
                     self.__http_host_protocol_scheme)

        '''
        Handling camera.vs3_host
        '''
        self.__vs3_host = 'api.iot-videonetics.com:9983'
        if not tmp_config.has_option('camera', 'vs3_host'):
            tmp_config.set('camera', 'vs3_host', self.__vs3_host)
            LOGGER.debug("File[%s] does not contain [camera.vs3_host]. Using vs3_host[%s]",
                         self.__config_file_abs_path, self.__vs3_host)
            ret += 1
        self.__vs3_host = tmp_config.get(
            'camera', 'vs3_host', fallback=self.__vs3_host)
        LOGGER.debug("Final[camera.vs3_host]=[%s]", self.__vs3_host)

        '''
        Handling camera.vs3_host_protocol_scheme
        '''
        self.__vs3_host_protocol_scheme = 'http'
        if not tmp_config.has_option('camera', 'vs3_host_protocol_scheme'):
            tmp_config.set('camera', 'vs3_host_protocol_scheme',
                           self.__vs3_host_protocol_scheme)
            LOGGER.debug("File[%s] does not contain [camera.vs3_host_protocol_scheme]. Using vs3_host_protocol_scheme[%s]",
                         self.__config_file_abs_path, self.__vs3_host_protocol_scheme)
            ret += 1
        self.__vs3_host_protocol_scheme = tmp_config.get(
            'camera', 'vs3_host_protocol_scheme', fallback=self.__vs3_host_protocol_scheme)
        if ('http' != self.__vs3_host_protocol_scheme and 'https' != self.__vs3_host_protocol_scheme):
            LOGGER.debug("File[%s] contains [camera.vs3_host_protocol_scheme][%s] Not supported. Using vs3_host_protocol_scheme[http]",
                         self.__config_file_abs_path, self.__vs3_host_protocol_scheme)
            self.__vs3_host_protocol_scheme = 'http'
        LOGGER.debug("Final[camera.vs3_host_protocol_scheme]=[%s]",
                     self.__vs3_host_protocol_scheme)

        '''
        Handling camera.http_timeout
        '''
        self.__http_timeout = 1
        if not tmp_config.has_option('camera', 'http_timeout'):
            tmp_config.set('camera', 'http_timeout', str(self.__http_timeout))
            LOGGER.debug("File[%s] does not contain [camera.http_timeout]. Using http_timeout[%s]",
                         self.__config_file_abs_path, self.__http_timeout)
            ret += 1
        self.__http_timeout = tmp_config.get(
            'camera', 'http_timeout', fallback=self.__http_timeout)
        LOGGER.debug("Final[camera.http_timeout]=[%s]", self.__http_timeout)

    """
    This method is only responsible to initiate the object
    that works with the engines API.
    """

    def __init_engines_api_network(self):
        self.__configuration = vtpl_api.Configuration()
        self.__configuration.host = self.__http_host_protocol_scheme + "://" + self.__http_host
        self.__api_instance = vtpl_api.EnginesApi(
            vtpl_api.ApiClient(self.__configuration))

    """
    This method is only responsible to check if an engine is registered.
    """

    def check_if_engine_registered(self):
        ret_val = False
        machineId = {}
        machineId["machineId"] = self.__my_id
        try:
            api_response = self.__api_instance.engines_get(
                where=json.dumps(machineId))
            LOGGER.debug(
                "check_if_engine_registered() api_response %s", api_response)
            for item in api_response.items:
                LOGGER.info("Got capabilities with %s", item.capabilities)
                ret_val = True
        except ApiException as e:
            LOGGER.exception(
                "Exception when calling EnginesApi->engines_get: %s\n" % e)
        except urllib3.exceptions.ConnectionError as e:
            LOGGER.exception("Exception occured %s", e)
        except urllib3.exceptions.ConnectTimeoutError as e:
            LOGGER.exception("timeout error occured %s", e)
        except urllib3.exceptions.MaxRetryError as e:
            LOGGER.exception('Max timeout error %s', e)
        except OSError:
            LOGGER.exception("No route to host %s", e)
        return ret_val

    """
    This method is only responsible to register an engine.
    """

    def register_engine(self):
        ret_val = False
        engine = vtpl_api.Engine(
            machine_id=self.__my_id, capabilities=[self.__capability])
        api_response = None
        try:
            api_response = self.__api_instance.engines_post(
                engine=engine)
            LOGGER.debug(
                "register_engine() api_response %s", api_response)
            ret_val = True
        except ApiException as e:
            LOGGER.exception(
                "Exception when calling EnginesApi->engines_get: %s\n" % e)
        except urllib3.exceptions.ConnectionError as e:
            LOGGER.exception("Exception occured %s", e)
        except urllib3.exceptions.ConnectTimeoutError as e:
            LOGGER.exception("timeout error occured %s", e)
        except urllib3.exceptions.MaxRetryError as e:
            LOGGER.exception('Max timeout error %s', e)
        except OSError:
            LOGGER.exception("No route to host %s", e)
        return ret_val

    """
    This method is to get engine tasks
    """

    def get_engine_task(self):

        source = None
        destination = None
        capability = None
        line_info = None
        zone_info = None
        api_response = None
        source_list = None
        destination_list = None

        job_found_with_my_machine_id = False
        job_found_with_my_capability_type = False

        try:
            engineMachineId = {}
            engineMachineId["engineMachineId"] = self.__my_id
            api_response = self.__api_instance.engine_tasks_get(
                where=json.dumps(engineMachineId))
            LOGGER.debug(
                "get_engine_task()[job_found_with_my_machine_id] api_response %s", api_response)
        except ApiException as e:
            LOGGER.exception('Exception occured %s', e)
        except urllib3.exceptions.ConnectionError as e:
            LOGGER.exception("Exception occured %s", e)
        except urllib3.exceptions.ConnectTimeoutError as e:
            LOGGER.exception("timeout error occured %s", e)
        except urllib3.exceptions.MaxRetryError as e:
            LOGGER.exception('Max timeout error %s', e)
        except OSError:
            LOGGER.exception("No route to host %s", e)

        if (api_response != None):
            for item in api_response.items:
                source = item.source
                destination = item.destination
                if (source is not None) and (destination is not None):
                    job_found_with_my_machine_id = True
                    break
        if not job_found_with_my_machine_id:
            try:
                capbilitiesType = {}
                capbilitiesType["capbilitiesType"] = self.__capability
                api_response = self.__api_instance.engine_tasks_get(
                    where=json.dumps(capbilitiesType))
                LOGGER.debug(
                    "get_engine_task()[job_found_with_my_capability_type] api_response %s", api_response)
                job_found_with_my_capability_type = True
            except ApiException as e:
                LOGGER.exception('Exception occured %s', e)
            except urllib3.exceptions.ConnectionError as e:
                LOGGER.exception("Exception occured %s", e)
            except urllib3.exceptions.ConnectTimeoutError as e:
                LOGGER.exception("timeout error occured %s", e)
            except urllib3.exceptions.MaxRetryError as e:
                LOGGER.exception('Max timeout error %s', e)
            except OSError:
                LOGGER.exception("No route to host %s", e)

        if job_found_with_my_capability_type:
            if (api_response != None):
                try:
                    for item in api_response.items:
                        try:
                            source_list = item.source.source_list
                            destination_list = item.destination.destination_list
                            if (source_list is not None) and (destination_list is not None):
                                engine_task = {}
                                engine_task["engineMachineId"] = self.__my_id
                                api_response = self.__api_instance.engine_tasks_id_patch(
                                    id=item._id, if_match=item.etag, engine_task=engine_task)
                                LOGGER.debug(
                                    "get_engine_task()[patch my machine id] %s", api_response)
                                break
                        except ApiException as e:
                            LOGGER.exception(
                                'Exception[%s] to patch existing task with my engine machine id [%s]', e)
                        except urllib3.exceptions.ConnectionError as e:
                            LOGGER.exception(
                                'Exception[%s] to patch existing task with my engine machine id [%s]', e)
                        except urllib3.exceptions.ConnectTimeoutError as e:
                            LOGGER.exception(
                                'Timeout[%s] to patch existing task with my engine machine id [%s]', e)
                        except urllib3.exceptions.MaxRetryError as e:
                            LOGGER.exception(
                                'MaxRetry[%s] to patch existing task with my engine machine id [%s]', e)
                        except OSError:
                            LOGGER.exception(
                                'No route to host[%s] to patch existing task with my engine machine id [%s]', e)
                except OSError:
                    LOGGER.exception(
                        "Error to patch existing task with my engine machine id [%s]", e)
        return source_list, destination_list, capability, zone_info, line_info

    """
    This method is to sent event
    """

    def send_event(self, destination_list, snap_id, snap_abs_path, snap_name):
        if destination_list is None:
            LOGGER.warning('No destination_list set')
            return
        else:
            for item in destination_list:
                LOGGER.debug('Destination[%s]', str(item))
                event = {}
                event["eventDetails"] = {}
                event["eventDetails"]["cameraId"] = item.source_id
                event["eventDetails"]["startTimeStamp"] = int(time.time())*1000
                event["eventDetails"]["endTimeStamp"] = int(time.time())*1000
                event["metaFaceEvent"] = {}
                url, uploaded = self.__upload_image(
                    item, snap_abs_path, snap_name)
                if uploaded:
                    LOGGER.info(
                        'Event Send Success. Type[%s], Payload[%s], Ret[%s]', item.type, str(event), url)
                    try:
                        os.remove(snap_abs_path)
                        LOGGER.debug(
                            'Deleted Snap [%s], as already uploaded', snap_abs_path)
                    except Exception as e:
                        LOGGER.error(
                            'Exception to delete snap[%s] Cause[%s]', snap_abs_path, e)
                else:
                    LOGGER.warning(
                        'Event Send Failure! Type[%s], [%s]', item.type, str(event))
                # print("UPLOADED VALUE"+str(uploaded))
                # if uploaded:
                #     snap = {}
                #     snap["snap"] = url
                #     snap["processCount"] = 0
                #     snap["snapId"] = snap_id
                #     snap["featureVector1"] = []
                #     snap["registeredFaceId"] = ''
                #     snap["confidence"] = 0
                #     snap["featureVector2"] = []
                #     snap_id = self.__post_event_snap(snap)
                #     print("SNAP ID VALUE IS::::"+str(snap_id))
                #     event["eventSnaps"].append(snap_id)
                #     self.__post_event(json.dumps(event))

        return

    """
    This method is to upload image
    """

    def __upload_image(self, destination, snap_abs_path, snap_name):
        destination_type = destination.type.lower()
        url = None
        uploaded = False
        if (destination_type == 'http' or destination_type == 'https'):
            url = self.post_image(destination, snap_abs_path, snap_name)
            LOGGER.debug(
                'Snap uploaded to [%s] Path[%s]  Return URL[%s]', destination_type, snap_abs_path, url)
            uploaded = True
        return url, uploaded

    def post_image(self, destination, snap_abs_path, snap_name):
        ret = None
        content_type = "image/jpeg"
        host_url = destination.base_url
        additional_url = destination.name
        if host_url == "":
            host_url = self.__vs3_host
        host_url = self.__vs3_host
        if ('http://' not in host_url and 'https://' not in host_url):
            api_url = self.__vs3_host_protocol_scheme + '://' + host_url
            if (host_url.endswith("/") or additional_url.startswith("/")):
                api_url = api_url + additional_url
            else:
                api_url = api_url + '/' + additional_url
        else:
            api_url = host_url + additional_url
        LOGGER.debug(
            'Going to post image ApiUrl[%s] FilePath[%s]', api_url, snap_abs_path)
        try:
            headers = {
                'content-type': "multipart/form-data",
                'cache-control': "no-cache"
            }
            files = {
                'filename': (snap_name, open(snap_abs_path, 'rb'))
            }
            r = requests.request(method="POST", url=api_url,
                                 data=headers, files=files)
            LOGGER.debug(
                'Status Response to upload file[%s] at[%s] : Status[%s] Text[%s]', snap_abs_path, api_url, r.status_code, r.text)

            if (r.status_code == 201 or r.status_code == 200):
                LOGGER.debug(
                    'Response to upload file[%s] at[%s] : Created', snap_abs_path, api_url)
                json_response = r.json()
                # json_response = {"items":[{"Location":"\\upload\\Durga_Puja_DS.jpg"}]}
                LOGGER.debug(
                    'Return JSON from upload file[%s] at[%s] : [%s]', snap_abs_path, api_url, json_response)
                ret = json_response['items'][0]['Location']
                LOGGER.debug(
                    'Return URL from upload file[%s] at[%s] : [%s]', snap_abs_path, api_url, ret)
        except ConnectionError:
            LOGGER.info('restpai client connection error')
        except Exception as e:
            LOGGER.info('rest_api_client (post_image), error: [%s]', e)

        return ret

    def construct_url(self, source_list):
        source_url = ''
        for item in source_list:
            if (item.type == 'http' or item.type == 'https'):
                source_url = item.base_url
                break
            elif (item.type == "rtsp"):
                source_url = "rtsp://" + item.user + \
                    ":" + item._pass + "@" + item.base_url[7:]
                break
        return source_url

    def get_capability(self):
        return str(self.__capability)

    def stop(self):
        pass
