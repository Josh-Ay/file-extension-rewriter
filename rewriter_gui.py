from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
from file_actions import get_files_and_sub_folders_in_folder, get_nested_files_in_folders_and_subfolders
from typing import Callable
import os

WHITE, DARKGREY, PALE_BLUE = "#fff", "#1d1d1d", "#81D4FA"
POPPINS_FONT = "Poppins"


class RewriterGui:
    def __init__(self):

        self.window = Tk()
        self.window.title("File Extension Rewriter")
        self.window.config(bg=WHITE, pady=20)

        self.width = 300
        self.height = 250

        self.canvas = Canvas(width=self.width, height=self.height, bg=WHITE, highlightthickness=0)
        self.canvas.grid(column=1, row=1, columnspan=4)

        self._create_main_layout()

        self.folder_to_update = ""
        self.list_of_files_to_display, self.list_of_files_to_rewrite = [], []
        self.resulting_checkboxes, self.resulting_checkbox_path_texts, self.resulting_checkbox_name_texts = [], [], []
        self.select_all_files_btn, self.new_file_extension = None, None

        self.window.mainloop()

    def _create_main_layout(self):
        """
        Creates the starting layout for the GUI.
        """
        self.get_started_text = self.canvas.create_text(150, 120,
                                                        text="Rewrite the extensions of \nfiles in a folder",
                                                        font=(POPPINS_FONT, 17), justify="center")
        self.get_started_btn = Button(text="Get Started", borderwidth=0, relief="flat", font=(POPPINS_FONT, 12),
                                      bg=DARKGREY, fg=WHITE, command=self._open_user_folders, padx=10, pady=5)
        self.get_started_btn.grid(row=2, column=1, columnspan=4)

    def _open_user_folders(self):
        """
        Opens up a dialog to select a folder and extracts all files in that folder.
        """

        # opening up a dialog to get a folder from the user's system
        self.folder_to_update = filedialog.askdirectory()

        if self.folder_to_update != "":
            # getting all the files and sub-folders in the folder
            list_of_files_in_folder, list_of_sub_folders = get_files_and_sub_folders_in_folder(self.folder_to_update)

            # updating the list of files to work on and creating a new list to hold possible files in sub-folders
            self.list_of_files_to_display, all_nested_files = [{"file_path": self.folder_to_update + "/" + file,
                                                                "name": file} for file in list_of_files_in_folder], []

            if len(list_of_sub_folders) > 0:
                # getting all of the nested files in any sub-folders and sub-sub folders
                nested_files = get_nested_files_in_folders_and_subfolders(self.folder_to_update, list_of_sub_folders,
                                                                          all_nested_files)
                for nested_file in nested_files:
                    path_to_file, files = nested_file['path_prefix'], nested_file['files']

                    # updating the list of files to work on
                    for file in files:
                        self.list_of_files_to_display.append({"file_path": path_to_file + "/" + file, "name": file})

            # updating the canvas to show the files to work on
            self._show_files_selection()

    def _show_files_selection(self, **kwargs):
        """
        Updates the GUI to show all files in the working folder.
        """
        # updating the width of the canvas and elements on canvas
        self.canvas.config(width=500)
        self.canvas.delete(self.get_started_text)
        self.get_started_btn.destroy()

        # TODO: Add scrollbar
        # scroll_bar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        # scroll_bar.grid(row=0, column=3, rowspan=10)
        # self.canvas.configure(yscrollcommand=scroll_bar.set)

        # adding a button to go back to the main layout
        back_btn = Button(text="Go back", borderwidth=0, relief="flat", font=(POPPINS_FONT, 10),
                          fg=DARKGREY, command=self._reset_layout)
        back_btn.grid(row=0, column=0, padx=20)

        # adding a button to select all the files found in the working folder
        self.select_all_files_btn = Button(text="Select all", borderwidth=0, relief="flat", font=(POPPINS_FONT, 10),
                                           fg=WHITE, bg=PALE_BLUE, command=self._select_all_files_in_folder)
        self.select_all_files_btn.grid(row=0, column=4, padx=20)

        # adding a 'title' title header
        name_header_text = Text(self.window, height=0, width=len("File"), relief="flat", font=(POPPINS_FONT, 10))
        name_header_text.insert(END, "File")
        name_header_text.grid(row=1, column=1)
        name_header_text.config(state=DISABLED)

        # adding a 'path' title header
        path_header_text = Text(self.window, height=0, width=len("Path"), relief="flat", font=(POPPINS_FONT, 10))
        path_header_text.insert(END, "Path")
        path_header_text.grid(row=1, column=2, columnspan=3)
        path_header_text.config(state=DISABLED)

        # creating variables for each checkbox and defining the row from which new checkboxes will be added
        self.list_of_files_to_rewrite, starting_row = [StringVar() for file in self.list_of_files_to_display], 2

        # deleting previous checkboxes, file names and paths when this entire function is called again
        if kwargs.get("reset_canvas") is not None:
            for previous_checkbox, previous_name, previous_path in zip(self.resulting_checkboxes,
                                                                       self.resulting_checkbox_name_texts,
                                                                       self.resulting_checkbox_path_texts):
                previous_checkbox.destroy()
                previous_name.destroy()
                previous_path.destroy()

        # creating new checkboxes specifying their names as well as their paths
        for index, file in enumerate(self.list_of_files_to_display):
            # adding a checkbox
            new_checkbox = Checkbutton(self.window, text="", variable=self.list_of_files_to_rewrite[index],
                                       onvalue=file["file_path"], offvalue="", highlightthickness=0, bd=0,
                                       bg=WHITE, command=self._check_if_all_selected)
            new_checkbox.grid(row=starting_row, column=0)

            # adding the name of the file in a Text widget
            file_name_text = Text(self.window, height=0, width=30, relief="flat", font=(POPPINS_FONT, 10))
            if len(file["name"]) > 25:
                file_name_text.insert(INSERT, file["name"][:25] + "...")
            else:
                file_name_text.insert(INSERT, file["name"])
            file_name_text.grid(row=starting_row, column=1)
            file_name_text.config(state=DISABLED)

            # adding the path of the file in a Text widget
            file_path_text = Text(self.window, height=0, width=90, relief="flat", font=(POPPINS_FONT, 10))
            if len(file["file_path"]) > 90:
                file_path_text.insert(END, file["file_path"][:90] + "...")
            else:
                file_path_text.insert(END, file["file_path"])
            file_path_text.grid(row=starting_row, column=2, columnspan=2)
            file_path_text.config(state=DISABLED)

            starting_row += 1
            self.resulting_checkboxes.append(new_checkbox)
            self.resulting_checkbox_name_texts.append(file_name_text)
            self.resulting_checkbox_path_texts.append(file_path_text)

        if kwargs.get("reset_canvas") is None:
            # adding an empty 'Text' widget to act as a separator
            empty_space = Text(self.window, height=2, width=0, relief="flat", font=(POPPINS_FONT, 10))
            empty_space.insert(END, "")
            empty_space.grid(row=starting_row + 1, column=0, columnspan=4)
            empty_space.config(state=DISABLED)

            rewrite_btn = Button(text="Rewrite selected", borderwidth=0, relief="flat", font=(POPPINS_FONT, 10),
                                 bg=DARKGREY, fg=WHITE, width=20, command=self._open_new_file_extension_selection)
            rewrite_btn.grid(row=starting_row + 2, column=2)

    def _change_select_all_btn_text(self, new_button_text: str, new_command_for_btn: Callable):
        """
        Changes the text for the 'self.select_all_files_btn' in the GUI.
        """

        # destroy previous 'select_all_files_btn' button widget
        if self.select_all_files_btn:
            self.select_all_files_btn.destroy()

        # creating a new 'select_all_files_btn' button widget
        self.select_all_files_btn = Button(text=new_button_text, borderwidth=0, relief="flat", font=(POPPINS_FONT, 10),
                                           fg=WHITE, bg=PALE_BLUE, command=new_command_for_btn)
        self.select_all_files_btn.grid(row=0, column=4, padx=20)

    def _select_all_files_in_folder(self):
        """
        Selects all the files in the working folder.
        """

        # update the 'select_all_files_btn' button
        self._change_select_all_btn_text("Unselect all", self._unselect_selected_files_in_folder)

        # select all current checkboxes
        for checkbox in self.resulting_checkboxes:
            checkbox.select()

    def _unselect_selected_files_in_folder(self):
        """
        Unselects all selected files in the working folder.
        """

        # update the 'select_all_files_btn' button
        self._change_select_all_btn_text("Select all", self._select_all_files_in_folder)

        # unselect all currently selected checkboxes
        for val in self.list_of_files_to_rewrite:
            if val.get() != "":
                val.set(0)

    def _check_if_all_selected(self):
        """
        Checks if all files in the current working folder are selected.
        """

        # getting the current selected checkboxes
        current_selected_vals = [val for val in self.list_of_files_to_rewrite if val.get() != ""]

        if len(current_selected_vals) == len(self.list_of_files_to_rewrite):
            self._change_select_all_btn_text("Unselect all", self._unselect_selected_files_in_folder)
        else:
            self._change_select_all_btn_text("Unselect selected", self._unselect_selected_files_in_folder)

    def _open_new_file_extension_selection(self):
        """
        Opens up a dialog to get the new choice of file extension.
        """

        # getting the current selected checkboxes
        current_selected_vals = [val for val in self.list_of_files_to_rewrite if val.get() != ""]

        if len(current_selected_vals) < 1:
            return messagebox.showinfo(title="Please select a file", message="You have not selected any files yet.")

        # getting the new file extension choice from the user
        self.new_file_extension = simpledialog.askstring(title="New file extension",
                                                         prompt="Please enter the new file extension you would like "
                                                                "for the selected file(s)"
                                                                " (e.g .txt, .doc, .pdf, .img)")
        if self.new_file_extension == "":
            return

        # call function to rewrite the selected checkbox items
        self._rewrite_selected_files()

    def _rewrite_selected_files(self):
        """
        Assigns selected files a new file extension.
        """

        # getting the current selected checkboxes
        current_selected_vals = [val for val in self.list_of_files_to_rewrite if val.get() != ""]

        for index, checked_val in enumerate(current_selected_vals):
            # getting the current file name and extension
            current_file_name, current_file_extension = os.path.splitext(checked_val.get())

            if self.new_file_extension[0] == ".":
                os.rename(checked_val.get(), current_file_name + self.new_file_extension)
            else:
                os.rename(checked_val.get(), current_file_name + "." + self.new_file_extension)

            # deleting the index of the rewritten file from the list of files to be displayed
            del self.list_of_files_to_display[index]

        # showing a dialog box showing informing of the number of files changed
        if len(current_selected_vals) > 1:
            messagebox.showinfo(title="Success",
                                message=f"Successfully changed extension for {len(current_selected_vals)} files")
        else:
            messagebox.showinfo(title="Success", message="Successfully changed extension for 1 file")

        continue_rewriting = messagebox.askokcancel(title="Continue", message="Would you like to continue rewriting?")

        # if the user would not like to rewrite other files in the folder
        if not continue_rewriting:
            return self._close_gui()

        self._change_select_all_btn_text("Select all", self._select_all_files_in_folder)
        self._show_files_selection(reset_canvas=True)

    def _reset_layout(self):
        """
        Resets the gui to its initial state.
        """

        self.window.destroy()
        self.__init__()

    def _close_gui(self):
        """
        Closes the gui.
        """

        messagebox.showinfo(title="Thank you", message="Thank you for trying out this automation tool.")
        self.window.destroy()
