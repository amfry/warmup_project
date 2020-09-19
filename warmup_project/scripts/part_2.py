import rospy
from visualization_msgs.msg import Marker

rospy.init_node('test_visual') #init node
vis_pub = rospy.Publisher('visualization_marker', Marker, queue_size=10) #creating a publisher

marker = Marker() # instance of the marker type
r = rospy.Rate(10)
marker.header.frame_id = "base_link"
marker.ns = "my_namespace"
marker.id = 0
marker.type = Marker.SPHERE
marker.action = Marker.ADD
marker.pose.position.x = 1
marker.pose.position.y = 2
marker.pose.position.z = 0
marker.pose.orientation.x = 0.0
marker.pose.orientation.y = 0.0
marker.pose.orientation.z = 0.0
marker.pose.orientation.w = 1.0
marker.scale.x = 1
marker.scale.y = 1  # 0.1
marker.scale.z = 1  # 0.1
marker.color.a = 1.0  # controls transparency of object
marker.color.r = 0.5
marker.color.g = 0.0
marker.color.b = 0.4
marker.mesh_resource = "package://pr2_description/meshes/base_v0/base.dae"
vis_pub.publish(marker)
r.sleep()