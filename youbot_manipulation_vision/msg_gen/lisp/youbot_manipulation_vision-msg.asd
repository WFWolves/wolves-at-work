
(cl:in-package :asdf)

(defsystem "youbot_manipulation_vision-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "DetectedObjects" :depends-on ("_package_DetectedObjects"))
    (:file "_package_DetectedObjects" :depends-on ("_package"))
    (:file "BoundingBox" :depends-on ("_package_BoundingBox"))
    (:file "_package_BoundingBox" :depends-on ("_package"))
    (:file "RotatedRect" :depends-on ("_package_RotatedRect"))
    (:file "_package_RotatedRect" :depends-on ("_package"))
    (:file "DetectedObject" :depends-on ("_package_DetectedObject"))
    (:file "_package_DetectedObject" :depends-on ("_package"))
  ))