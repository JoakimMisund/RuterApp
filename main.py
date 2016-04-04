#User created
import web, lazy

#Built in
import sys, json
from StringIO import StringIO

import datetime as dt


url_prefix = r'http://reisapi.ruter.no/'
url_getlines = r"Line/GetLines/"
url_getlinestops = r"Line/GetStopsByLineId/"
url_stops = r"Place/GetStopsRuter/"
url_departures = r"StopVisit/GetDepartures/"

def get_lines():
    url = url_prefix + url_getlines;
    lines = json_parse(web_buffer(url));

    return lines

def json_parse(obj):
    
    return json.load(StringIO(obj));


def get_start_stop(lines):
    
    result = [];
    url = url_prefix + url_getlinestops;
    for line in lines:
        
        stops = json_parse(web_buffer(url + str(line["ID"])));
        start, end = stops[0]["Name"], stops[-1]["Name"];
        result.append({line["Name"]:[start, end]});

    return result;


def get_stops():
    url = url_prefix + url_stops;
    return json_parse(web_buffer(url));

def print_numbered_list(l):
    count = 0
    while(count < len(l)):
        print u"{0}: {1}".format(count, l[count])
        count += 1
                          
def get_selection(l):
    if len(l) == 1:
        return l[0]
    index = -1;
    num_elem = len(l)
    while(index < 0 or index >= num_elem):
        print_numbered_list(l);
        index = int(input("Enter number of wanted stop: "))

    return l[index];
    
    
        
def get_departures_stop(stop_name):
    possible_stops = get_matching_stops(stop_name);
    url = url_prefix + url_departures;

    stop_names = [s[1] for s in possible_stops]
    selected_stop = get_selection(stop_names)

    stop_id = None
    for s in possible_stops:
        if s[1] == selected_stop:
            stop_id = str(s[0])
    

    req_url = url + stop_id
    departures = json_parse(web_buffer(req_url));
    return selected_stop, departures



def main():
    
    interactive_loop();


def print_cmds():
    print("Usage:\n0: exit\n1:lookup stop id\n2:Print stop's departures\n3:Next departure from with line");

def get_matching_stops(stop_name):
    matches = []
    for s in stops:
        if s["Name"].lower().startswith(stop_name.lower()):
            matches.append([s["ID"], s["Name"], s["District"]]);

    return matches


def interactive_loop():
    
    cmd = "";
    
    cmd = raw_input("Enter command (h for help): ")
    while(cmd != "0"):
          if(cmd == "h"):
              print_cmds();
          elif(cmd == "1"):
              stop_name = raw_input("Enter stop name: ").decode('utf-8');
              print get_matching_stops(stop_name)
          elif(cmd == "2"):
              stop_name = raw_input("Enter stop name: ").decode('utf-8');
              stop_name, departures = get_departures_stop(stop_name);
              print "Departures from stop: %s\n" % stop_name;
              for departure in departures:
                  print "Line %s to %s at %s, in congestion %s" %\
                      (departure["MonitoredVehicleJourney"]["LineRef"],
                       departure["MonitoredVehicleJourney"]["MonitoredCall"]["DestinationDisplay"],
                       departure["MonitoredVehicleJourney"]["MonitoredCall"]["AimedDepartureTime"],
                       departure["MonitoredVehicleJourney"]["InCongestion"])
          elif(cmd == "3"):
              stop_name = raw_input("Enter stop name: ").decode('utf-8')
              line_num = int(raw_input("Enter line number: ").decode('utf-8'))
              towards = raw_input("Enter towards stop: ").decode('utf-8')
              
#              towards = get_selection([s[1] for s in get_matching_stops(towards)])
#              print "Towards: %s" % towards
              
              time_now = dt.datetime.now()
              stop_name, departures = get_departures_stop(stop_name);
              for departure in departures:
                  #2016-04-04T14:07:00+02:00
                  time_dep = dt.datetime.strptime(departure["MonitoredVehicleJourney"]["MonitoredCall"]["AimedDepartureTime"],
                                                  "%Y-%m-%dT%X+02:00");

                  if time_dep > time_now and departure["MonitoredVehicleJourney"]["LineRef"] == str(line_num)\
                     and departure["MonitoredVehicleJourney"]["MonitoredCall"]["DestinationDisplay"].lower().startswith(towards.lower()):
                      print "Line %s to %s at %s, in congestion %s" %\
                          (departure["MonitoredVehicleJourney"]["LineRef"],
                           departure["MonitoredVehicleJourney"]["MonitoredCall"]["DestinationDisplay"],
                           departure["MonitoredVehicleJourney"]["MonitoredCall"]["AimedDepartureTime"],
                           departure["MonitoredVehicleJourney"]["InCongestion"])
                      break;
              
          cmd = raw_input("Enter command (h for help): ")    
          

web_buffer = lazy.Lazy(web.getHtml); #Buffer to be used for online requests.
stops = get_stops();
lines = get_lines();


main();
