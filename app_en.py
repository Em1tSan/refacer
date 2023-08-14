import gradio as gr
from refacer import Refacer
import argparse
import multiprocessing as mp
import os
import shutil

def clear_temp_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

folder = 'tmp/gradio'  # Замените на ваш путь к папке
clear_temp_folder(folder)

parser = argparse.ArgumentParser(description='Refacer')
parser.add_argument("--max_num_faces", help="Max number of faces on UI", type=int, default=8)
parser.add_argument("--force_cpu", help="Force CPU mode", default=False,action="store_true")
parser.add_argument("--share_gradio", help="Share Gradio", default=False,action="store_true")
parser.add_argument("--autolaunch", help="Auto start in browser", default=False,action="store_true")
parser.add_argument("--server_name", help="Server IP address", default="127.0.0.1")
parser.add_argument("--server_port", help="Server port", type=int, default=7860)
parser.add_argument("--tensorrt", help="TensorRT activate", default=False,action="store_true")
parser.add_argument("--gpu-threads", help="number of threads to be use for the GPU", dest="gpu_threads", type=int, default=1)
parser.add_argument('--max-memory', help='maximum amount of RAM in GB to be used', dest='max_memory', type=int)
parser.add_argument('--video_quality', help='настроить качество выходного видео', dest='video_quality', type=int, default=18, choices=range(52), metavar='[0-51]')
parser.add_argument("--frame_limit", help="Maximum number of frames to process at once", dest='frame_limit', type=int, default=1000)
parser.add_argument("--use_video_path", help="Use path to video", default=False,action="store_true")
parser.add_argument("--fp16_inswapper", help=" ", default=False,action="store_true")

args = parser.parse_args()

clear_temp_folder(folder)

refacer = Refacer(force_cpu=args.force_cpu,tensorrt=args.tensorrt,gpu_threads=args.gpu_threads,max_memory=args.max_memory,video_quality=args.video_quality,frame_limit=args.frame_limit,fp16_inswapper=args.fp16_inswapper)

num_faces=args.max_num_faces

def run(*vars):
    video_path=vars[0]
    origins=vars[1:(num_faces+1)]
    destinations=vars[(num_faces+1):(num_faces*2)+1]
    thresholds=vars[(num_faces*2)+1:]
    upscaler=vars[-1]

    faces = []
    for k in range(0,num_faces):
        if origins[k] is not None and destinations[k] is not None:
            faces.append({
                'origin':origins[k],
                'destination':destinations[k],
                'threshold':thresholds[k]
            })

    # Преобразование upscaler в строку
    return refacer.reface(video_path,faces,str(upscaler))

origin = []
destination = []
thresholds = []
upscaler = []
upscaler_models = ['None']
upscaler_models += [file for file in os.listdir('upscaler_models') if file.endswith('.onnx')]
print(upscaler_models)

with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("# Refacer v 1.3.2 </br> Version by [Neurogen](https://t.me/neurogen_news) </br> [Support me](https://www.donationalerts.com/r/em1t)")
    with gr.Row():
        if args.use_video_path:
           video=gr.Text(label="Path to the original video (For example: C:\Video\example.mp4)", interactive=True)
        else:
            video=gr.Video(label="Original video ", interactive=True)
        video2=gr.Video(label="Refaced video",interactive=False,format="mp4")

    for i in range(0,num_faces):
        with gr.Tab(f"Face #{i+1}"):
            with gr.Row():
                origin.append(gr.Image(label="Face to replace"))
                destination.append(gr.Image(label="Destination face"))
            with gr.Row():
                thresholds.append(gr.Slider(label="Threshold",minimum=0.0,maximum=1.0,value=0.2))
    with gr.Row():
        #upscaler.append(gr.Radio(label="Upscaler", choices=models_ESRGAN, value=models_ESRGAN[0], interactive=True))
        upscaler.append(gr.Dropdown(label="Choose upscaler/enhacer model", choices=upscaler_models, value=upscaler_models[0], interactive=True))
    with gr.Row():
        button=gr.Button("Reface", variant="primary")

    button.click(fn=run,inputs=[video]+origin+destination+thresholds+upscaler,outputs=[video2])

#demo.launch(share=True,server_name="0.0.0.0", show_error=True)
demo.queue().launch(show_error=True,share=args.share_gradio,server_name=args.server_name,inbrowser=args.autolaunch)

#demo.launch(share=True,server_name="0.0.0.0", show_error=True)
#demo.queue().launch(show_error=True,share=False,inbrowser=True)
#e().launch(show_error=True,share=False,inbrowser=True)