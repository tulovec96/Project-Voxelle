import websockets
import asyncio
import json
import random
import os
import copy
from utils.logging import logger

# Make sure VTube Studio is running API is enabled to port 8001
class VTSHotkeyPlugin():
    def __init__(self, config):
        self.config = config

        # Metadata
        self.main_plugin_info = {
            "pluginName": "J.A.I.son Hotkeyer",
            "pluginDeveloper": "Limit Cant Code",
        }
        self.event_plugin_info = {
            "pluginName": "J.A.I.son Event Manager",
            "pluginDeveloper": "Limit Cant Code",
        }

        # Debugging metrics
        self.debug_unseen_emotions = None
        self.debug_unseen_hotkeys = None
        self.debug_nonexist_emotions = None
        self.debug_nonexist_hotkeys = None

        # Animations setup
        self.emotion_map = {}
        self.hotkey_map = {}
        self.animations = []
        self.DEFAULT_HOTKEY_SET = None
        self.hotkey_queue = []

        self.run_data = dict()

        self.main_ws, self.event_ws = None, None
        self._trigger_hotkey_awaitable: asyncio.Future = None
        self.hotkey_execution_task, self.event_listener_task, self.message_listener_task = None, None, None
        
        self.response_job_id: str = None
        self.response_emotion_gotten: bool = False

    async def start(self):
        self.main_ws = await self._setup_ws(
            os.path.join(os.getcwd(),'tokens','vts_token_main.txt'), 
            self.main_plugin_info
        )
        self.event_ws = await self._setup_ws(
            os.path.join(os.getcwd(),'tokens','vts_token_events.txt'), 
            self.event_plugin_info
        )
        logger.info(f"Plugins successfully connected to {self.config['vts_url']}")
        
        await self._parse_hotkeys()
        logger.debug("Parsing keys finished with the following results:")
        logger.debug(f"Unused emotions: {self.debug_unseen_emotions}")
        logger.debug(f"Unused hotkeys: {self.debug_unseen_hotkeys}")
        logger.debug(f"Non-existant emotions: {self.debug_nonexist_emotions}")
        logger.debug(f"Non-existant hotkeys: {self.debug_nonexist_hotkeys}")

        self.hotkey_execution_task = asyncio.create_task(self._hotkey_exec_loop())
        logger.debug("Hotkey execution loop task initialized!")
        self.event_listener_task = asyncio.create_task(self._event_listener())
        logger.debug("Event listener task thread initialized!")
        self.message_listener_task = asyncio.create_task(self._message_listener())
        logger.debug("Message listener task initialized!")

        logger.info("VTS Hotkey Plugins successfully initialized!")

    # Setup and authenticate websocket to talk to VTube Studio instance API
    async def _setup_ws(self, token_filename: str, plugin_info: dict):
        try:
            # Connect to VTS API
            logger.debug(f"Setting up websocket {plugin_info} on {self.config['vts_url']}")
            ws = await websockets.connect(self.config['vts_url'])

            # Authenticate this Plugin
            auth_token = None
            if os.path.isfile(token_filename): # Get token from file if gotten and saved previously
                logger.debug(f"Found token file {token_filename}. Authenticating using cached token...")
                token_file = open(token_filename, 'r')
                auth_token = token_file.read()
                token_file.close()
                request = {
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": "1.0",
                    "requestID": "authenticate-plugin",
                    "messageType": "AuthenticationRequest",
                    "data": {
                        **plugin_info,
                        "authenticationToken": auth_token
                    }
                }
                await ws.send(json.dumps(request))
                response = json.loads(await ws.recv())
                if response['data']['authenticated']:
                    return ws
            
            logger.debug(f"Token file {token_filename} doesn't exist. Getting new token...")
            # If no token file or authentication with saved token fails, reauthenticate
            # Authentication request (must accept on VTS GUI)
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "get-auth-token",
                "messageType": "AuthenticationTokenRequest",
                "data": plugin_info
            }
            await ws.send(json.dumps(request))
            response = json.loads(await ws.recv())
            if 'authenticationToken' in response['data']: # Save to file
                logger.debug(f"Saving new token to {token_filename}")
                auth_token = response['data']['authenticationToken']
                token_file = open(token_filename, 'w')
                token_file.write(auth_token)
                token_file.close()
            else:
                raise Exception("Failed to get authenication token: {}".format(response))

            # Authenticate with new token
            logger.debug("Authenticating with new token...")
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "authenticate-plugin",
                "messageType": "AuthenticationRequest",
                "data": {
                    **plugin_info,
                    "authenticationToken": auth_token
                }
            }
            await ws.send(json.dumps(request))
            response = json.loads(await ws.recv())
            if not response['data']['authenticated']:
                raise Exception('Failed to authenticate VTS plugin: {}'.format(response))
            
            return ws
        except Exception as err:
            logger.error(f"Failed to setup websocket {plugin_info}: {err}")
            raise err

    # Parse configured hotkeys configuration for use by this plugin
    async def _parse_hotkeys(self):
        try:
            # Info for debugging
            POSSIBLE_EMOTION_LABELS = set(["admiration","amusement","approval","caring","desire","excitement","gratitude","joy","love","optimism","pride","anger","annoyance","disappointment","disapproval","embarrassment","fear","disgust","grief","nervousness","remorse","sadness","confusion","curiosity","realization","relief","surprise","neutral"])
            vts_info = await self._get_vts_info()
            POSSIBLE_HOTKEYS = set([hotkey[0] for hotkey in vts_info["hotkeys"]])
            self.animations = [hotkey[0] for hotkey in vts_info["hotkeys"] if hotkey[1]]

            # Config checks
            if self.config['vts_hotkey_config_file'] is None:
                raise Exception('"vts_hotkey_config_file" no configured...')
            vts_hotkey_config_filepath = os.path.join(self.config['vts_hotkey_config_file'])
            if not os.path.isfile(vts_hotkey_config_filepath):
                raise Exception('Compiled filepath: "{}" does not exist'.format(vts_hotkey_config_filepath))
            elif not self.config['vts_hotkey_config_file'].lower().endswith('.json'):
                raise Exception('Configured file: "{}" is not a json'.format(self.config['vts_hotkey_config_file']))
            
            # Load and parse
            with open(vts_hotkey_config_filepath, 'r') as hotkey_file:
                hotkey_dict = json.load(hotkey_file)
            self.debug_unseen_emotions = copy.copy(POSSIBLE_EMOTION_LABELS)
            self.debug_unseen_hotkeys = copy.copy(POSSIBLE_HOTKEYS)
            self.debug_nonexist_emotions = set()
            self.debug_nonexist_hotkeys = set()
            for hotkey_set in hotkey_dict:
                # Add to object map attributes
                self.emotion_map[hotkey_set] = hotkey_dict[hotkey_set]['emotions']
                self.hotkey_map[hotkey_set] = hotkey_dict[hotkey_set]['hotkeys']

                # set default set for idle
                if self.DEFAULT_HOTKEY_SET is None:
                    self.DEFAULT_HOTKEY_SET = hotkey_set

                # Tracking unused and non-existing for preemptive debugging
                self.debug_unseen_emotions = self.debug_unseen_emotions - set(hotkey_dict[hotkey_set]['emotions'])
                self.debug_unseen_hotkeys = self.debug_unseen_hotkeys - set(hotkey_dict[hotkey_set]['hotkeys'])
                self.debug_nonexist_emotions = self.debug_nonexist_emotions | set(hotkey_dict[hotkey_set]['emotions']) - POSSIBLE_EMOTION_LABELS
                self.debug_nonexist_hotkeys = self.debug_nonexist_hotkeys | set(hotkey_dict[hotkey_set]['hotkeys']) - POSSIBLE_HOTKEYS

        except Exception as err:
            logger.error(f"Failed to parse hotkeys: {err}")
            raise err

    # Get general info from VTS
    async def _get_vts_info(self):
        try:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "SomeID",
                "messageType": "HotkeysInCurrentModelRequest",
                "data": {}
            }

            await self.main_ws.send(json.dumps(request))
            response = json.loads(await self.main_ws.recv())
            output = {
                "model_ready": response['data']['modelLoaded'],
                "model_name": response['data']['modelName'],
                "model_id": response['data']['modelID'],
                "hotkeys": [(hotkey_obj['name'], hotkey_obj['type'] == "TriggerAnimation") for hotkey_obj in response['data']['availableHotkeys']], # hotkey[1] is True when hotkey triggers an animation
            }
        except Exception as err:
            logger.error(f"Failed to get general information from VTS: {err}")
            raise err

        return output

    # Hotkeyer that runs in a separate thread
    # Continuously trigger configured VTube Studio hotkeys queued in self.hotkey_queue
    # Will keep self.hotkey_queue filled with idle animations so queue is never empty
    # Will iterate only once when awoken by _trigger_hotkey_awaitable
    async def _hotkey_exec_loop(self):
        while True:
            logger.debug("Hotkey execution loop starting next iteration...")

            self._trigger_hotkey_awaitable = asyncio.Future()

            # Populate queue initially so there is something to play
            while len(self.hotkey_queue) < 10:
                self.hotkey_queue.append(random.choice(self.hotkey_map[self.DEFAULT_HOTKEY_SET]))

            # Request hotkey execution to VTS
            try:
                hotkey = self.hotkey_queue.pop(0)
                logger.debug(f"Requesting next hotkey: {hotkey}")
                request = json.dumps({
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": "1.0",
                    "requestID": "message_hotkey",
                    "messageType": "HotkeyTriggerRequest",
                    "data": {
                        "hotkeyID": hotkey,
                    }
                })
                await self.main_ws.send(request)
                response = await self.main_ws.recv()
                response = json.loads(response)

                if 'hotkeyID' not in response['data']:
                    logger.error(f"Failed to play hotkey: {response}")
            
                # Wait for next call to run hotkey if hotkey was not an animation
                # (non-animations are instant hotkeys that don't need to wait to finish)
                if hotkey in self.animations:
                    await self._trigger_hotkey_awaitable

            except Exception as err:
                logger.error(f"Error occured while playing hotkey this iteration: {err}")

    # Event listener that runs in a separate thread
    # Waits for currently playing animation to end (not overwritten by another animation)
    # Then triggers next hotkey to be pressed
    async def _event_listener(self):
        # Subscribe to hotkey end event
        try:
            request = json.dumps({
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "event_subscribe_anim_end",
                "messageType": "EventSubscriptionRequest",
                "data": {
                    "eventName": "ModelAnimationEvent",
                    "subscribe": True,
                    "config": {
                        "ignoreLive2DItems": True,
                        "ignoreIdleAnimations": True
                    }
                }
            })
            await self.event_ws.send(request)
            response = await self.event_ws.recv()
            response = json.loads(response)

            if 'subscribedEventCount' not in response['data']:
                raise Exception("VTS Hotkey Thread did not subscribe to event: {}".format(response))

            logger.debug("Event listener subscribed to events")
        except asyncio.InvalidStateError:
            pass
        except Exception as err:
            logger.error(f"Event listener could not subscribe to events: {err}")
            raise err
        
        # Event loop
        while True:
            event = json.loads(await self.event_ws.recv())
            logger.debug(f"Event received {event}")
            if event["data"]["animationEventType"] == "End":
                self._trigger_hotkey_awaitable.set_result(None)

    def play_hotkey_using_message(self, label: str): 
        try:
            logger.debug(f"Playing hotkey on label: {label}")

            # Get hotkeys corresponding to emotion
            set_name = self.DEFAULT_HOTKEY_SET
            for set_key in self.emotion_map:
                if label in self.emotion_map[set_key]:
                    set_name = set_key
                    break
            
            # Select random hotkey from options
            hotkey = random.choice(self.hotkey_map[set_name])
            logger.debug(f"Selected hotkey: {hotkey}")
            
            # Add to hotkey queue
            self.hotkey_queue.insert(0,hotkey)
            self._trigger_hotkey_awaitable.set_result(None)
        except asyncio.InvalidStateError:
            pass
        except Exception as err:
            logger.error(f"Error occured while playing animation on message: {err}")
            raise err

    # Interprets emotion of input message and queues the corresponding hotkey in front # TODO
    async def _message_listener(self):
        while True:
            try:
                async with websockets.connect(self.config['jaison_ws_endpoint']) as ws:
                    logger.info("Connected to JAIson ws server")
                    while True:
                        data = json.loads(await ws.recv())
                        event, status = data[0], data[1]
                        logger.debug(f"Event received {str(event):.200}")
                        
                        status, message, response = event.get("status", 500), event.get("message", "unknown"), event.get("response", {})
                        match message:
                            case "response":
                                if self.response_job_id != response.get("job_id", None):
                                    self.response_job_id = response.get("job_id", None)
                                    self.response_emotion_gotten = False
                                
                                if (not self.response_emotion_gotten) and response.get("result", {}).get("emotion", None):
                                    self.play_hotkey_using_message(response.get("result", {}).get("emotion", None))
                                    self.response_emotion_gotten = True
                            case _:
                                pass
            except OSError:
                logger.error("Server closed suddenly. Attempting reconnect in 5 seconds", exc_info=True)
                self.run_data = dict()
                await asyncio.sleep(5)
            except Exception as err:
                logger.error("Event listener encountered an error", exc_info=True)
                self.run_data = dict()
