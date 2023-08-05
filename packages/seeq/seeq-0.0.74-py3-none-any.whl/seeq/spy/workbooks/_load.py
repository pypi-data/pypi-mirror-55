from ._workbook import *


def load(folder):
    """
    Loads a list of workbooks from a folder on disk into Workbook objects in
    memory.

    Parameters
    ----------
    folder : str
        A folder on disk containing workbooks to be loaded. Note that any
        subfolder structure will work -- this function will scan for any
        subfolders that contain a Workbook.json file and assume they should be
        loaded.
    """
    if not os.path.exists(folder):
        raise RuntimeError('Folder "%s" does not exist' % folder)

    workbook_json_files = glob.glob(os.path.join(folder, '**', 'Workbook.json'), recursive=True)

    workbooks = list()
    for workbook_json_file in workbook_json_files:
        workbooks.append(Workbook.load(os.path.dirname(workbook_json_file)))

    return workbooks
