
(cl:in-package :asdf)

(defsystem "youbot_scanner_lines-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :sensor_msgs-msg
)
  :components ((:file "_package")
    (:file "DetectedLaserLines" :depends-on ("_package_DetectedLaserLines"))
    (:file "_package_DetectedLaserLines" :depends-on ("_package"))
    (:file "DetectedLaserLine" :depends-on ("_package_DetectedLaserLine"))
    (:file "_package_DetectedLaserLine" :depends-on ("_package"))
  ))