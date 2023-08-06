"""
注: 本模块的行为与 pathlib, os 等模块的方法有区别或有更多限制 (目的是为了简化处
    理逻辑, 提高处理速度)
"""
import os
import sys


# ------------------------------------------------

def prettify_dir(adir: str) -> str:
    return adir.replace('\\', '/').strip('/')


def prettify_file(afile: str) -> str:
    return afile.replace('\\', '/')


# ------------------------------------------------ path getters

def get_dirname(adir: str):
    """传入目标目录的绝对路径, 返回目录名. (目录可以预先不存在)"""
    return adir.strip('/').rsplit('/', 1)[-1]


def get_filename(file: str, suffix=True):
    """传入文件的路径, 返回文件名. (路径可以是绝对路径, 相对路径或单纯文件名)"""
    if '/' in file:
        file = file.rsplit('/', 1)[-1]
    return file if suffix else file.rsplit('.', 1)[0]


def _get_launch_path():
    # NOTE: 该方法仅在 Pycharm IDE 中有效.
    path = os.path.abspath(sys.argv[0])
    return prettify_file(path)


def _get_curr_dir() -> str:
    """
    NOTE: 该方法仅在 Pycharm IDE 中有效.
    IN: _get_launch_path()
            获得启动文件的绝对路径, e.g. 'D:/workspace/my_project/launcher.py'
    OT: 返回启动文件所在的目录. e.g. 'D:/workspace/my_project/'
    """
    adir = os.path.split(_get_launch_path())[0]
    """
    'D:/workspace/my_project/launcher.py' -> 'D:/workspace/my_project'
    """
    return prettify_dir(adir)


def _find_project_dir(custom_working_entrance=''):
    """
    NOTE: 该方法仅在 Pycharm IDE 中有效.
        当从 pycharm 启动时, 项目路径就是 sys.path 的第二个元素 (sys.path[1]);
        当从 cmd 或者 pyinstaller 导出后的 exe 启动时, 项目路径就是当前文件所在
        的路径.
        如果您想要自定义项目路径, 请在启动脚本的顶部加入此代码片段:
            # test.py
            from lk_utils import file_sniffer
            file_sniffer.prj_dir = file_sniffer._find_project_dir(
                file_sniffer.curr_dir
            )
            # 或者
            file_sniffer.prj_dir = file_sniffer._find_project_dir(
                __file__
            )
    """
    if custom_working_entrance:
        p = os.path.abspath(custom_working_entrance)
    else:
        p = sys.path[1]
        
    _prj_dir = prettify_dir(p)
    
    if _prj_dir in curr_dir:  # curr_dir is a global variant from outer side.
        """
        assume_project_dir = 'D:/likianta/workspace/myprj/'
        curr_dir = 'D:/likianta/workspace/myprj/src/'
        """
        return _prj_dir
    else:
        return curr_dir


curr_dir = _get_curr_dir()
prj_dir = _find_project_dir()


# ------------------------------------------------ path stitches

def stitch_path(*path, wrapper=None):
    path = '/'.join(map(str, path))
    return path if wrapper is None else wrapper(path)


def lkdb(*subpath):
    """
    传入子路径, 返回一个以 LKDB 为入口拼接后的新路径.
    FEATURE:
        使用关键字 "{PRJ}" 表示当前项目名. 例如: 假设当前项目的项目名为
            "myproject", 则 `lkdb('{PRJ}', 'abc')` 表示
            "D:\likianta\workspace\database\myproject\abc"
            (注意: 该功能仅在 Pycharm IDE 中有效.)
    NOTE: 请事先设置 LKDB 为环境变量: (示例)
        键: LKDB
        值: D:\likianta\workspace\database
    """
    dbpath = prettify_dir(os.environ['LKDB'])
    subpath = '/'.join(map(str, subpath))
    return f'{dbpath}/{subpath}'.replace(
        '{PRJ}', get_dirname(prj_dir)
    )


# ------------------------------------------------ path finders

def find_files(adir, suffix='', rtype='filepath'):
    """
    ARGS:
        adir (str)
        suffix (str, tuple, list): 后缀名必须以 '.' 开头. 例如 '.jpg' 或
            ['.jpg', '.png'] 等
            suffix 针对不同类型的数值, 采用的策略是不同的. 有如下注意事项:
                如果 suffix 类型为 str, 则 suffix 采用的是 "模糊" 查找策略 -- 只
                要文件名中包含 suffix 就能被查找到. 比如 suffix = '.xls', 会同时
                找到 '.xls' 和 '.xlsx' 的文件; 比如 suffix = '.htm', 会同时找到
                '.htm' 和 '.html' 的文件. 这在大多数情况下是既正确又方便的.
                但 "模糊" 查找也带来了很多不确定性, 例如, 当文件中混有 'xlsx' 和
                'xlsm' (excel 模板文件) 时, 后者也会被包含进来; 此外 '.jpg' 也无
                法关联查找到 '.jpeg' (因为二者的字符串并非 "包含" 关系, 且基于效
                益考虑, 此类关联不会被支持); 而且 '.xlsx' 向 '.xls' 的关联查找也
                是不行的; 此外, 一种比较罕见的情况是, 如果有文件名为
                'A.jpg.txt', 那么也会被 suffix = '.jpg' 接纳... 因此, 如果您需要
                更确定的查找结果, 应使用 list 或 tuple类型.
                当 suffix 类型为 list 或 tuple 时, 使用的是精确查找. 比如
                ['.xls'] 的返回结果不会包含除 '.xls' 以外的文件.
        rtype (str): 'filepath'|'filename'|'dict'|'list'|'zip'
            'filepath': 返回完整路径.
                e.g. ['D:/A/B.txt', 'D:/A/C.txt']
            'filename': 返回文件名.
                e.g. ['B.txt', 'C.txt']
            'dict': 返回 {filename: filepath} 格式.
                e.g. {'B.txt': 'D:/A/B.txt', 'C.txt': 'D:/A/C.txt'}
            'list': 返回 (filenames, filepaths) 格式.
                e.g. (['B.txt', 'C.txt'], ['D:/A/B.txt', 'D:/A/C.txt'])
            'zip': 返回 zip(filenames, filepaths) 格式.
                e.g. zip((['B.txt', 'C.txt'], ['D:/A/B.txt', 'D:/A/C.txt']))
            此外, 为了简化写法, 我们提供了另外的方案:
                1. 如果只想返回文件名, 可以改用 find_filenames() 方法
    """
    adir = prettify_dir(adir)
    all_files = [x for x in os.listdir(adir) if os.path.isfile(f'{adir}/{x}')]
    
    if suffix:
        if isinstance(suffix, str):
            filenames = [x for x in all_files if suffix in x]
        else:  # type tuple | list
            # filenames = list(filter(
            #     lambda x: os.path.splitext(x)[1].lower() in suffix, all_files
            # ))
            filenames = [x for x in all_files
                         if os.path.splitext(x)[1].lower() in suffix]
    else:
        filenames = all_files
    
    if rtype == 'filename':
        return filenames
    filepaths = [f'{adir}/{x}' for x in filenames]
    if rtype == 'filepath':
        return filepaths
    if rtype == 'dict':
        return dict(zip(filenames, filepaths))
    if rtype == 'list':
        return filenames, filepaths
    if rtype == 'zip':
        return zip(filenames, filepaths)
    
    raise AttributeError  # unknown rtype


def find_filenames(adir, suffix=''):
    return find_files(adir, suffix, 'filename')


def findall_files(main_dir: str) -> list:
    collector = []
    for root, dirs, files in os.walk(main_dir):
        root = prettify_dir(root)
        collector.extend([f'{root}/{f}' for f in files])
    return collector


def find_subdirs(main_dir, return_full_path=True,
                 except_protected_folder=True) -> list:
    """
    ARGS:
        main_dir: 入口目录
        return_full_path: 返回完整路径
        except_protected_folder: 排除受保护的文件夹. 当启用时, 对以 "." 或 "__"
            开头的文件夹排除 (例如 ".git", ".idea", "__pycache__").
    """
    paths = os.listdir(main_dir)
    if except_protected_folder:
        paths = filter(
            lambda x: not (x.startswith('.') or x.startswith('__')), paths
        )
    paths = filter(lambda x: os.path.isdir(f'{main_dir}/{x}'), paths)
    if return_full_path:
        return [f'{main_dir}/{x}' for x in paths]
    else:
        return list(paths)


def findall_subdirs(main_dir: str, except_protected_folder=True) -> list:
    """
    refer: https://www.cnblogs.com/bigtreei/p/9316369.html
    """
    collector = []
    
    def my_filter(x: str):
        if except_protected_folder:
            return not (x.startswith('.') or x.startswith('__'))
        else:
            return True
    
    for root, dirs, files in os.walk(main_dir):
        root = prettify_dir(root)
        collector.extend(root + d for d in filter(my_filter, dirs))
    
    return collector


find_dirs = find_subdirs
findall_dirs = findall_subdirs


# ------------------------------------------------
# 注意: 以下方法相比 os 同名方法相比虽然速度快, 更灵活, 但是不可靠. 请谨慎使用.

def isfile(filepath: str) -> bool:
    """
    一个不很可靠的方法, 判断是否 (看起来像是) 文件的路径.
    NOTE:
        1. 当一个文件夹路径且该文件夹的名称中带点号会被误判为 "文件"
        2. 当一个文件路径且该文件不存在且该文件的名称中不含点号会误判为 "文件夹"
    """
    if os.path.exists(filepath):
        return os.path.isfile(filepath)
    if filepath.endswith('/'):
        return False
    if '.' in filepath.rsplit('/', 1)[-1]:
        return True
    else:
        return False


def isdir(dirpath: str) -> bool:
    """
    一个不很可靠的方法, 判断是否 (看起来像是) 文件夹的路径.
    """
    if dirpath in ('.', './', '/'):
        return True
    else:
        return not isfile(dirpath)


# ------------------------------------------------

def getpath(path: str):
    """
    传入一个相对于 "当前项目" 的路径, 返回它的绝对路径.
    该方法提供了一种通用的获取路径的方式, 使其不用考虑启动文件的层级.
    例如:
        假设存在项目:
            myprj
            |- A
                |- a.py
            |- B
                |- C
                    |- c.py
                |- b.txt
        其中 a 调用了 c 时, c 要读取 b.txt 就要用 'B/b.txt'.
        当从 c 自身启动时, c 要读取 b.txt 就要用 '../b.txt'.
        这就导致了不同的启动位置, 令 c 的读取路径发生了变化.
        为了避免这种变化的影响, 可以使用本方法来取得一致:
            无论是 a 调用 c 还是从 c 自身启动, c 要读取 b.txt 均使用:
                # 'B/b.txt' 是 b.txt 相对于项目根路径的路径
                filesniff.getpath('B/b.txt')
    REF: https://blog.csdn.net/Likianta/article/details/89299937#20190414185549
    """
    path = path.strip('./')
    return f'{prj_dir}/{path}'


def calc_relpath(a, x):
    """
    已知绝对路径 a, 求 "相对距离" 为 x 的某一路径.
    
    IO: a                           | x         | out
        'D:/workspace/myprj/A/B.py' | '../'     | 'D:/workspace/myprj/'
        'D:/workspace/myprj/A/B.py' | 'C/D/'    | 'D:/workspace/myprj/A/C/D/'
        'D:/workspace/myprj/A/'     | 'C/D/'    | 'D:/workspace/myprj/A/C/D/'
        'D:/workspace/myprj/A/B.py' | '../C/D/' | 'D:/workspace/myprj/C/D/'
    """
    if isfile(a):
        a = os.path.split(a)[0]
    
    if x in ('', '.', './'):
        return prettify_dir(a)
    
    if isfile(x):
        return prettify_file(os.path.abspath(os.path.join(a, x)))
    else:
        return prettify_dir(os.path.abspath(os.path.join(a, x)))


# ------------------------------------------------ interactive

def dialog(adir, suffix, prompt='请选择您所需文件的对应序号') -> str:
    """
    文件对话框.
    DEVNOTE: 本函数不建议使用 lk_logger.
    IN: 要查看的文件夹和该文件夹下的指定后缀的文件
    OT: 指定的文件的绝对路径
    """
    print(f'当前目录为: {adir}')
    
    # fn: filenames, fp: filepaths
    fn, fp = find_files(adir, suffix, 'list')
    
    if not fn:
        print('[WARNING] 当前目录没有找到表格类型的文件')
        return ''
    
    elif len(fn) == 1:
        print(f'当前目录找到了一个目标类型的文件: {fn[0]}')
        return fp[0]
    
    else:
        x = ['{} | {}'.format(i, j) for i, j in enumerate(fn)]
        print('当前目录找到了多个目标类型的文件:'
              '\n\t{}'.format('\n\t'.join(x)))

        if not prompt.endswith(': '):
            prompt += ': '
        index = input(prompt)
        return fp[int(index)]
