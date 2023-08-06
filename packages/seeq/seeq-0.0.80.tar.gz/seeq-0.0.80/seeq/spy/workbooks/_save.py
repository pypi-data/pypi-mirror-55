import os

from seeq.base import system

from ._workbook import Workbook

from .._common import Status


def save(workbooks, folder=None, *, datasource_map_folder=None, clean=False):
    """
    Saves a list of workbooks to a folder on disk from Workbook objects in
    memory.

    Parameters
    ----------
    workbooks : list[Workbook]
        A list of Workbook objects to save.

    folder : str, default os.getcwd()
        A folder on disk to which to save the workbooks. It will be saved as a
        "flat" set of subfolders, no other hierarchy will be created.

    datasource_map_folder : str, default None
        Specifies a curated set of datasource maps that should accompany the
        workbooks (as opposed to the default maps that were created during the
        spy.workbooks.pull call).

    clean : bool, default False
        True if the target folder should be removed prior to saving the
        workbooks.
    """
    status = Status()

    try:
        if not isinstance(workbooks, list):
            workbooks = [workbooks]

        if folder is None:
            folder = os.getcwd()

        if clean:
            status.update('Removing "%s"' % folder, Status.RUNNING)
            system.removetree(folder, keep_top_folder=True)

        datasource_maps = None if datasource_map_folder is None else Workbook.load_datasource_maps(
            datasource_map_folder)

        for workbook in workbooks:  # type: Workbook
            if not isinstance(workbook, Workbook):
                raise RuntimeError('workbooks argument must be a list of Workbook objects')

            workbook_folder_name = '%s (%s)' % (workbook.name, workbook.id)
            workbook_folder = os.path.join(folder, system.cleanse_filename(workbook_folder_name))

            if datasource_maps is not None:
                workbook.datasource_maps = datasource_maps

            status.update('Saving to "%s"' % workbook_folder, Status.RUNNING)
            workbook.save(workbook_folder)

        status.update('Success', Status.SUCCESS)

    except KeyboardInterrupt:
        status.update('Save canceled', Status.CANCELED)
