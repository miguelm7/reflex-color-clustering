"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
import cv2
import numpy as np

from .components.navbar import navbar

from .pages.about import about

G_TAG = "G-W0XSPLQDLS"

def get_colors(image, clusters):
    def create_bar(height, width, color):
        bar = np.zeros((height, width, 3), np.uint8)
        bar[:] = color
        red, green, blue = int(color[2]), int(color[1]), int(color[0])
        return bar, (red, green, blue)
    
    img = cv2.imread(f'uploaded_files/{image}')
    width = 300
    height = 200

    # Resize the image for performance
    img = cv2.resize(img, (width, height))

    height, width, _ = np.shape(img)
    # print(height, width)

    data = np.reshape(img, (height * width, 3))
    data = np.float32(data)

    number_clusters = int(clusters)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
    # print(centers)

    font = cv2.FONT_HERSHEY_SIMPLEX
    bars = []
    rgb_values = []

    for index, row in enumerate(centers):
        bar, rgb = create_bar(200, 200, row)
        bars.append(bar)
        rgb_values.append(rgb)

    return rgb_values

# class IterState(rx.State):

#     color :list[str] = ['#%02x%02x%02x' % color for color in get_colors()]


def colored_box(color: str):
    return rx.box(
        rx.text(color),
        background_color=color,
        color=color,
        border_radius="1px",
        width="20%",
        margin="1px",
        padding="1px",)

def hex_colors(color: str):
    return rx.box(
        rx.text(color),
        background_color="white",
        border_radius="1px",
        width="20%",
        margin="1px",
        padding="1px",)

def rgb_colors(color: tuple):
    return rx.box(
        rx.text(color),
        background_color="white",
        border_radius="1px",
        width="20%",
        margin="1px",
        padding="1px",)


def simple_foreach(fun, var):
    return rx.hstack(
        rx.foreach(var, fun),
        columns=var.length(),
    )
    
def clusters_input():
    return rx.vstack(
        rx.heading(State.clusters),
        rx.input(
            placeholder="Search here...",
            value=State.clusters,
            on_change=State.clusters,
        ),
    )

# def index() -> rx.Component:
#     # Welcome Page (Index)
#     return rx.container(
#         rx.color_mode.button(position="top-right"),
#         simple_foreach(),
#     )


class State(rx.State):
    """The app state."""

    # The images to show.
    color :list[str] 
    rgb_color :list[tuple]
    img: list[str]
    show_state: bool = True
    detect_state: bool = False
    clusters : str = "5"
    clusters_selector : list[str] = ["3","4","5","6","7","8","9","10"]

    def change(self):
        self.show_state = not (self.show_state)

    def change_detect(self):
        self.detect_state = not (self.detect_state)

    async def handle_detect(self, image: str , clusters):
        self.color = ['#%02x%02x%02x' % color for color in get_colors(image, clusters)]
        self.rgb_color = get_colors(image, clusters)
        self.detect_state = True

    async def handle_delete(self, image: str ):
        self.img.remove(image)
        self.color = []
        self.detect_state = False
        self.change()

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)
        
        self.change()


color = "rgb(107,99,246)"


def index():
    """The main view."""
    return rx.container(
        navbar(),
        rx.vstack(
            rx.cond(
                State.show_state,
                    rx.upload(
                        rx.vstack(
                            rx.button("Select File", color=color, bg="white", border=f"1px solid {color}"),
                            rx.text("Drag and drop files here or click to select files"),
                        ),
                        id="upload2",
                        multiple=False,
                        accept = {
                            "image/png": [".png"],
                            "image/jpeg": [".jpg", ".jpeg"],
                            "image/gif": [".gif"],
                            "image/webp": [".webp"],
                        },
                        max_files=1,
                        disabled=False,
                        # on_keyboard=True,
                        on_drop=State.handle_upload(rx.upload_files(upload_id="upload2")),
                        border=f"1px dotted {color}",
                        padding="5em",
                    ),
                    rx.vstack(
                        rx.image(
                            src=rx.get_upload_url(State.img[-1]),
                            width="600px",
                            height="auto",
                        ),
                        rx.text(State.img[-1]),
                        rx.hstack(
                        rx.text("Select the number of colors:"),
                        rx.select(
                            State.clusters_selector,
                            value=State.clusters,
                            on_change=State.set_clusters,    
                        ),
                            rx.button(
                                "Get Palette",
                                on_click=State.handle_detect(State.img[-1], State.clusters)
                            ),
                            rx.hstack(
                                rx.button(
                                    "remove",
                                    on_click=State.handle_delete(State.img[-1]),
                                ),
                            justfy="end"
                            ),
                            justify="between",
                            align_items="center",
                        ),
                        rx.cond(
                            State.detect_state,
                            rx.vstack(
                                simple_foreach(colored_box, State.color),
                                simple_foreach(hex_colors, State.color),
                                # simple_foreach(rgb_colors, State.rgb_color)

                            ),
                            rx.container()
                            
                        )
                    ),
            ),
            width="100%",
            align="center",
            padding="5em",  

        )
    )



    

app = rx.App(
    theme=rx.theme(
        appearance="light"
    ),    
    head_components=[
        rx.script(src=f"https://www.googletagmanager.com/gtag/js?id={G_TAG}"),
        rx.script(
            f"""
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{G_TAG}');
            """
        ),
    ],
)
app.add_page(
    index,
    title="Dominant Colors from Image",
    description=
    """This tool is a simple color palette grenerator from images. 
    You can upload any image from the supported types and get a color 
    palette from the dominant colors of the image.""")
app.add_page(about,"about")