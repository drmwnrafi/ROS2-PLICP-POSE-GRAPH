import rclpy
from rclpy.node import Node
from wheel_interfaces.msg import WheelInfos
import gradio as gr
import subprocess
import serial.tools.list_ports
import pandas as pd

class GUI(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.cmd_publisher = self.create_publisher(WheelInfos, 'wheel_cmd', 10)
        self.timer = self.create_timer(0.001, self.publish_values)
        self.MAX_SPEED = 15
        self.declare_parameters(
            namespace='',
            parameters=[
                ('port', 7860),
                ('address', '127.0.0.1')
            ]
        )
        self.port = self.get_parameter('port').value
        self.address = self.get_parameter('address').value
        self.port_avail = list(serial.tools.list_ports.comports())
        self.port_desc_dict = {port.device: port.description for port in self.port_avail}
        self.setup_gui()

    def publish_values(self, cmd:list):
        wheel_cmd = WheelInfos()
        wheel_cmd.cmd_value = cmd
        self.cmd_publisher.publish(wheel_cmd)

    def setup_gui(self):
        html = f"""
            <iframe src="http://{self.address}:8888/" style="width: 100%; height: 600px; border-radius: 20px;"></iframe>
        """
        with gr.Blocks() as demo:
            with gr.Row():
                gr.HTML(html)
                with gr.Tab("Control"):
                    with gr.Column():
                        direction_text = gr.Textbox(label="Robot Direction")
                        with gr.Row():
                            button_left_up = gr.Button(value="↖️")
                            button_up = gr.Button(value="⬆️")
                            button_right_up = gr.Button(value="↗️")
                        with gr.Row():
                            button_left_curve = gr.Button(value="🔁")
                            button_stop = gr.Button(value="🛑")
                            button_right_curve = gr.Button(value="🔄")
                        with gr.Row():
                            button_left_down = gr.Button(value="↙️")
                            button_down = gr.Button(value="⬇️")
                            button_right_down = gr.Button(value="↘️")
                with gr.Tab("Configuration"):
                    with gr.Column():
                        data = {'Port Available': self.port_avail}
                        df = pd.DataFrame(data)
                        gr.Dataframe(value = df, min_width=50, column_widths='50%')
                        with gr.Row():
                            left_motor_port = gr.Dropdown(self.port_desc_dict, label="Left Motor Port", interactive = True)
                            right_motor_port = gr.Dropdown(self.port_desc_dict, label="Right Motor Port", interactive = True)
                            lidar_port = gr.Dropdown(self.port_desc_dict, label="Lidar Port")
                        button_start_motor = gr.Button(value="Start Motor Node")
                        button_start_lidar = gr.Button(value="Start Lidar Node")
                        button_start_slam = gr.Button(value="Start slam_toolbox")

            button_up.click(self.up, outputs=[direction_text])
            button_down.click(self.down, outputs=[direction_text])
            button_left_up.click(self.left_up, outputs=[direction_text])
            button_right_up.click(self.right_up, outputs=[direction_text])
            button_left_down.click(self.left_down, outputs=[direction_text])
            button_right_down.click(self.right_down, outputs=[direction_text])
            button_left_curve.click(self.left_curve, outputs=[direction_text])
            button_right_curve.click(self.right_curve, outputs=[direction_text])
            button_stop.click(self.stop, outputs=[direction_text])
            button_start_motor.click(self.start_motor_node)
            button_start_lidar.click(self.start_lidar_node)
            button_start_slam.click(self.start_slam_toolbox)
            
        demo.launch(share=False, server_name=self.address, server_port=self.port)

    def up(self):
        self.publish_values([-(self.MAX_SPEED), self.MAX_SPEED])
        return f"Forward \n Speed : {-(self.MAX_SPEED), self.MAX_SPEED}"

    def down(self):
        self.publish_values([self.MAX_SPEED, -(self.MAX_SPEED)])
        return f"Backward \n Speed : {self.MAX_SPEED, -(self.MAX_SPEED)}"

    def left_up(self):
        self.publish_values([0, (self.MAX_SPEED)])
        return f"Left \n Speed : {0, (self.MAX_SPEED)}"

    def right_up(self):
        self.publish_values([self.MAX_SPEED, 0])
        return "Right"

    def left_down(self):
        self.publish_values([0, self.MAX_SPEED])
        return "Left"

    def right_down(self):
        self.publish_values([0, -(self.MAX_SPEED)])
        return "Right"

    def right_curve(self):
        self.publish_values([-(self.MAX_SPEED), -(self.MAX_SPEED)])
        return "Right"

    def left_curve(self):
        self.publish_values([self.MAX_SPEED, self.MAX_SPEED])
        return "Left"

    def stop(self):
        self.publish_values([0, 0])
        return "Stop"
    
    def start_motor_node(self):
        subprocess.Popen(['ros2', 'run', 'motor', 'motor'])
        return "Motor Node Started"

    def start_lidar_node(self):
        subprocess.Popen(['ros2', 'launch', 'lslidar_driver', 'lslidar_launch.py'])
        return "Lidar Node Started"

    def start_slam_toolbox(self):
        params_file = 'src/gui/gui/mapper_params_online_async.yaml'
        use_sim_time = 'false'
        subprocess.Popen(['ros2', 'launch', 'slam_toolbox', 'online_async_launch.py', f'params_file:={params_file}', f'use_sim_time:={use_sim_time}'])
        return "Start Mapping"


def main():
    node_name = 'gui'
    rclpy.init()
    gui = GUI(node_name)
    rclpy.spin(gui)
    gui.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
