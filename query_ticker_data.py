import blpapi
import datetime
from optparse import OptionParser


SESSION_TERMINATED = blpapi.Name("SessionTerminated")
RESPONSE_ERROR = blpapi.Name("responseError")
TICK_DATA = blpapi.Name("tickData")
TIME = blpapi.Name("time")
TYPE = blpapi.Name("type")
VALUE = blpapi.Name("value")
TICK_SIZE = blpapi.Name("size")
COND_CODE = blpapi.Name("conditionCodes")
CATEGORY = blpapi.Name("category")
MESSAGE = blpapi.Name("message")


def parseCmdLine():
  parser = OptionParser(description="Retrieve reference data.")
  parser.add_option("-a",
                    "--ip",
                    dest="host",
                    help="server name or IP (default: %default)",
                    metavar="ipAddress",
                    default="10.8.8.1")
  parser.add_option("-p",
                    dest="port",
                    type="int",
                    help="server port (default: %default)",
                    metavar="tcpPort",
                    default=8194)

  (options, args) = parser.parse_args()

  return options


def printErrorInfo(leadingStr, errorInfo):
  print "%s%s (%s)" % (leadingStr, errorInfo.getElementAsString(CATEGORY),
                       errorInfo.getElementAsString(MESSAGE))


def processMessage(msg):
  data = msg.getElement(TICK_DATA).getElement(TICK_DATA)

  retdata = []
  for item in data.values():
    value = item.getElementAsFloat(VALUE)
    retdata.append(value)
  return retdata


def processResponseEvent(event):
  for msg in event:
    #print msg
    if msg.hasElement(RESPONSE_ERROR):
      printErrorInfo("REQUEST FAILED: ", msg.getElement(RESPONSE_ERROR))
      continue
    return processMessage(msg)


def startSession(session):
  if not session.start():
    print "Failed to connect!"
    return False

  if not session.openService("//blp/refdata"):
    print "Failed to open //blp/refdata"
    session.stop()
    return False

  return True


def sendIntradayTickRequest(session, options):
  refDataService = session.getService("//blp/refdata")
  request = refDataService.createRequest("IntradayTickRequest")

  # only one security/eventType per request
  request.set("security", options['security'])

  # Add fields to request
  request.getElement("eventTypes").appendValue("TRADE")
  request.getElement("eventTypes").appendValue("AT_TRADE")
  request.set("includeConditionCodes", True)

  # All times are in GMT
  request.set("startDateTime", options['startDateTime'])
  request.set("endDateTime", options['endDateTime'])

  print "Sending Request:", request
  session.sendRequest(request)


def eventLoop(session):
  while True:
    # nextEvent() method below is called with a timeout to let
    # the program catch Ctrl-C between arrivals of new events
    event = session.nextEvent(500)
    if event.eventType() == blpapi.Event.PARTIAL_RESPONSE:
      print "Processing Partial Response"
      return processResponseEvent(event)
    elif event.eventType() == blpapi.Event.RESPONSE:
      print "Processing Response"
      return processResponseEvent(event)
    else:
      for msg in event:
        if event.eventType() == blpapi.Event.SESSION_STATUS:
          if msg.messageType() == SESSION_TERMINATED:
            return


def queryData(ticker):
  # Fill SessionOptions
  sessionOptions = blpapi.SessionOptions()
  sessionOptions.setServerHost('10.8.8.1')
  sessionOptions.setServerPort(8194)

  print "Connecting to %s:%d" % ('10.8.8.1', 8194)

  # Create a Session
  session = blpapi.Session(sessionOptions)

  # Start a Session
  if not session.start():
    print "Failed to start session."
    return

  if not session.openService("//blp/refdata"):
    print "Failed to open //blp/refdata"
    return


  date = datetime.datetime.now()
  # uncomment below for real time instead of demo
  #date = date.replace(second=0, microsecond=0)
  date = date.replace(month=10, day=3, hour=13, minute=30, second=0, microsecond=0)
  print 'Querying', ticker, date

  rq_options = {}
  rq_options['startDateTime'] = date
  rq_options['endDateTime'] = date
  rq_options['security'] = '%s US Equity' % ticker

  tick_data = []
  try:
    sendIntradayTickRequest(session, rq_options)
    tick_data = eventLoop(session)
  except Exception as e:
    print 'Exception raised', e
    session.stop()

  return tick_data


