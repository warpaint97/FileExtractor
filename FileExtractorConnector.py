import ExtractFiles as ef
import FileExtractor as ui
import threading

# Global thread variable
thread = None

def only_extract_compressed_files():
    ef.copy_and_extract_compressed_files(ui.source_folder.get(), ui.source_folder.get())

def only_extract_files():
    ef.copy_files_to_target(ui.source_folder.get(), ui.target_folder.get(), get_extensions_list())

def extract_files_from_compressed_files():
    ui.add_to_log('Attempting to extract all files by extensions from the compressed files.')
    source = ui.source_folder.get()
    target = ui.target_folder.get()
    exts = get_extensions_list()
    ef.copy_and_extract_compressed_files(source, source)
    ef.copy_files_to_target(source, target, exts)
    #ui.show_success_message(f"Successfully extracted compressed files in {source} and copied {', '.join(exts)} files to {target}.")

def get_extensions_list():
    exts = ui.extension_entry.get().replace(' ', '').split(',')
    return ['.' + ext.replace('.', '') for ext in exts]

def start_thread(func):
    global thread
    if thread is not None and thread.is_alive():
        ui.add_to_log("A process is already running. Please wait until it finishes.")
        return thread
    thread = threading.Thread(target=func)
    thread.start()
    return thread

if __name__ == "__main__":
    # Connect button functions
    ui.set_extract_zips_function(lambda: start_thread(only_extract_compressed_files))
    ui.set_extract_files_function(lambda: start_thread(only_extract_files))
    ui.set_extract_files_from_zips_function(lambda: start_thread(extract_files_from_compressed_files))

    # Connect message functions
    ef.log_message = ui.add_to_log
    ef.success_message = ui.show_success_message
    ef.error_message = ui.show_error_message
    ef.show_message = ui.show_message
    
    # Start running the UI
    ui.showUI()
