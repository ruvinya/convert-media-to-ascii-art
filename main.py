import os
import pathlib
import shutil
import sys
import time

import dearpygui.dearpygui as dpg

import mediatoascii as mta

IMAGE_FORMAT = ["tif", "tiff", "bmp", "jpg", "jpeg", "png"]
VIDEO_FORMAT = ["mp4", "mov", "avi", "webm", "gif"]

RED = (255, 0, 0)
GREEN = (0, 255, 0)
HOOKERS_GREEN = (81, 118, 100)
INCHWORM = (193, 233, 100)
RICH_BLACK = (12, 14, 7)
LIGHT_RICH_BLACK = (23, 27, 14)
RAISIN_BLACK = (38, 35, 34)
BLACK_COFFEE = (54, 40, 37)
OLD_BURGUNDY = (69, 45, 39)
LIVER_ORGAN = (99, 55, 44)
COPPER_CRAYOLA = (201, 125, 96)
MELON = (255, 188, 181)
ALMOND = (242, 229, 215)

dpg.create_context()
dpg.create_viewport(title="Media to Ascii", width=800, height=365, resizable=False)
dpg.set_viewport_small_icon("source/icon.ico")
dpg.set_viewport_large_icon("source/icon.ico")
dpg.setup_dearpygui()

with dpg.font_registry():
    default_font = dpg.add_font(mta.FONT_PATH, 20)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 8)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 3)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 12)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 12)
        dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 12)
        dpg.add_theme_color(
            dpg.mvThemeCol_WindowBg, RAISIN_BLACK, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(dpg.mvThemeCol_Text, ALMOND, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(
            dpg.mvThemeCol_FrameBg, OLD_BURGUNDY, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_FrameBgHovered, LIVER_ORGAN, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_FrameBgActive, COPPER_CRAYOLA, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_MenuBarBg, BLACK_COFFEE, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_HeaderHovered, LIVER_ORGAN, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_HeaderActive, LIVER_ORGAN, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_Header, LIVER_ORGAN, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_CheckMark, MELON, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_Button, RICH_BLACK, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_ButtonHovered, LIGHT_RICH_BLACK, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_PopupBg, OLD_BURGUNDY, category=dpg.mvThemeCat_Core
        )
    with dpg.theme_component(dpg.mvInputText):
        dpg.add_theme_color(dpg.mvThemeCol_Text, INCHWORM, category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvButton, enabled_state=False):
        dpg.add_theme_color(
            dpg.mvThemeCol_ButtonHovered, RICH_BLACK, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_ButtonActive, RICH_BLACK, category=dpg.mvThemeCat_Core
        )
    with dpg.theme_component(dpg.mvButton, enabled_state=True):
        dpg.add_theme_color(
            dpg.mvThemeCol_ButtonHovered, LIGHT_RICH_BLACK, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_ButtonActive, LIGHT_RICH_BLACK, category=dpg.mvThemeCat_Core
        )

dpg.bind_theme(global_theme)
dpg.bind_font(default_font)

with dpg.window(label="main_win", width=800, height=365, tag="main_win_tag"):

    with dpg.menu_bar():
        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Change Font")
        with dpg.menu(label="Developer Tools"):
            dpg.add_menu_item(
                label="Open Font Manager", callback=lambda: dpg.show_font_manager()
            )
            dpg.add_menu_item(
                label="Open Item Registry", callback=lambda: dpg.show_item_registry()
            )
            dpg.add_menu_item(
                label="Open Style Editor", callback=lambda: dpg.show_style_editor()
            )

    def disable_all():
        dpg.configure_item("_mt", color=HOOKERS_GREEN)
        dpg.set_value("_mtinput", "")
        dpg.disable_item("_resinput")
        dpg.set_value("_resinput", "None")
        dpg.configure_item("_res", color=HOOKERS_GREEN)
        dpg.disable_item("_invinput")
        dpg.configure_item("_inv", color=HOOKERS_GREEN)
        dpg.disable_item("_imageoptionsinput")
        dpg.configure_item("_imageoptions", color=HOOKERS_GREEN)
        dpg.disable_item("_videooptionsinput")
        dpg.configure_item("_videooptions", color=HOOKERS_GREEN)
        dpg.set_value("_finalinfo", "")
        dpg.disable_item("_finalbutton")

    def get_path():
        disable_all()
        path = pathlib.Path(dpg.get_value("_pathinput"))
        path_split = os.path.split(path)
        if path.exists():
            dpg.set_value("_pathinfo", "File found named {}".format(path_split[1]))
            dpg.configure_item("_pathinfo", color=GREEN)
            dpg.configure_item("_mt", color=COPPER_CRAYOLA)
            dpg.enable_item("_resinput")
            dpg.set_value("_resinput", "100")
            dpg.configure_item("_res", color=COPPER_CRAYOLA)
            dpg.enable_item("_invinput")
            dpg.configure_item("_inv", color=COPPER_CRAYOLA)
            dpg.set_value("_finalinfo", "Ready")
            dpg.configure_item("_finalinfo", color=INCHWORM)
            dpg.enable_item("_finalbutton")
            if path_split[1].split(".")[-1] in VIDEO_FORMAT:
                dpg.set_value("_mtinput", "Video")
                dpg.set_value("_mtinput", "Video")
                dpg.enable_item("_videooptionsinput")
                dpg.configure_item("_videooptions", color=COPPER_CRAYOLA)
            elif path_split[1].split(".")[-1] in IMAGE_FORMAT:
                dpg.set_value("_mtinput", "Image")
                dpg.enable_item("_imageoptionsinput")
                dpg.configure_item("_imageoptions", color=COPPER_CRAYOLA)
            else:
                dpg.set_value(
                    "_pathinfo",
                    "Incorrent file format, please enter a video or image file.",
                )
                dpg.configure_item("_pathinfo", color=RED)
                disable_all()
        else:
            dpg.set_value(
                "_pathinfo", "Cannot found specified path. Check it and try again."
            )
            disable_all()

    with dpg.group(horizontal=True) as path_group:
        dpg.add_text("File Path:", parent="_pathinput", color=COPPER_CRAYOLA)
        dpg.add_input_text(
            width=670,
            hint="Insert the full path of the media and then hit ENTER.",
            tag="_pathinput",
            on_enter=True,
            callback=get_path,
        )
        with dpg.tooltip(dpg.last_item()):
            dpg.add_text("Hover over file -> Shift + Right Click -> Copy as Path")

    dpg.add_text("", tag="_pathinfo")
    dpg.add_separator()

    with dpg.group(horizontal=True, tag="media_type_group") as media_type_group:
        dpg.add_text("Media Type:", parent="_mtinput", color=HOOKERS_GREEN, tag="_mt")
        dpg.add_text("", tag="_mtinput", color=GREEN)

    with dpg.group(horizontal=True, tag="inverse_group") as inverse_group:
        dpg.add_text(
            "Invert Colors:", parent="_invinput", color=HOOKERS_GREEN, tag="_inv"
        )
        with dpg.tooltip(dpg.last_item()):
            dpg.add_text("Use light colors for darker colors.")
        dpg.add_checkbox(tag="_invinput", enabled=False, default_value=False)

    with dpg.group(horizontal=True, tag="res_group") as res_group:
        dpg.add_text("Resolution:", parent="_resinput", color=HOOKERS_GREEN, tag="_res")
        with dpg.tooltip(dpg.last_item()):
            dpg.add_text("Width as character count. Larger means more resemblance.")
        dpg.add_combo((50, 100, 150), tag="_resinput", enabled=False, width=150)

    dpg.add_separator()

    with dpg.group(horizontal=True, tag="image_options_group") as image_options_group:
        dpg.add_text(
            "Image Options:",
            parent="_imageoptionsinput",
            color=HOOKERS_GREEN,
            tag="_imageoptions",
        )
        dpg.add_radio_button(
            ("Export as image", "Export as text"),
            tag="_imageoptionsinput",
            horizontal=True,
            enabled=False,
            default_value="Export as image",
        )

    with dpg.group(horizontal=True, tag="video_options_group") as video_options_group:
        dpg.add_text(
            "Video Options:",
            parent="_videooptionsinput",
            color=HOOKERS_GREEN,
            tag="_videooptions",
        )
        dpg.add_radio_button(
            ("Export (10 FPS)", "Play (10 FPS)"),
            tag="_videooptionsinput",
            horizontal=True,
            enabled=False,
            default_value="Export",
        )

    with dpg.window(
        label="Player", width=1920, height=1080, show=False, tag="play_window"
    ):
        dpg.add_text(tag="_playtext")

    def get_options():
        file_path = r"{}".format(pathlib.Path(dpg.get_value("_pathinput")))
        export_path = os.path.split(file_path)[0]
        media_type = dpg.get_value("_mtinput")
        inv = dpg.get_value("_invinput")
        res = int(dpg.get_value("_resinput"))
        image_options = dpg.get_value("_imageoptionsinput")
        video_options = dpg.get_value("_videooptionsinput")
        return [
            file_path,
            export_path,
            media_type,
            inv,
            res,
            image_options,
            video_options,
        ]

    def run():
        dpg.set_value("_finalinfo", "Running, please wait...")
        options = get_options()
        chars = mta.CHARS_ARR_R if options[3] else mta.CHARS_ARR
        if options[2] == "Video":
            process_video = mta.ProcessVideo(options[0], options[4])
            export_video = mta.ExportVideo(process_video)
            if options[6] == "Export (10 FPS)":
                export_video.save_as_video(options[1], options[4], chars)
            else:
                dpg.maximize_viewport()
                dpg.set_value(
                    "_playtext", "Please wait, video is in process (10 sec to 2 min)."
                )
                dpg.show_item("play_window")
                frame_array = export_video.prep_frame_array(options[4], chars)
                current_frame = 0
                while current_frame < len(frame_array):
                    dpg.set_value("_playtext", frame_array[current_frame])
                    current_frame = current_frame + 1
                    time.sleep(0.1)
                time.sleep(2)
                dpg.hide_item("play_window")
        elif options[6] == "Image":
            process_image = mta.ProcessImage(options[0], options[4], True)
            as_text = process_image.run(chars)
            export_image = mta.ExportPhoto(as_text, mta.FONT_PATH)
            if options[5] == "Export as image":
                export_image.save_as_image(options[1])
            else:
                export_image.save_as_text(options[1])
        else:
            sys.exit("Error")
        dpg.set_value("_finalinfo", "Done")

    with dpg.group(tag="final_group", horizontal=True) as final_group:
        dpg.add_button(
            label="     Run     ", enabled=False, tag="_finalbutton", callback=run
        )
        dpg.add_text("", tag="_finalinfo")


dpg.show_viewport()
dpg.set_primary_window("main_win_tag", True)
dpg.start_dearpygui()
dpg.destroy_context()
