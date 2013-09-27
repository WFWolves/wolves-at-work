#!/bin/bash

VALUE=$(rosparam get /youbot_main_ai/intercept_actuator)

if "$VALUE" = "true"; then
    echo "true"
    rosparam set /youbot_main_ai/intercept_actuator false
else
    echo "false"
    rosparam set /youbot_main_ai/intercept_actuator true
fi
