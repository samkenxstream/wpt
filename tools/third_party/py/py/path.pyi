from typing import Any, AnyStr, Callable, ContextManager, Generic, IO, Iterable, Iterator, List, Optional, Text, Type, Union
from typing_extensions import Final, Literal
import os
import sys

class _FNMatcher(Generic[AnyStr]):
    pattern: AnyStr = ...
    def __init__(self, pattern: AnyStr) -> None: ...
    def __call__(self, path: local) -> bool: ...

class _Stat:
    path: Final[local] = ...
    mode: Final[int]
    ino: Final[int]
    dev: Final[int]
    nlink: Final[int]
    uid: Final[int]
    gid: Final[int]
    size: Final[int]
    atime: Final[float]
    mtime: Final[float]
    ctime: Final[float]
    atime_ns: Final[int]
    mtime_ns: Final[int]
    ctime_ns: Final[int]
    if sys.version_info >= (3, 8) and sys.platform == "win32":
        reparse_tag: Final[int]
    blocks: Final[int]
    blksize: Final[int]
    rdev: Final[int]
    flags: Final[int]
    gen: Final[int]
    birthtime: Final[int]
    rsize: Final[int]
    creator: Final[int]
    type: Final[int]
    if sys.platform != 'win32':
        @property
        def owner(self) -> str: ...
        @property
        def group(self) -> str: ...
    def isdir(self) -> bool: ...
    def isfile(self) -> bool: ...
    def islink(self) -> bool: ...


if sys.version_info >= (3, 6):
    _PathLike = os.PathLike
else:
    class _PathLike(Generic[AnyStr]):
        def __fspath__(self) -> AnyStr: ...
_PathType = Union[bytes, Text, _PathLike[str], _PathLike[bytes], local]

class local(_PathLike[str]):
    class ImportMismatchError(ImportError): ...

    sep: Final[str]
    strpath: Final[str]

    def __init__(self, path: _PathType = ..., expanduser: bool = ...) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __add__(self, other: object) -> local: ...
    def __cmp__(self, other: object) -> int: ...
    def __div__(self, other: _PathType) -> local: ...
    def __truediv__(self, other: _PathType) -> local: ...
    def __fspath__(self) -> str: ...

    @classmethod
    def get_temproot(cls) -> local: ...
    @classmethod
    def make_numbered_dir(
        cls,
        prefix: str = ...,
        rootdir: Optional[local] = ...,
        keep: Optional[int] = ...,
        lock_timeout: int = ...,
    ) -> local: ...
    @classmethod
    def mkdtemp(cls, rootdir: Optional[local] = ...) -> local: ...
    @classmethod
    def sysfind(
        cls,
        name: _PathType,
        checker: Optional[Callable[[local], bool]] = ...,
        paths: Optional[Iterable[_PathType]] = ...,
    ) -> Optional[local]: ...

    @property
    def basename(self) -> str: ...
    @property
    def dirname(self) -> str: ...
    @property
    def purebasename(self) -> str: ...
    @property
    def ext(self) -> str: ...

    def as_cwd(self) -> ContextManager[Optional[local]]: ...
    def atime(self) -> float: ...
    def bestrelpath(self, dest: local) -> str: ...
    def chdir(self) -> local: ...
    def check(
        self,
        *,
        basename: int = ..., notbasename: int = ...,
        basestarts: int = ..., notbasestarts: int = ...,
        dir: int = ..., notdir: int = ...,
        dotfile: int = ..., notdotfile: int = ...,
        endswith: int = ..., notendswith: int = ...,
        exists: int = ..., notexists: int = ...,
        ext: int = ..., notext: int = ...,
        file: int = ..., notfile: int = ...,
        fnmatch: int = ..., notfnmatch: int = ...,
        link: int = ..., notlink: int = ...,
        relto: int = ..., notrelto: int = ...,
     ) -> bool: ...
    def chmod(self, mode: int, rec: Union[int, str, Text, Callable[[local], bool]] = ...) -> None: ...
    if sys.platform != 'win32':
        def chown(self, user: Union[int, str], group: Union[int, str], rec: int = ...) -> None: ...
    def common(self, other: local) -> Optional[local]: ...
    def computehash(self, hashtype: str = ..., chunksize: int = ...) -> str: ...
    def copy(self, target: local, mode: bool = ..., stat: bool = ...) -> None: ...
    def dirpath(self, *args: _PathType, abs: int = ...) -> local: ...
    def dump(self, obj: Any, bin: Optional[int] = ...) -> None: ...
    def ensure(self, *args: _PathType, dir: int = ...) -> local: ...
    def ensure_dir(self, *args: _PathType) -> local: ...
    def exists(self) -> bool: ...
    def fnmatch(self, pattern: str): _FNMatcher
    def isdir(self) -> bool: ...
    def isfile(self) -> bool: ...
    def islink(self) -> bool: ...
    def join(self, *args: _PathType, abs: int = ...) -> local: ...
    def listdir(
        self,
        fil: Optional[Union[str, Text, Callable[[local], bool]]] = ...,
        sort: Optional[bool] = ...,
    ) -> List[local]: ...
    def load(self) -> Any: ...
    def lstat(self) -> _Stat: ...
    def mkdir(self, *args: _PathType) -> local: ...
    if sys.platform != 'win32':
        def mklinkto(self, oldname: Union[str, local]) -> None: ...
        def mksymlinkto(self, value: local, absolute: int = ...) -> None: ...
    def move(self, target: local) -> None: ...
    def mtime(self) -> float: ...
    def new(
        self,
        *,
        drive: str = ...,
        dirname: str = ...,
        basename: str = ...,
        purebasename: str = ...,
        ext: str = ...,
    ) -> local: ...
    def open(self, mode: str = ..., ensure: bool = ..., encoding: Optional[str] = ...) -> IO[Any]: ...
    def parts(self, reverse: bool = ...) -> List[local]: ...
    def pyimport(
        self,
        modname: Optional[str] = ...,
        ensuresyspath: Union[bool, Literal["append", "importlib"]] = ...,
    ) -> Any: ...
    def pypkgpath(self) -> Optional[local]: ...
    def read(self, mode: str = ...) -> Union[Text, bytes]: ...
    def read_binary(self) -> bytes: ...
    def read_text(self, encoding: str) -> Text: ...
    def readlines(self, cr: int = ...) -> List[str]: ...
    if sys.platform != 'win32':
        def readlink(self) -> str: ...
    def realpath(self) -> local: ...
    def relto(self, relpath: Union[str, local]) -> str: ...
    def remove(self, rec: int = ..., ignore_errors: bool = ...) -> None: ...
    def rename(self, target: _PathType) -> None: ...
    def samefile(self, other: _PathType) -> bool: ...
    def setmtime(self, mtime: Optional[float] = ...) -> None: ...
    def size(self) -> int: ...
    def stat(self, raising: bool = ...) -> _Stat: ...
    def sysexec(self, *argv: Any, **popen_opts: Any) -> Text: ...
    def visit(
        self,
        fil: Optional[Union[str, Text, Callable[[local], bool]]] = ...,
        rec: Optional[Union[Literal[1, True], str, Text, Callable[[local], bool]]] = ...,
        ignore: Type[Exception] = ...,
        bf: bool = ...,
        sort: bool = ...,
    ) -> Iterator[local]: ...
    def write(self, data: Any, mode: str = ..., ensure: bool = ...) -> None: ...
    def write_binary(self, data: bytes, ensure: bool = ...) -> None: ...
    def write_text(self, data: Union[str, Text], encoding: str, ensure: bool = ...) -> None: ...


# Untyped types below here.
svnwc: Any
svnurl: Any
SvnAuth: Any
