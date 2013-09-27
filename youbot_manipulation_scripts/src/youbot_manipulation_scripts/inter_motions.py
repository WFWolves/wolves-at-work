#!/usr/bin/env python
#author:
#version: 0.1
#description:
import sys 
import re
LIST_REGEX = re.compile("^[\[\]0-9e\-\,\.\W]*$")
def get_motion_from_string(motion_str):
        """Parses a motion from a python list string"""
        if LIST_REGEX.match(motion_str) is None:
            rospy.logerr("Error: List regex does not match!")
            return False
        else:
            try:
                lst = eval(motion_str)
                if isinstance(lst, list):
                    return lst
                else:
                    rospy.logerr("Error: Resulting Data is not a list type!")
                    return None
            except SyntaxError as exc:
                rospy.logerr("Error: SyntaxError while trying to parse motion!")
                rospy.logerr("in line: %d; offset: %d; -->%s<--" % (exc.lineno, exc.offset, exc.text))
                return None

def new_motion(start, end, num, acNum):
    result = range(5)
    print "s", "e", "sep", "td"
    for r in result:
        total_div = start[r] - end[r]
        step = total_div / num
        result[r] = round(start[r] - ((acNum + 1) * step), 4)
        print start[r], end[r], step, total_div, num, acNum
        print "result", result
    return result

if sys.argv[1] != "":
    fload = open(sys.argv[1], "r")
    data = fload.read()
    motions = get_motion_from_string(data)
    fload.close()
    print "Die Motion hat ", (len(motions)/2), " Eintraege."
    i = 0
    for x in motions:
        if isinstance(x, list): 
            print i, ":: ", x
            i += 1
    start_index = 2 * int(input("Nach welcher motion soll interpoliert werden?"))
    start_pos=motions[start_index]
    end_pos=motions[start_index + 2]
    print start_pos
    print end_pos
    number_of_inter=int(input("Wie of soll interpoliert werden?"))
    for x in range(number_of_inter-1):
        motions.insert((start_index + 2 + (x*2)), new_motion(start_pos, end_pos, number_of_inter, x))
        motions.insert((start_index + 2 + (x*2) + 1), 0.0)
    print "complete /n"
    i = 0
    for x in motions:
        if isinstance(x, list): 
            print i, ":: ", x
            i += 1
    is_override = input("[1]Ueberschreiben, [2]Speichern unter, [3]erwerfen")
    if is_override == 1:
        print "Speichern"
        fsave = open(sys.argv[1], "w")
        fsave.write(str(motions).replace(", [", ", \n["))
        fsave.close()
    elif is_override == 2:
        print "Speichern Unter"
    else :
        print "Verwerfen"
    

