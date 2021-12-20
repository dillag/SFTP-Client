from typing import Any, List, Union
import paramiko
import pathlib


class MySFTPClient(paramiko.SFTPClient):
    def _adjust_cwd(self, path: Any) -> str:
        return super()._adjust_cwd(str(path))

    def put(self, localpath: Union[str, pathlib.Path], remotepath: Union[str, pathlib.Path], callback=None,
            confirm=True) -> str:
        return super().put(str(localpath), str(remotepath), callback, confirm)

    def get(self, remotepath: Union[str, pathlib.Path], localpath: Union[str, pathlib.Path], callback=None,
            prefetch=True) -> str:
        return super().get(str(remotepath), str(localpath), callback, prefetch)

    def listdir_attr(self, path: Union[str, pathlib.Path], sort=False) -> List[Any]:
        if sort:
            files = super().listdir_attr(str(path))
            files.sort(key=lambda f: f.st_atime)
            return files[::-1]
        else:
            return super().listdir_attr(str(path))

    def listdir(self, path: Union[str, pathlib.Path], sort=False) -> List[Any]:
        if sort:
            return [f.filename for f in self.listdir_attr(path, sort)]
        else:
            return super().listdir(str(path))

    def get_last_filename(self, remotepath: Union[str, pathlib.Path]) -> str:
        lastfile = self.listdir_attr(remotepath, True)
        return lastfile[0].filename
